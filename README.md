# Keylime: Enabling Trust in the Cloud - QEMU/KVM


## Project Background
In cloud computing, users running applications on Infrastructure-as-a-Service (IaaS) nodes can not verify for themselves that the resources they are using are secure. Because of this, they must fully trust the cloud service provider that nothing (from the hypervisors to the OS) has been compromised. This raises a concern, because the user does not know if the resources are controlled by malicious insiders and rogue organizations. 

A Trusted Platform Module (TPM) is a hardware chip with secure key generation and storage functionalities. It contains Platform Configuration Registers (PCRs) that are able to store measurements of system integrity in firmwares, hypervisors, OSes, etc. Through this, it can verify if the system has been altered or tampered with. However, using TPMs is complex, can lead to slower performance, and not compatible with virtualized machines (because it is a physical device).

Keylime is a bootstrapping and integrity management software tool that connects the security features of TPMs to cloud computing.  It allows users to verify that every level of their remote system has not been compromised or tampered with, without having to deal with the drawbacks mentioned before. It also continuously measures system integrity by monitoring the cloud (IaaS) nodes, also known as Keylime agents. 

The Keylime system includes four key executable components: a cloud verifier that periodically checks the integrities of the nodes, a registrar that stores public attestation identity keys (AIKs) of TPMs, an agent node that is able to communicate with the TPM, and the tenant client that a user can use to interact with the three previously mentioned components.

Keylime consists of two main services: **trusted bootstrapping** and **continuous attestation**.
 
 **Trusted Bootstrapping (Making a cryptographic identity for a cloud node)**
 
 ![Trusted Bootstrapping p1](/assets/images/boot_p1.png)

 
  - Tenant generates a new bootstrap key for node being provisioned and splits it into two
  - Tenant keeps one piece for bootstrapping and gives the other piece to the Verifier
  - Tenant interacts with the Agent to demonstrate the intent to provision the node
  - Tenant and Verfier both send separate attestation requests to the Agent, and validate the quote returned using the Registrar
  
   ![Trusted Bootstrapping p2](/assets/images/boot_p2.png)
  
  - When either one of them receive a valid attestation result, they send their piece of the bootstrap key to the node being provisioned
  - Once both parts of the key are sent to the node, the Agent can recombine and decrypt the node’s configuration data including private keys sent to the node via configuration service

**Continuous Attestation (Continuously monitoring the identity to see if the node has been tampered with)**

 ![System diagram of Keylime implementation](/assets/images/attest_succ.png)
 
  - the verifier continuously requests quotes (sets of measurements for system integrity) from the agent
  - each request induces agent to retrieve a quote from that nodes TPM (or vTPM) 
  - that quote is returned to verifier, which cryptographically verifies if the quote is valid
  - if invalid - denoting system state of the reporting node has somehow changed - the verifier issues a revocation notice to the CA
  - Once CA receives revocation notice, it should invalidate the affected nodes’ keys, effectively breaking all crypto related network connections and services for the node 

Please note that the diagrams and procedures mentioned above are for the Xen implementation.

## Project Vision and Goals

Keylime: Enabling Trust in the Cloud - QEMU/KVM is an extension of the current implementation of the Keylime project. Because the Xen and KVM hypervisors differ in capabilities (such as a virtual TPM), a new Keylime system structure is blueprinted specifically for KVM (see in solution concept). We will aim to develop missing features that are needed for the bootstrapping capabilities of the Keylime-KVM port. The high-level goals of this project are as follows:

1. Instantiate each component of Keylime (for KVM)  in a VM or container
2. Investigate (and implement) a registration process for KVM
3. Create a Merkle tree implementation that will be used by the cloud verifier to handle many quote requests
4. Create an interface for the tenant verifier to communicate with the cloud verifier
5. Create an interface layer to abstract from the Merkle Tree layer

These goals will be explained in the solution concept.

## Project Users/Personas
The Keylime extension will be used by cloud service providers, cloud service users, and developers.  It specifically targets open-source cloud users, since QEMU/KVM is the most popular open-source hypervisor. 

Ideally, cloud service providers will run Keylime on their servers.  This would include having a Keylime verifier and registrar to monitor system integrity in addition to any other nodes. However, this still restricts integrity verification to cloud providers.  Keylime is mainly intended to benefit cloud service users. In the KVM implementation, both the user and service provider will run their own Keylime implementations and communicate with each other in a verifiable way to establish trust. This way, instead of just trusting the "all clear" message from cloud providers, users can see for themselves that the nodes they are using have not been compromised.

The Keylime extension will also be used by the Keylime development community to push the project forward. The community is committed to introducing and integrating new security verification features for cloud computing.

In general, Keylime targets organizations that could benefit from cloud computing, but are reluctant to use it due to security limitations in protecting sensitive data.  These organizations include, but are not limited to, the government, medical organizations, and financial institutions.

