# Keylime: Enabling Trust in the Cloud - QEMU/KVM
## Table of Contents
* [Project Background and Current Solutions](#project-background-and-current-solutions)
  * [Automated](#automated)
  * [Manual](#manual)
* [Project Vision and Goals](#project-vision-and-goals)
* [Project Scope and Features](#project-scope-and-features)
* [Project Users and Personas](#project-users-and-personas)
  * [Configuring keylime](#configuring-keylime)
  * [Running keylime](#running-keylime)
  * [Provisioning](#provisioning)
  * [Using keylime CA](#using-keylime-ca)
* [Report a Security Vulnerability](#report-a-security-vulnerability)
* [Meeting Information](#project-meetings)
* [First Timers Support](#first-timers-support)
* [Additional Reading](#additional-reading)
* [License](#license)
## Project Background and Current Solutions
In cloud computing, users running applications on Infrastructure-as-a-Service (IaaS) nodes can not verify for themselves that the resources they are using are secure. Because of this, they must fully trust the cloud service provider that nothing (from the hypervisors to the OS) has been compromised. This raises a concern, because the user does not know if the resources are controlled by malicious insiders and rogue organizations. 

A Trusted Platform Module (TPM) is a hardware chip with secure key generation and storage functionalities. It contains Platform Configuration Registers (PCRs) that are able to store measurements of system integrity in firmwares, hypervisors, OSes, etc. Through this, it can verify if the system has been altered or tampered with. However, using TPMs is complex, can lead to slower performance, and not compatible with virtualized machines (because it is a physical device).

Keylime is a bootstrapping and integrity management software tool that connects the security features of TPMs to cloud computing.  It allows users to verify that every level of their remote system has not been compromised or tampered with, without having to deal with the drawbacks mentioned before. It also continuously measures system integrity by monitoring the cloud (IaaS) nodes, also known as Keylime agents. 

The Keylime system includes four main executable components: a cloud verifier that periodically checks the integrities of the nodes, a registrar that stores public attestation identity keys (AIKs) of TPMs, an agent node that is able to communicate with the TPM, and the tenant client that a user can use to interact with the three previously mentioned components.

Keylime consists of two main services (**trusted bootstrapping** and **continuous attestation**). A **registration** phase/minor service is needed before the two main services can be used. 
  
 **Registration (How do I know that I am talking to a valid/real TPM?)**
 
Before any other services begin, Keylime must start with a registration process involving the hardware TPM and Keylime registrar. The hardware TPM must prove that it is a valid TPM to the Keylime registrar by first cryptographically giving its public AIK to the registrar. The registrar then asks to the TPM to decrypt a message with its private key, and stores the public AIK if the decrypted message is correct. By having a valid AIK, the registrar can verify a quote that is signed by the TPM's AIK.
 
 **Trusted Bootstrapping (How do I give my cloud node an secret key/cryptographic identity?)**
 
To make a cloud node (agent and VM) unique to the tenant (cloud user), secrets and identities must be placed inside the VM. For example, if tenants wanted to provision a username and password to protect their AWS node, they would need to give the secrets directly to Amazon and trust that Amazon will put these secrets into their cloud node. Keylime's bootstrapping service allows tenants to put secret keys into their cloud nodes without having to go through the cloud service provider as a "trusted" middle man. 
 
 ![Trusted Bootstrapping p1](/assets/images/boot_p1.png)

 
In the figure above, the tenant will first generate a new bootstrap secret key for cloud node being provisioned, and splits the key into two pieces (named U and V). The tenant keeps one piece (U) to give directly to the cloud node (agent), and gives the other piece (V) to the verifier. The verifier will request a quote, which is a signed report of system integrity measurements (PCRs), from the cloud node's TPM. The verifier will also provide a nonce (random number) that it asks the cloud node to return along with the quote. This will ensure the verifier that the quote being returned is fresh and not obselete.  

The cloud node with its TPM will sign the quote and nonce with the TPM's AIK, and returns this along with another key (NK). The verifier will check with the registrar to see if the AIK signature is valid. If it is valid and the system integrity is good, it will encrypt the V key piece with NK and send this to the verifier.  
  
   ![Trusted Bootstrapping p2](/assets/images/boot_p2.png)
  
In the figure above, the tenant does a similar attestation test to check for system integrity and the TPM's validity. It will also return the U key piece in a similar way compared to the verifier with the V key piece. This way, both parts of the key are sent to the node securely,and the node can recombine the key. This key can decrypt the node’s configuration data including private keys sent to the node via configuration service.

**Continuous Attestation (How can I continuously monitor to see if the node has been tampered with?)**

Once trust is established through the bootstrapping phase, Keylime needs to ensure the tenant that the node has not been compromised over time. 

![System diagram of Keylime implementation](/assets/images/attest_succ.png)
 
The verifier will continuously request quotes (with nonces) from the cloud node/agent. Each request induces the node to retrieve a quote from its TPM (or vTPM). The quote is returned to verifier, which cryptographically verifies if the quote is valid. If it is invalid (denoting system state of the reporting node has somehow changed), the verifier issues a revocation notice to the certificate authority (tenant). Once tenant receives revocation notice, it should invalidate the affected nodes’ keys, effectively breaking all crypto related network connections and services for the node.

Please note that the diagrams and procedures mentioned above are for the **Xen** implementation. Because the Xen implementation comes with a virtual TPM that is directly linked to the hardware TPM, Keylime can use a deepquote function to communicate directly with the hardware TPM for quotes.

## Project Vision and Goals

Keylime: Enabling Trust in the Cloud - QEMU/KVM is an extension of the current implementation of the Keylime project. Because the Xen and KVM hypervisors differ in how a virtual/emulated TPM is set up for a VM, a new Keylime system structure is blueprinted specifically for KVM (see in solution concept). There are two roles under the KVM solution framework, the cloud node with real hardware TPM on it is the **Provider**, and the virtual machine running on the node is called **Tenant**. We will aim to develop provider cloud verifier interface, which tenant verifier can ask for a quote from the hardware TPM. The high-level goals of this project are as follows:

1. Instantiate each component of Keylime (for KVM)  in a VM or container
2. Investigate (and implement) a registration process for KVM
3. Create a Merkle tree implementation that will be used by the cloud verifier to handle and batch up many quote requests, and create an interface layer to abstract from the Merkle Tree layer
4. Create an interface for the tenant verifier to communicate with the cloud verifier

These goals will be explained in the solution concept.

## Project Users and Personas
The Keylime extension will be used by cloud service providers, cloud service users, and developers.  It specifically targets open-source cloud users, since QEMU/KVM is the most popular open-source hypervisor. 

Ideally, cloud service providers will run Keylime on their servers.  This would include having a Keylime verifier and registrar to monitor system integrity in addition to any other nodes. However, this still restricts integrity verification to cloud providers.  Keylime is mainly intended to benefit cloud service users. In the KVM implementation, both the user and service provider will run their own Keylime implementations and communicate with each other in a verifiable way to establish trust. This way, instead of just trusting the "all clear" message from cloud providers, users can see for themselves that the nodes they are using have not been compromised.

The Keylime extension will also be used by the Keylime development community to push the project forward. The community is committed to introducing and integrating new security verification features for cloud computing.

In general, Keylime targets organizations that could benefit from cloud computing, but are reluctant to use it due to security limitations in protecting sensitive data.  These organizations include, but are not limited to, the government, medical organizations, and financial institutions.

The Keylime extension does not target users who have a non-QEMU/KVM hypervisor.

## Project Scope and Features

What is in scope of the project:
- Add any functionalities needed for Keylime to support vTPM in KVM
- Get all currently implemented system components up and running in a VM
- Investigate and design methods to implement the registration process
- Implement and store Merkle trees in the Keylime system as a way to handle multiple quote requests to the TPM via cloud verifier
- Add changes or additions to Keylime codebase (libraries) for KVM support
- Edit APIs so that Keylime components can send the proper data needed to each other (Merkle trees, keys, etc.)

What is NOT in scope of the project:
- Communicate between the hardware TPM directly from the virtual TPM via deepquote function (possible only in the Xen version of Keylime)
- Improve features of the Xen implementation

## Solution Concept
The main high-level system components of the Keylime extension are Keylime itself, the QEMU/KVM hypervisor (including the virtual TPM), and the Trusted Platform Module (TPM): Version 2.0.

- System components
  - QEMU/KVM hypervisor
  - Hardware TPM (using TPM emulator instead when developing)
  - Libvert library
  - TPM Emulator
  - Keylime used by the user/tenant
    - Tenant Cloud Verifier
    - Tenant Registrar
    - Keylime agent (in the VM/resource)
  - Keylime used by the cloud provider
    - Provider Registrar
    - Provider Cloud Verifier
    - Keylime agent (outside the VM/resource, used by the cloud provider)
  
  
### Desired architecture
 
![System diagram of Keylime implementation](/assets/images/architecture.png)

Instead of having the vTPM directly communicate with the TPM, as was done in the XEN implementation of Keylime, we will rather have the cloud provider deploy a second instance of Keylime on it's host machine/physical hardware and have the provider's Keylime components interact with the tenant's Keylime components. This is because the guest VM has a emulated TPM that has no link to the hardware TPM, so the tenant must communicate with the hardware TPM for quotes to check the integrity of the underlining cloud node. 

We will need to write an interface for the provider verifier to send the current root to the provider node and the node the result quote back. We need to still decide whether the Merkle Tree will live on the provider node or provider verifier. We need to write interface endpoints for the tenant verifier to communicate with the provider verifier to request quotes asynchronously, and an interface layer to abstract from the Merkle Tree. We still need to figure out the registration process that will let both the tenant registrar to know where and which one is its provider using IP address. Furthermore it also need the public AIK key from the provider to validate quote from hardaware TPM. Before we implement the registrartion process, we will using hardcoding provider info inside the tenant. 

![System diagram of Merkle Tree implementation](/assets/images/merkel_tree.jpg)

A host machine will have many VMs/cloud nodes up and running (each with an instance of Keylime), and each tenant verifier will send quote requests with different nonces to the provider verifier. Because the hardware TPM is slow for processing and returning a quote, the provider verifier (or provider agent/node) can store all the nonces in a Merkle tree data structure. With the hashed data structure, the provider verifier can send a single quote request to the hardware TPM with the root of the Merkle tree as the nonce, and receive a quote. By leveraging the proof function in the Merkle tree, the provider verifier can then send the quote, the root of Merkle tree and the according proof to all tenant verifiers that requested a quote.

### Change of Verifier State Machine
The verifier in the Keylime works in the schema of a state machine. There is a function inside called ![process_agent](https://github.com/BU-NU-CLOUD-F19/Keylime-_Enabling_Trust_in_the_Cloud_QEMU-KVM/blob/7ec8fd3050cd0cf7c50a73a0706cd741c42911b0/keylime/cloud_verifier_tornado.py#L549) which takes in the operational instruction. It perfroms state transforming according to the input and current state, and perform relevant operations.

The former workflow of verifier is shown as blow:
![Former state machine](/assets/images/state_machine_former.png)
First is the bootstrapping process:
When an agent is provisioned by the tenant though a POST request from tenant, like `keylime_tenant -t 127.0.0.1 -f /home/zycai/Keylime_test/keylime/README.md`.
Then it starts to ask a quote from agent. If the request fails, it will retry until it successes or reach the maximum number of retries(user-defined).
Next it will provide the V (first half of initial secret) to the agent. There is also a fail-retry handling for this step. 

After providing V, it will enter the attestation process, which is the self-loop of `get_quote`.

Since we need to develope the process of getting provider's quote, we need to change the state-machine. The modified state-machine is shown below:
![New_state_machine](/assets/images/state_machine_newer.png)

The request for a provider quote happens in the bootstrapping process, so we add the new state `Get Provider's quote`in front of the `Provide V` state. We also add fail-retry handling for this state similarly.

Inside the verifier, we have a agent dictionary to store all the information about the agent. Inside the dictionary, we add a key-value pair `need_provider_quote` to differentiate whether the agent is provider or not.  If the agent is cloud node, that means it is the provider, so `need_provider_quote` is False, it goes to the `Provide V` state directly. If the agent is a VM on cloud node, the `need_provider_quote` is Ture, it will go to the `Get Provider's quote` state to ask a quote from provider. Also, because we haven't implement the registration process, we manually enter the identity of agent through tenant terminal when provisioning the agent. 

Inside the state `Get Provider's quote`, we send a GET request to the provider verifier, with parameters  nonce, mask and vmask. Since the registration processing has not implement yet, we use the ip address entered from the tenant to indicate where the provider is. How the endpoint in the provider verifier process the request will be discussed in the next section. After getting provider quote back, the tenant verifier will validate the quote (will discuss in the Verification of quote section). If the quote is invalid, it will go to the `Invalid Quote` state and stall there. Otherwise, it will continue following the bootstrapping process, go to the `Provide V` state.


### REST API and Endpoint design
We design an API inside the verifier for tenant verifier to invoke when it need provider's quote. We define a new endpoint for the API `'provider's ip':'verifier port'/verifier?nonce=$=&mask=&vmask=`. The tenant uses the provider's IP address to locate the provider, passes parameters needed to generate a quote. After receiving requests from tenant verifiers, the provider verifier will aggregate nonce from multiple request from differe tenant verifiers and grows a Merkle tree (details will illustrate in the next section). Then the provider verifier will use the root of the Merkle tree as the new nonce to ask for a quote from its agent. After getting quote from its own agent, provider verifier will forward this quote back to tenant verifier along with the root of the Merkle tree and the proof of Merkle tree (illustrate in next dsection). And the tenant verifier will be able to verify the quote using the information above. 
![Rest_API.png](/assets/images/Rest_API.png)
### Nonce Aggregation with Merkle tree

### Verification of quote

## Acceptance Criteria

The minimum acceptance criteria for this project is a working Keylime port to QEMU/KVM in Python 3.6. The MVP for our projects are: 
- Create a streamlined API for communication between tenant verifier and provider verifier, including workflow modification in tenant verifier
- Aggregate nonces from tenant verifier in the provider verifier with Merkle tree, ask for quote with root of the Merkle tree and send proof back alone with quote
- Verify the quote quote from provider verifier

The stretch goals of the Keylime extension is to implement registration process, clarify concepts on how to deliver a public AIK (attestation key) of the hardware TPM to the tenant registrar (involves a certificate authority and libvirt)

## Installing and Deploying our Keylime Prototype 
For this project we built two main demonstrations

1. A new commnucation pipeline between verifiers to allow tenant verifiers to request a quote from the provider verifier's agent which

2. A new method to handle quote requests in the verifier, it will bath quote request nonces into a merkle tree when they are either concurrent or the hardware TPM is busy. Then the verifier also handles redistrobution of the quotes, merkle tree head, and relavent proofs to the tenant verifiers. 

The following provides information on how to setup our prototype keylime environment, as well as run demos proving the validity of the above features. 

Please begin this process by cloning our repository and ensuring you have ![VirtualBox](https://www.virtualbox.org/wiki/Downloads) downloaded

### Environment Setup 

To run our demonstrations the keylime environments can either be provisioned automatically with Vagrant or manually vi the virtualbox GUI 

Instructions for both are shown below

We STRONGLY recommend using Vagrant and the automatic provisioning process due to the complex setup keylime requires, however Vagrant has been shown to cause some issues with windows users on this project 

#### Vagrant Setup (recomended)

A `Vagrantfile` is available for automatically provisioning the vitual machines. For even more information on this vagrant setup see the original ![ansible-keylime-tpm-emulator repository](https://github.com/keylime/ansible-keylime-tpm-emulator)

1. Navagate to `Vagrantfile` with `cd keylime_environment_setup`
2. Run `vagrant --instances=2 --repo=<user_home>/Keylime-_Enabling_Trust_in_the_Cloud_QEMU-KVM/keylime_master --cpus=2 --memory=2048  up --provider virtualbox --provision`
     - make sure `repo` is set to the location `keylime_master`
     - This will create two VMs named `Keylime1` and `keylime2` 
3. Connect to the two VMs by bringing up to terminals already in the `keylime_environment_setup` directory and then run `vagrant --instances=2 ssh keylime1` in the first terminal and `vagrant --instances=2 ssh keylime2` in the second terminal 
4. Navigate to the root directory in both VMs with the command `sudo su -`
5. Ensure keylime shared folder is working with `cd keylime_master` and then run `python3 setup.py install` to ensure the keylime codebase is loaded properly
6. Then run `tpm2_getrandom 8` in each VM to ensure the TPM emulator is running, the ouput should be similar to the following
     - `0x6F 0xA7 0xE0 0x28 0x98 0x33 0x62 0x78`
     - If function returns an error try to start the tpm server with `tpm_serverd` and try again 
7. Finally, for each VM, open 3 more Terminals and redo steps 3. and 4. so that you have a total of 4 terminals, connected to keylime1 and 4 connected keylime2. 
     
#### Manual Virualbox Setup with Fedora 30 image
1. Download Fedora 30 image ![link](https://dl.fedoraproject.org/pub/fedora/linux/releases/30/Workstation/x86_64/iso/Fedora-Workstation-Live-x86_64-30-1.2.iso) (if link not work, https://dl.fedoraproject.org/pub/fedora/linux/releases/30/Workstation/x86_64/iso/Fedora-Workstation-Live-x86_64-30-1.2.iso)
2. Create a virtual machine and install Fedora 30. _Fedora requires a minimum of 10GB disk, 1GB RAM, and a 1GHz processor to install and run successfully._
3. Download the keylime bash file which will help you finish the installation. 
```bash
wget https://gist.githubusercontent.com/lukehinds/539daa4374f5cc7939ab34e62be54382/raw/d663744210652d0f4647456e9a3d05033294d91a/keylime.sh
chmod +x keylime.sh
```
4. See if the TPM works
 i. try `tpm_serverd`, if that works, you are free to go
 ii. if you are not try `export TPM2TOOLS_TCTI="tabrmd:bus_name=com.intel.tss2.Tabrmd"`, then tried i. again
 iii. if that still not work, try `systemctl status tpm2-abrmd`
 
4. Clone the our repo, change to branch andrew_multi_verifier
```bash
git clone https://github.com/BU-NU-CLOUD-F19/Keylime-_Enabling_Trust_in_the_Cloud_QEMU-KVM.git
cd Keylime-_Enabling_Trust_in_the_Cloud_QEMU-KVM/
git branch andrew_multi_verifier
```
5. Run the setup file inside the sudo mode
```bash
sudo su
enter your password:
python3 setup.py install
```
6. Start two identical virtual machines with keylime installed. One is the provider and the other one is the tenant. Put these two machines into same network, using VB's NAT networking GUI

7. Remove the original DB file to resolve the incompatibility `rm /var/lib/keylime/cv_data.sqlite`, since the structure of DB has been changed.

8. install merklelib with `pip3 install --user merklelib`

9. Finally for each VM bring up 4 terminals for a total of 8 terminals 

### Demos

DISCLAIMER: The following instuctions will assume two VMs with keylime are already runing

For the Vagrant envrionment setup refer to the VMs as follows:
- **keylime1** -> Provider 
- **keylime2** -> Tenant

For the manual environment setup Provider/Tenant assignment is arbitrary just make sure to keep trck of each respectively 

#### Tenant/Provider Verifier communication pipeline

1. Provision Keylime in the **Provider** first, make sure the following commands run without errors 
      - In the first terminal, run `keylime_verifier`
      - In the second terminal, run `keylime_registrar`
      - In the third terminal, run `keylime_agent`
      - In the fourth terminal, run `keylime_tenant -t 10.0.0.11 -f <user_home>/Keylime-_Enabling_Trust_in_the_Cloud_QEMU-KVM/keylime_master/README.md` 

2. Provision Keylime in the **Tenant** 
      - In the first terminal, run `keylime_verifier`
      - In the second terminal, run `keylime_registrar`
      - In the third terminal, run `keylime_agent`
      - In the fourth terminal, run `keylime_tenant -t 10.0.0.21 -pv 10.0.0.11 -pvp 8991 -npq True -f <user_home>/Keylime-_Enabling_Trust_in_the_Cloud_QEMU-KVM/keylime_master/README.md` 
      
 3.  Wait ~5s (an exaggerated simulation of TPM hardware latency) From the first terminal in the tenant VM, that is the tenant verifier. You can see the provider's quote which the tenant verifier asked, and the result of the validity of the quote.
 
 4. Run `keylime_tenant -t 10.0.0.11 -c delete` in **Provider** terminal to delete Agent 
 
 5. Run `keylime_tenant -t 10.0.0.21 -c delete` in **Tenant** terminal to delete Agent 
 
 6. Run `Ctrl-C` in all other terminals to shut down Keylime

#### Quote Request Nonce batching and redistrobution utilizing a Merkletree structure 
1. Provision Keylime in the **Provider** first, make sure the following commands run without errors 
      - In the first terminal, run `keylime_verifier`
      - In the second terminal, run `keylime_registrar`
      - In the third terminal, run `keylime_agent`
      - In the fourth terminal, run `keylime_tenant -t 10.0.0.11 -f <user_home>/Keylime-_Enabling_Trust_in_the_Cloud_QEMU-KVM/keylime_master/README.md` 

2. In **Tenant** VM execute the following 
      - `./keylime_maste/scripts/verifier_tester.sh`
      - This will concurrenly send 10 GET requests to the provider verifier 

3. Wait ~5s (an exaggerated simulation of TPM hardware latency) and look inside the first terminal, the verifier, you can see nonces are aggregated, and form a merkle tree inside with these nonces.

4. Run `keylime_tenant -t 10.0.0.11 -c delete` in **Provider** terminal to delete Agent 
 
6. Run `Ctrl-C` in all other terminals to shut down Keylime


## Release Planning
- Release 1
  - Complete all research spikes associated with the project components
  - Get Keylime up and running on a Docker container
  - Communicate between a tenant client and the Keylime verifier
- Release 2
  - Plan out all elements that need to be modified and what modifications needed to be made
  - Design a simple Merkle tree
  - Established a simple communication method between two instances of Keylime (agent-agent connection) on a private network
- Release 3
  - Set up components of the KVM system in a VM (via Vagrant) or container (via Docker)
  - Enable nested virtualization by making a nested VM inside the "host" VM
  - Enable tenant verifier to talk to provider verifier
- Release 4
  - Refine verifier-verifier interface
  - Implement Merkle tree data structure into Keylime APIs
  - Blueprint the registration process, share with open source community
  - Debug all edits to the APIs
- Release 5
  - Test bootstrapping process
  - Continue debugging
  - Performance enhancement

## Presentation slides
- Sprint 1: https://docs.google.com/presentation/d/1YRiCh9JLPN-RTcto8vccMqHcnGL8mvYgsJaDZAbDeK8/edit?usp=sharing

- Sprint 2: https://docs.google.com/presentation/d/1LFivYyhJpFX_lmF8cqmzGQFmB9MhNZT_oJUljYssW3Q/edit?usp=sharing

- Sprint 3: https://docs.google.com/presentation/d/1MnS7aXz9ixZjlN98U2TjNehpFPX2v_VejRKxmizOrq4/edit?usp=sharing

- Sprint 4: https://docs.google.com/presentation/d/1f7PKg0XRrGfxl30nEswwOwc1WoNt6B_7EcswfEGwWZM/edit?usp=sharing

- Sprint 5: https://docs.google.com/presentation/d/1UV8ofkxnf9tNP9tAMLAE8R9iZfG0QSWeJ7MyaONYzSg/edit?usp=sharing

## Open Questions & Risks

Questions still needed to be answered:
- Does the MOC provide a TPM for Keylime to utilize?
- Do we need to consider different versions of TPM and which can be supported?
- What happens to the node/resources when the user is done using it? 
- Will we need to emulated TPM for anything?
- How should we unravel the Merkle tree?
- Can one verifier be used for multiple agents/nodes?
- How to register VTPMs on Tenant agent nodes with provider Agent's AIK_pub
- Do we share the Merkle Tree with all instances? 

## References and Resources
- About the project: 
  - https://docs.google.com/document/d/1K-mTbK9LBRvG6KEFH4Ys-Eb1zROZD1neWJRi9C-groo/edit#heading=h.jxvflg4dxu72
  - https://docs.google.com/document/d/1Y-EJXihnJM3puRJQfb1v-4sS7g-mni-AoM5CMNZ0ncc/edit

- About Keylime
  - https://next.redhat.com/2018/09/11/building-trust-in-cloud-computing-with-keylime/
  - https://github.com/keylime/keylime
  - https://keylime-docs.readthedocs.io/en/latest/
  - https://github.com/keylime/keylime/issues/29
  - https://gitter.im/keylime-project/community
  - https://www.ll.mit.edu/sites/default/files/publication/doc/2018-04/2016_12_07_SchearN_ACSAC_FP.pdf

- About vTPM
  - https://arxiv.org/pdf/1905.08493.pdf
  
## 
  
