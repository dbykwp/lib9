
# apt-get install libvirt-bin libvirt-dev qemu-system-x86 qemu-system-common genisoimage -y

apt-get install python3-pip libffi-dev libpython3-dev libssh-dev libsnappy-dev build-essential python3-dev pkg-config libvirt-dev -y
pip3 install -U cryptography
#for development mode
pip3 install -e .
