# IMPORTANT
This repository is still in progress on importing to GitHub and refining to remove all hardcoded entries to make it environment-agnostic.
Using this repository requires ZFS to be installed due to the way the program is developed

# pycloudplatform
Simple libvirt web frontend for deploying VMs
Code is tested to be working on Python 3.7 and Ubuntu 18.04. More OS support is planned for future expansion

## What is this project?
It is part of my final year project to develop a web-based virtual machine management that interacts with [libvirt](http://libvirt.org/) library.

## How to run it? 
- Install Python >=3.7
- Make sure ZFS is installed and `<pool>/kvm-images` dataset exist
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

## Implementation state: INCOMPLETE
### Implemented features
- Creating virtual machines (from template/snapshot only)
- Starting virtual machines
- Power off virtual machines
- Shut down virtual machines
- Snapshot virtual machines (through ZFS snapshot and requires VM to be powered off

### Upcoming features
- [Cloud-Init](https://cloud-init.io/) support 
- Hot-add and hot-remove vCPU and RAM
- Live resize virtual disks (only upsizing, downsizing is tricky to set up)

### Missing features
- Custom virtual machine creation (requires user to manually deploy VMs
- libvirt-based VM snapshot
- Tons of things I can't think of right now

## License
MIT
