# Keylime: Enabling Trust in the Cloud - QEMU/KVM

## Project Vision and Goals

The Keylime project is a scalable cloud management system that connects the security features of hardware Trusted Platform Modules to cloud computing.  It allows users to verify that every level of their remote system has not been compromised or tampered with, and continuously measures system integrity by monitoring Infrastructure-as-a-Service (IaaS) nodes.

Keylime: Enabling Trust in the Cloud - QEMU/KVM is an extension of the current implementation of the Keylime project. The high-level goals of this project are as follows:

1. Extend trust from the hardware TPM to the vTPM by chaining trust upwards from the hardware module.
2. Provide bootstrapping and monitoring capabilities in virtualized environments for QEMU/KVM.


## Project Users/Personas
The Keylime extension will be used by cloud service providers, cloud service users, and developers.  It specifically targets open-source cloud users, since QEMU/KVM is the most popular open-source hypervisor. 

The Keylime extension will also be used by the Keylime development community to push the project forward. The community is committed to introducing and integrating new security verification features for cloud computing.

In general, Keylime targets organizations that could benefit from cloud computing, but are reluctant to use it due to security limitations in protecting sensitive data.  These organizations include, but are not limited to, the government, medical organizations, and financial institutions.

The Keylime extension does not target users who have a non-QEMU/KVM hypervisor.


## Project Scope and Features [TODO: In progress]
- Add any functionalities needed for Keylime to support KVM
- Port Xen implementation to QEMU
- Extend trust from hardware TPM to vTPM
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
    
- Problem: vTPM is not isolated hardware, since it is stored on disk, and can be tampered with or spoofed. We need to extend trust from the hardware TPM to vTPM.

![System diagram of Keylime implementation](/assets/images/keylime_diagram.png)

Building on the existing Keylime project, we will continue using the exisiting techonology to extend trust from TPM to vTPM. The key parts of the solution will involve using the Xen Hypervisor to develop vTPM, using DeepQuote instead of quote in the former Keylime.

Each vTPM is a separate Xen VM. Trust of vTPM rooted in hardware of the htpervisor, that the extention of trust from TPM to vTPM. DeepQuote operation is applied to obtain hardware TPM quote from a vTPM. By virtualizing Keylime, Tenant Cloud Verifier can verify many cloud nodes as well as derive a key in less than 2 second, which enable Keylime scale to monitor integrity of thousands of cloud machines.

## Acceptance Criteria

The minimum acceptance criteria for this project is a working Keylime port to QEMU/KVM in Python 3.6.  This includes the ability to verify the trust of a KVM hypervisor, and extending the trust from the hardware TPM to the vTPM running on the QEMU/KVM hypervisor.

The stretch goals of the Keylime extension are to implement the project in RUST, and to work on closing issues in the Keylime GitHub repo.


## Release Planning
- Release 1
  - Complete all research spikes associated with the project components
  - Communicate with TPM hardware
- Release 2
  - Verify trust of a KVM hypervisor
- Release 3
  - Extend trust from one hardware TPM to one QEMU/KVM vTPM
- Release 4
  - Extend trust from one hardware TPM to many QEMU/KVM vTPMs
- Release 5
  - Performance enhancement
  - Port Keylime extension to RUST

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

- About vTPM
  - https://arxiv.org/pdf/1905.08493.pdf
