# Keylime: Enabling Trust in the Cloud - QEMU/KVM


## Project Background
In cloud computing, users running applications on Infrastructure-as-a-Service (IaaS) nodes can not verify for themselves that the resources they are using are secure. Because of this, they must fully trust the cloud service provider that nothing (from the hypervisors to the OS) has been compromised. This raises a concern, because the user does not know if the resources are controlled by malicious insiders and rogue organizations. 

A Trusted Platform Module (TPM) is a hardware chip with secure key generation and storage functionalities. It contains Platform Configuration Registers (PCRs) that are able to store measurements of system integrity in firmwares, hypervisors, OSes, etc. Through this, it can verify if the system has been altered or tampered with. However, using TPMs is complex, can lead to slower performance, and not compatible with virtualized machines (because it is a physical device).

Keylime is a bootstrapping and integrity management software tool that connects the security features of TPMs to cloud computing.  It allows users to verify that every level of their remote system has not been compromised or tampered with, without having to deal with the drawbacks mentioned before. It also continuously measures system integrity by monitoring the cloud (IaaS) nodes, also known as Keylime agents.

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

## Project Vision and Goals

Keylime: Enabling Trust in the Cloud - QEMU/KVM is an extension of the current implementation of the Keylime project. The high-level goals of this project are as follows:

1. Extend trust from the hardware TPM to the vTPM by chaining trust upwards from the hardware module.
2. Provide bootstrapping and monitoring capabilities in virtualized environments for QEMU/KVM hypervisor.


## Project Users/Personas
The Keylime extension will be used by cloud service providers, cloud service users, and developers.  It specifically targets open-source cloud users, since QEMU/KVM is the most popular open-source hypervisor. 

Ideally, cloud service providers will run Keylime on their servers.  This would include having a Keylime verifier and registrar to monitor system integrity in addition to any other nodes. However, this still restricts integrity verification to cloud providers.  Keylime is mainly intended to be run by cloud service users.  This way, instead of just trusting the "all clear" message from cloud providers, users can see for themselves that the nodes they are using have not been compromised.

The Keylime extension will also be used by the Keylime development community to push the project forward. The community is committed to introducing and integrating new security verification features for cloud computing.

In general, Keylime targets organizations that could benefit from cloud computing, but are reluctant to use it due to security limitations in protecting sensitive data.  These organizations include, but are not limited to, the government, medical organizations, and financial institutions.

The Keylime extension does not target users who have a non-QEMU/KVM hypervisor.


## Project Scope and Features

- Add any functionalities needed for Keylime to support vTPM in KVM
- Port Xen implementation to QEMU
- Extend trust from hardware TPM to vTPM through a function called "deepquote"
  - Get backend code to recognize a special deepquote request
  - Port deepquote functionality to vTPM
  - Integrate TPM 2.0 functionality with Keylime
- Add changes or additions to Keylime codebase (libraries) for KVM support

![System diagram of Keylime implementation](/assets/images/solution_diagram.png)


## Solution Concept [TODO: In progress]
The main high-level system components of the Keylime extension are Keylime itself, the QEMU/KVM hypervisor (including the virtual TPM), and the Trusted Platform Module (TPM): Version 2.0.

- System components
  - QEMU/KVM hypervisor
  - Trusted Platform Module (TPM): Version 2.0
  - Keylime
    - Tenant Cloud Verifier
    - Tenant Registrar
    - Provider Registrar
  


**Problem:** 
  - vTPM is not isolated hardware, since it is stored on disk, and can be tampered with or spoofed. We need to extend trust from the hardware TPM to vTPM. 
  - TPM V2.0 is not backward compatible with previous TPM. Since Keylime is developed based on former version(V1.2), it also need to be upgraded to be compatible with TPM V2.0.
  - Current implementation of Keylime is written in Python but want to port to a Rust, a more secure language.
  
**Desired architecture**
 
![System diagram of Keylime implementation](/assets/images/keylime_diagram.png)

Building on the existing Keylime project, we will continue using the exisiting techonology to extend trust from TPM to vTPM. The key parts of the solution will involve using the QEMU/KVM Hypervisor to develop vTPM, using DeepQuote instead of quote in the former Keylime.

Each vTPM is a separate VM. Trust of vTPM rooted in hardware of the htpervisor, that the extention of trust from TPM to vTPM. DeepQuote operation is applied to obtain hardware TPM quote from a vTPM. By virtualizing Keylime, Tenant Cloud Verifier can verify many cloud nodes as well as derive a key in less period, which enable Keylime scale to monitor integrity of thousands of cloud machines.

## Acceptance Criteria

The minimum acceptance criteria for this project is a working Keylime port to QEMU/KVM in Python 3.6.  This includes the ability to verify the trust of a KVM hypervisor, and extending the trust from the hardware TPM to the vTPM running on the QEMU/KVM hypervisor.

The stretch goals of the Keylime extension are to implement the project in RUST, and to work on closing issues in the Keylime GitHub repo.


## Release Planning
- Release 1
  - Complete all research spikes associated with the project components
  - Get Keylime up and running on a Docker container
  - Communicate with TPM hardware
- Release 2
  - Plan out all elements that need to be modified and what modifications needed to be made
  - Verify trust of a KVM hypervisor
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

## Open Questions & Risks
- Does the MOC provide a TPM for Keylime to utilize?
- Which functions/code do we need to focus on editing?
- What versions of TPM are supported by which hypervisors?
- Does the vTPM already exist on a QEMU/KVM hypervisor?
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
