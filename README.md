# IMPORTANT
This repository is still in progress on importing to GitHub and refining to remove all hardcoded entries to make it environment-agnostic.
Using this repository requires ZFS to be installed due to the way the program is developed.

# pycloudplatform
Simple libvirt web frontend for deploying VMs.
Code is tested to be working on Python 3.7, libvirt 4.0, ZFS 0.7.9 and Ubuntu 18.04. More OS support is planned for future expansion.

## What is this project?
It is part of my final year project to develop a web-based virtual machine management that interacts with [libvirt](http://libvirt.org/) library.

## But why? There's so many alternatives like VMware ESXi/Proxmox/VirtualBox/VMware Workstation/Virtual Machine Manager/\<insert your hypervisor here\>
- It is for my final year project (I don't have any extra ideas I can do lol)
- I love using libvirt and KVM, but command line is a bit eh...
- Most hypervisors require you to have a desktop environments (except VMware ESXi)
- `virsh` is good, but then, command line (read point 2)
- I need a project that I really need to make it work (too many dead projects that never seen the light)

## How to run it? 
- Install Python >=3.7
- Make sure ZFS is installed and `zfs-pool-ubuntu/kvm-images` dataset exist
- `sudo apt install libvirt-bin virtinst bridge-utils libosinfo-bin libguestfs-tools virt-top python3.7-dev libvirt-dev`
- git clone this project
- cd into the folder
- create a virtualenv with Python 3.7 version
- `pip install -r requirements.txt`
- set up MySQL server, create necessary users, database (name of database has to be `pycloudplatform` and allow full permissions for the user to that database
- copy `instance/config.example.py` to `instance/config.py` and modify based on the instructions given in the file
- `flask db init`
- `flask db migrate`
- `flask db upgrade`
- `export FLASK_CONFIG=development`
- `python run.py`

## Implementation state
### Implemented features
- Creating virtual machines (from template/snapshot only)
- Starting virtual machines
- Power off virtual machines
- Shut down virtual machines
- Snapshot virtual machines (through ZFS snapshot and requires VM to be powered off)

### Planned features
- [Cloud-Init](https://cloud-init.io/) support 
- Hot-add and hot-remove vCPU and RAM
- Live resize virtual disks (only upsizing, downsizing is tricky to set up)
- Add in additional storage methods (rather than being hard-coded to ZFS only)
- Add more hypervisor support

### Missing features
- Custom virtual machine creation (requires user to manually deploy VMs)
- libvirt-based VM snapshot
- Tons of things I can't think of right now

## TODO
- Unspaghetti the code (it's really bad)
- Remove all hard-coding especially on the storage side
- Improve code naming and organization
- DOCUMENTATION
- Refactor the code to assume standard storage (ext4-based virtual disks)
- <insert yet to be seen features that I can't think of>

## Known issues
- Installation steps are incomplete. This will be fixed after most of the hardcoding has been eliminated
- VM operations has a significant delay because all operations are synchronous

## License
MIT
