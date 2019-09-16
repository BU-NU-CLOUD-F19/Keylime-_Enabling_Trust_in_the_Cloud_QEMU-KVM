# Keylime: Enabling Trust in the Cloud - QEMU/KVM

## Vision and goals of the project

Keylime: Enabling Trust in the Cloud - QEMU/KVM is an extension of the current implementation of the Keylime project. The high-level goals of this project are as follows:

1. Extend trust from the hardware TPM to the vTPM by chaining trust upwards from the hardware module.
2. Provide bootstrapping and monitoring capabilities in virtualized environments for QEMU/KVM.


## Users/personas of the project
The Keylime extension  will be used by cloud service providers, cloud service users, and developers.  It specifically targets open-source cloud users, since QEMU/KVM is the most popular open-source hypervisor. 

The Keylime extension will also be used by the Keylime development community to push the project forward. The community is committed to introducing and integrating new security verification features for cloud computing.

In general, Keylime targets organizations that could benefit from cloud computing, but are reluctant to use it due to security limitations in protecting sensitive data.  These organizations include, but are not limited to, the government, medical organizations, and financial institutions.


## Scope and features of the project [TODO: In progress]
- Add any functionalities needed for Keylime to support KVM
- Port Xen implementation to QEMU
- Extend trust from hardware TPM to virtual TPM
- Add changes or additions to Keylime codebase (libraries) for KVM support

![System diagram of Keylime implementation](/assets/images/solution_diagram.png)


## Solution concept [TODO: In progress]
The main system components of the Keylime extension are Keylime itself, the QEMU/KVM hypervisor (including the virtual TPM), and the Trusted Platform Module (TPM): Version 2.0.
- System components
  - QEMU/KVM hypervisor
  - Trusted Platform Module (TPM): Version 2.0
  - Keylime
- Problem: vTPM is not isolated hardware, can be tampered with or spoofed. So we need to extend trust from hardware TPM to vTPM.

![System diagram of Keylime implementation](/assets/images/keylime_diagram.png)


## Acceptance criteria

The minimum acceptance criteria for this project is a working Keylime port to QEMU/KVM in Python 3.6.  This includes the ability to verify the trust of a KVM hypervisor, and extending the trust from the hardware TPM to the vTPM running on the QEMU/KVM hypervisor.

The stretch goals of the Keylime extension are to implement the project in RUST, and to work on closing issues in the Keylime GitHub repo.


## Release planning
- Release 1
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
- About project: 
  - https://docs.google.com/document/d/1K-mTbK9LBRvG6KEFH4Ys-Eb1zROZD1neWJRi9C-groo/edit#heading=h.jxvflg4dxu72
  - https://docs.google.com/document/d/1Y-EJXihnJM3puRJQfb1v-4sS7g-mni-AoM5CMNZ0ncc/edit
- Example project description: 
  - https://github.com/BU-NU-CLOUD-SP18/sample-project/blob/master/MOC-UI-ProjectProposalExample.md

- About Keylime
  - https://next.redhat.com/2018/09/11/building-trust-in-cloud-computing-with-keylime/
  - https://github.com/keylime/keylime
  - https://keylime-docs.readthedocs.io/en/latest/
  - https://github.com/keylime/keylime/issues/29
  - https://gitter.im/keylime-project/community

- About vTPM
  - https://arxiv.org/pdf/1905.08493.pdf