The Keylime extension does not target users who have a non-QEMU/KVM hypervisor.

## Project Scope and Features

What is in scope of the project:
- Add any functionalities needed for Keylime to support vTPM in KVM
- Get all currently implemented system components up and running in a VM for developing
- Investigate ways to implement the registration process
- Implement and store Merkle trees in the Keylime system as a way to handle multiple quote requests to the TPM via cloud verifier
- Add changes or additions to Keylime codebase (libraries) for KVM support

What is NOT in scope of the project:
- Design and implement a virtual TPM from scratch
- Communicate between the hardware TPM directly from the virtual TPM via deepquote function (possible in the Xen version of Keylime)
- Improve features of the Xen implementation

## Solution Concept
The main high-level system components of the Keylime extension are Keylime itself, the QEMU/KVM hypervisor (including the virtual TPM), and the Trusted Platform Module (TPM): Version 2.0.

- System components
  - QEMU/KVM hypervisor
  - Hardware TPM
  - Libvert library
  - Emulated/virtual TPM
  - Keylime used by the user/tenant
    - Tenant Cloud Verifier
    - Tenant Registrar
    - Keylime agent (in the VM/resource)
  - Keylime used by the cloud provider
    - Provider Registrar
    - Provider Cloud Verifier
    - Keylime agent (outside the VM/resource, used by the cloud provider)
  
  
**Desired architecture**
 
![System diagram of Keylime implementation](/assets/images/keylime_scope.jpg)

Instead of having the vTPM directly communicate with the TPM, as was done in the XEN implementation of Keylime, we will rather have the Cloud Provider deploy a second instance of Keylime on it's physical hardware and have the provider's Keylime components interact with the tenant's Keylime components. 

![System diagram of Merkle Tree implementation](/assets/images/merkel_tree.jpg)

Instead of deepquote we will create a Merkle Tree of the hashes of the nonces.

The key parts of the solution will involve using the QEMU/KVM Hypervisor to develop vTPM. We will also need to write an interface for the provider verifier to send the current root to the provider agent and the agent the result quote back. We need to still decide whether the Merkle Tree will live on the provider agent or provider verifier. We need to write interface endpoints for the tenant verifier to communicate with the provider verifier to request quotes synchronously, and an interface layer to abstract from the Merkle Tree. We still need to figure out registration for the provider agent to provider provider registrar, and how secure we can make that.

## Acceptance Criteria

The minimum acceptance criteria for this project is a working Keylime port to QEMU/KVM in Python 3.6. What makes the Keylime port functional at a minimum is the ability to bootstrap and establish trust cryptographically between the user and cloud node via communications with the hardware TPM.

The stretch goals of the Keylime extension are to implement the project in RUST, and to work on closing issues in the Keylime GitHub repo.


## Release Planning
- Release 1
  - Complete all research spikes associated with the project components
  - Get Keylime up and running on a Docker container
  - Communicate with TPM hardware
- Release 2
  - Plan out all elements that need to be modified and what modifications needed to be made
  - Set up a KVM hypervisor and verify trust from it
  - Set up components of the KVM system in a VM (via Vagrant) or container (via Docker)
- Release 3
  - Communicate with the software TPM (vTPM) on a QEMU/KVM hypervisor 
- Release 4
  - Extend trust from one hardware TPM to one QEMU/KVM vTPM
- Release 5
  - Extend trust from one hardware TPM to many QEMU/KVM vTPMs
  - Performance enhancement
  - Port Keylime extension to RUST

## Presentation slides
- Sprint 1: https://docs.google.com/presentation/d/1YRiCh9JLPN-RTcto8vccMqHcnGL8mvYgsJaDZAbDeK8/edit?usp=sharing

- Sprint 2: https://docs.google.com/presentation/d/1LFivYyhJpFX_lmF8cqmzGQFmB9MhNZT_oJUljYssW3Q/edit?usp=sharing

## Open Questions & Risks

Problems considered:
- vTPM is not isolated hardware, since it is stored on disk, and can be tampered with or spoofed. We need to extend trust from the hardware TPM to vTPM. 
- TPM V2.0 is not backward compatible with previous TPM. Since Keylime is developed based on former version(V1.2), it also need to be upgraded to be compatible with TPM V2.0.
- Current implementation of Keylime is written in Python but want to port to a Rust, a more secure language.

Questions still needed to be answered:
- Does the MOC provide a TPM for Keylime to utilize?
- Which functions/code do we need to focus on editing?
- What versions of TPM are supported by which hypervisors?
- What are the implementation differences (in code) in TPM1.2 and TPM2.0?
- What would be considered beyond the scope of this project?
- What happens to the node/resources when the user is done using it? 

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
