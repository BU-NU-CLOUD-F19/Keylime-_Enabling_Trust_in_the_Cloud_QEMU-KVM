#!/bin/bash


WORK_DIR=$(pwd)
KEYLIME_HOME="${WORK_DIR}/keylime"
SWTPM_HOME="${WORK_DIR}/swtpm"

if [ "$EUID" -ne 0 ] 
  then echo "Please run as root"
  exit
fi

SELINUXSTATUS=$(getenforce);

if [ "$SELINUXSTATUS" == "Enforcing" ]; then
    echo "Disabling SeLinux";
    sed -i s/^SELINUX=.*$/SELINUX=disabled/ /etc/selinux/config
    setenforce 0
    REBOOT=true
fi;

echo -e "Setting up copr repository"

dnf copr enable lhinds/Keylime 

echo -e "Updating packages"

yum update -y

echo -e "Install dependencies"

yum -y install git \
           bzip2-devel \
           dbus-devel \
           openssl-devel \
           procps \
           libtool \
           gcc \
           make \
           automake \
           m2crypto \
           redhat-rpm-config \
           libselinux-python \
           gnulib \
           glib2-devel \
           glib2-static \
           uthash-devel \
           wget \
           which \
           zeromq-devel \
           shtool \
           yum-utils


echo -e "Installing Emulator and Keylime source"

mkdir ${SWTPM_HOME}
cd ${SWTPM_HOME}
wget --content-disposition http://sourceforge.net/projects/ibmswtpm2/files/ibmtpm1119.tar.gz/download
tar -zxvf ibmtpm1119.tar.gz
cd ${SWTPM_HOME}/src
make
install -c tpm_server /usr/local/bin/tpm_server

echo -e "Install Keylime"

dnf install keylime -y 
sed -i 's/.*require_ek_cert.*/require_ek_cert = False' /etc/keylime.conf


echo -e "Grab some keylime scripts needed"
cd ${WORK_DIR}
git clone https://github.com/keylime/keylime ${KEYLIME_HOME}
cd ${KEYLIME_HOME}/swtpm2_scripts
chmod +x ${KEYLIME_HOME}/swtpm2_scripts/init_tpm_server
chmod +x ${KEYLIME_HOME}/swtpm2_scripts/tpm_serverd
install -c ${KEYLIME_HOME}/swtpm2_scripts/init_tpm_server /usr/local/bin/init_tpm_server
install -c ${KEYLIME_HOME}/swtpm2_scripts/tpm_serverd /usr/local/bin/tpm_serverd


echo -e "Start tpm and Configure tpm2-abrmd systemd"
export TPM2TOOLS_TCTI="tabrmd:bus_name=com.intel.tss2.Tabrmd"
pkill -HUP dbus-daemon
/usr/local/bin/tpm_serverd
sed -i 's/.*ExecStart.*/ExecStart=\/usr\/sbin\/tpm2-abrmd --tcti=mssim/' /usr/lib/systemd/system/tpm2-abrmd.service
systemctl daemon-reload
systemctl enable tpm2-abrmd
systemctl start tpm2-abrmd


# System requirs reboot?
if [ "$REBOOT" = true ] ; then
    echo -e 'Please reboot machine to make SElinux changes permanent'
    echo -e 'And then run'
    echo -e 'tpm_serverd'
    echo -e 'systemctl restart tpm2-abrmd'
fi