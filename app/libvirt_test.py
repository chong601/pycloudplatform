import libvirt
import subprocess
import operator
from ..config import Config

LIBVIRT_URI="qemu:///system"

class libvirt_test:
    domain_state={0:"No State",1:"Running",2:"Blocked",3:"Paused",4:'Shutting Down',5:"Powered Off",6:"Crashed",7:"Suspended",8:"LAST"}
    def __init__(self):
        """Initialize libvirt_test"""
        pass
        #self.conn=libvirt.open(LIBVIRT_URI)
        #if self.conn==None:
        #    return False, "Error connecting to libvirt"

    # use regex .*@(.*)
    def internal_list_snapshots(self,domain_name):
        pass

    def internal_set_up(self):
        """Set up libvirt connection"""
        self.conn=libvirt.open(LIBVIRT_URI)
        #if self.conn==None:
        #    return False, "Error connecting to libvirt"
    
    def internal_close_connection(self):
        """Tear down libvirt connection"""
        self.conn.close()
    
    def api_list_domains(self):
        vm_name_list=[]
        try:
            self.internal_set_up()
            domainIDs = self.conn.listAllDomains()
            if domainIDs==None:
                result=False, "Failed to get a list of domain IDs"
            if len(domainIDs)==0:
                result=True, "No domains"
            else:
                for domainID in domainIDs:
                    templist=[]
                    templist.append(domainID.name())
                    domaininfo=domainID.info()
                    for n in range(0,len(domainID.info())):
                        if n==0:
                            templist.append(self.domain_state.get(domaininfo[n],None))
                        if n==2:
                            templist.append(str(int(domaininfo[n]/1024)))
                        if n==3:
                            templist.append(domaininfo[n])
                    templist.append(domainID.UUIDString())
                    templist.append(domaininfo[0])
                    vm_name_list.append(templist)
                vm_name_list=sorted(vm_name_list,key=operator.itemgetter(0))
                result=True, vm_name_list
            self.internal_close_connection()
        except libvirt.libvirtError as error:
            print(error)
        finally:
            return result

    def api_set_vm_vcpu_count(self,uuid,vcpu_count):
        try:
            self.internal_set_up()
            dom=self.conn.lookupByUUIDString(uuid)
            dom.setVcpusFlags(vcpu_count)
            print('The vCPU for domain with of UUID '+uuid+' has changed to '+str(vcpu_count))
            result=True, uuid
        except libvirt.libvirtError:
            result=False, "VM "+dom.name()+" vCPU setup failed"
        finally:
            self.internal_close_connection()
        return result

    def api_set_vm_ramsize_count(self,uuid,ram_mb):
        try:
            self.internal_set_up()
            dom=self.conn.lookupByUUIDString(uuid)
            dom.setMemoryFlags(ram_mb*1024)
            print('The memory for domain with of UUID '+uuid+' has changed to '+str(ram_mb)+" MB")
            result=True, uuid
        except libvirt.libvirtError:
            result=False, "VM "+dom.name()+" memory setup failed"
        finally:
            self.internal_close_connection()
        return result

    def api_get_domain_detail(self, uuid):
        try:
            self.internal_set_up()
            dom=self.conn.lookupByUUIDString(uuid)
            templist=[]
            templist.append(dom.name())
            domaininfo=dom.info()
            for n in range(0,len(domaininfo)):
                if n==0:
                    templist.append(self.domain_state.get(domaininfo[n],None))
                if n==2:
                    templist.append(int(domaininfo[n]/1024))
                if n==3:
                    templist.append(domaininfo[n])
            templist.append(dom.UUIDString())
            templist.append(domaininfo[0])
            print(templist)
            return True, templist
        except libvirt.libvirtError:
            result=False, "Domain with UUID "+uuid+" is not found"
        finally:
            self.internal_close_connection()
        return result
        
        return True, templist
    def api_get_uuid(self, domain_name):
        try:
            self.internal_set_up()
            dom=self.conn.lookupByName(domain_name)
            uuid=dom.UUIDString()
            print('The UUID of domain '+domain_name+' is '+uuid)
            result=True, uuid
        except libvirt.libvirtError:
            result=False, "VM "+domain_name+" is not found"
        finally:
            self.internal_close_connection()
        return result

    def api_get_domain_name(self, uuid):
        try:
            self.internal_set_up()
            dom=self.conn.lookupByUUIDString(uuid)
            vm_name=dom.name()
            print('The name of domain with UUID '+uuid+' is '+vm_name)
            return True, vm_name
        except libvirt.libvirtError:
            return False, "VM with UUID"+uuid+" is not found"
        finally:
            self.internal_close_connection()
        return None, "Internal Error"
        """result=None
        try:
            self.internal_set_up()
            dom=self.conn.lookupByName(domain_name)
            if dom==None:
                result=False, "Domain name "+domain_name+" is not found"
            uuid=dom.UUIDString()
            print('The UUID of domain '+domain_name+' is '+uuid)
            result=True, uuid
            self.internal_close_connection()
        except libvirt.libvirtError:
            pass
        finally:
            return result"""

    #start
    def api_start_vm_name(self, domain_name):
        result=None
        try:
            self.internal_set_up()
            dom=self.conn.lookupByName(domain_name)
            try:
                dom.create()
                result=True, dom.name()
            except libvirt.libvirtError:
                result=False, "VM "+dom.name()+" is already started"
        except libvirt.libvirtError:
            result=False, "VM "+domain_name+" is not found"
        finally:
            self.internal_close_connection()
        return result
        
    #stop
    def api_shutdown_vm_name(self, domain_name):
        try:
            self.internal_set_up()
            dom=self.conn.lookupByName(domain_name)
            try:
                dom.shutdown()
                result=True, dom.name()
            except libvirt.libvirtError:
                result=False, "VM "+dom.name()+" is already shut down"
        except libvirt.libvirtError:
            result=False, "VM "+domain_name+" is not found"
        finally:
            self.internal_close_connection()
        return result

    #destroy
    def api_destroy_vm_name(self, domain_name):
        try:
            self.internal_set_up()
            dom=self.conn.lookupByName(domain_name)
            try:
                dom.destroy()
                result=True, dom.name()
            except libvirt.libvirtError:
                result=False, "VM "+dom.name()+" is already destroyed"
        except libvirt.libvirtError:
            result=False, "VM "+domain_name+" is not found"
        finally:
            self.internal_close_connection()
        return result
    
    #start
    def cmd_start_vm_name(self, domain_name):
        result=None
        try:
            self.internal_set_up()
            dom=self.conn.lookupByName(domain_name)
            process_result=subprocess.run(['virsh','start',domain_name],capture_output=True,universal_newlines=True)
            returncode=process_result.returncode
            if returncode==0:
                result=True, dom.name()
            else:
                result=False, "VM "+dom.name()+" is already started"    
        except libvirt.libvirtError:
            result=False, "VM "+domain_name+" is not found"
        finally:
            self.internal_close_connection()
        return result
        
    #stop
    def cmd_shutdown_vm_name(self, domain_name):
        try:
            self.internal_set_up()
            dom=self.conn.lookupByName(domain_name)
            try:
                dom.shutdown()
                result=True, dom.name()
            except libvirt.libvirtError:
                result=False, "VM "+dom.name()+" is already shut down"
        except libvirt.libvirtError:
            result=False, "VM "+domain_name+" is not found"
        finally:
            self.internal_close_connection()
        return result

    #destroy
    def cmd_destroy_vm_name(self, domain_name):
        try:
            self.internal_set_up()
            dom=self.conn.lookupByName(domain_name)
            try:
                dom.destroy()
                result=True, dom.name()
            except libvirt.libvirtError:
                result=False, "VM "+dom.name()+" is already destroyed"
        except libvirt.libvirtError:
            result=False, "VM "+domain_name+" is not found"
        finally:
            self.internal_close_connection()
        return result

    #start
    def api_start_vm_uuid(self, uuid):
        result=None
        try:
            self.internal_set_up()
            dom=self.conn.lookupByUUIDString(uuid)
            try:
                dom.create()
                result=True, dom.UUIDString()
            except libvirt.libvirtError:
                result=False, "VM "+dom.name()+" is already started"
        except libvirt.libvirtError:
            result=False, "VM is not found"
        finally:
            self.internal_close_connection()
        return result
        
        
    #stop
    def api_shutdown_vm_uuid(self, uuid):
        try:
            self.internal_set_up()
            dom=self.conn.lookupByUUIDString(uuid)
            try:
                dom.shutdown()
                result=True, dom.UUIDString()
            except libvirt.libvirtError:
                result=False, "VM "+dom.name()+" is already shut down"
        except libvirt.libvirtError:
            result=False, "VM is not found"
        finally:
            self.internal_close_connection()
        return result

    #destroy
    def api_destroy_vm_uuid(self, uuid):
        try:
            self.internal_set_up()
            dom=self.conn.lookupByUUIDString(uuid)
            try:
                dom.destroy()
                result=True, dom.UUIDString()
            except libvirt.libvirtError:
                result=False, "VM "+dom.name()+" is already destroyed"
        except libvirt.libvirtError:
            result=False, "VM is not found"
        finally:
            self.internal_close_connection()
        return result
        

    #create
    def cmd_create_vm(self, domain_name, snapshot_name, new_domain_name):
        #zfs_vm_dataset='zfs-pool-libvirt-fyp/kvm-images/'
        # Fun trick to coax Python to generate trailing slashes, needed to 
        # provide a valid name for ZFS datasets
        zfs_vm_dataset='/'.join([Config.ZFS_POOL, Config.ZFS_DATASET, ''])
        # Same as above, but this one forces a / in the beginning to generate
        # a valid path for virt-clone
        mountpoint_vm_dataset='/'.join([Config.ZFS_MOUNTPOINT, '')
        #sourcename=domain_name+'@'+snapshot_name
        sourcename='@'.join([domain_name, snapshot_name])
        sourcedataset=zfs_vm_dataset+sourcename
        destdataset=zfs_vm_dataset+new_domain_name
        destmountpoint=mountpoint_vm_dataset+new_domain_name+'/'
        destdisk=destmountpoint+'disk1.img'
        print("ZFS VM dataset is {}".format(zfs_vm_dataset))
        print("VM mountpoint is {}".format(mountpoint_vm_dataset))
        print("Source VM dataset is {}".format(sourcedataset))
        print("Destination VM dataset is {}".format(destdataset))
        print("Destination mountpoint is {}".format(destmountpoint))
        print("Destination disk is located at {}".format(destdisk))
        
        zfs_clone_result=subprocess.run(['sudo', 'zfs', 'clone', sourcedataset, destdataset],capture_output=True,universal_newlines=True)
        zfs_clone_output=str(zfs_clone_result.returncode)+', '+zfs_clone_result.stdout+', '+zfs_clone_result.stderr
        print(zfs_clone_output)
        if zfs_clone_result.returncode != 0:
            return False, "The dataset already exists!"
        virt_clone_result=subprocess.run(['virt-clone', '-o', domain_name, '-n', new_domain_name, '--file', destdisk, '--preserve-data', '--check', 'all=off'],capture_output=True,universal_newlines=True)
        virt_clone_output=str(virt_clone_result.returncode)+', '+virt_clone_result.stdout+', '+virt_clone_result.stderr
        print(virt_clone_output)
        if virt_clone_result.returncode != 0:
            return False, "VM "+new_domain_name+" already exists!"
        #print(virt_clone_output)
        return True, "VM {} successfully created.".format(new_domain_name)

    #delete
    #VM is considered to be free of clones if it reaches here, template checking should be done on the model side before this command is called
    def api_delete_vm(self, uuid):
        try:
            self.internal_set_up()
            dom=self.conn.lookupByUUIDString(uuid)
            if dom.state()[0] != 5:
                return False, "VM "+dom.name()+" is not powered off!"
            dom.undefine()
            #zfs_vm_dataset='zfs-pool-libvirt-fyp/kvm-images/'
            zfs_vm_dataset='/'.join([Config.ZFS_POOL, Config.ZFS_DATASET, ''])
            targetdataset=zfs_vm_dataset+dom.name()
            zfs_destroy_result=subprocess.run(['sudo', 'zfs', 'destroy', '-r', targetdataset],capture_output=True,universal_newlines=True)
            zfs_destroy_output=str(zfs_destroy_result.returncode)+', '+zfs_destroy_result.stdout+', '+zfs_destroy_result.stderr
            print(zfs_destroy_output)
            if zfs_destroy_result.returncode != 0:
                return False, "The dataset is already deleted"
            #sudo zfs destroy zfs-pool-libvirt-fyp/kvm-images/vm-ubuntu-bionic-test-clone-libvirt-test-api
            result=True, dom.UUIDString()
        except libvirt.libvirtError:
            result=False, "VM is not found"
        finally:
            self.internal_close_connection()
        return result
        
    #clone
    #requires vm name, not uuid
    #NOTE: requires validation on the model side to make sure the template exists
    def cmd_clone_vm(self, domain_name, snapshot_name, new_domain_name):
        """NOT FINAL"""
        #zfs_vm_dataset='zfs-pool-libvirt-fyp/kvm-images/'
        zfs_vm_dataset='/'.join([Config.ZFS_POOL, Config.ZFS_DATASET, ''])
        #mountpoint_vm_dataset='/kvm-images/'
        mountpoint_vm_dataset='/'.join([Config.ZFS_MOUNTPOINT, '')
        #sourcename=domain_name+'@'+snapshot_name
        sourcename='@'.join([domain_name, snapshot_name])
        sourcedataset=zfs_vm_dataset+sourcename
        destdataset=zfs_vm_dataset+new_domain_name
        #destmountpoint='/kvm-images/'+new_domain_name+'/'
        destmountpoint=mountpoint_vm_dataset+new_domain_name+'/'
        destdisk=destmountpoint+'disk1.img'
        print("ZFS VM dataset is {}".format(zfs_vm_dataset))
        print("VM mountpoint is {}".format(mountpoint_vm_dataset))
        print("Source VM dataset is {}".format(sourcedataset))
        print("Destination VM dataset is {}".format(destdataset))
        print("Destination mountpoint is {}".format(destmountpoint))
        print("Destination disk is located at {}".format(destdisk))
        
        zfs_clone_result=subprocess.run(['sudo', 'zfs', 'clone', sourcedataset, destdataset],capture_output=True,universal_newlines=True)
        zfs_clone_output=str(zfs_clone_result.returncode)+', '+zfs_clone_result.stdout+', '+zfs_clone_result.stderr
        print(zfs_clone_output)
        if zfs_clone_result.returncode != 0:
            return False, "The dataset already exists!"
        virt_clone_result=subprocess.run(['virt-clone', '-o', domain_name, '-n', new_domain_name, '--file', destdisk, '--preserve-data'],capture_output=True,universal_newlines=True)
        virt_clone_output=str(virt_clone_result.returncode)+', '+virt_clone_result.stdout+', '+virt_clone_result.stderr
        if virt_clone_result.returncode != 0:
            return False, "VM "+new_domain_name+" already exists!"
        print(virt_clone_output)
        return True, "VM {} successfully created.".format(new_domain_name)
    
    def cmd_create_snapshot(self, domain_name, snapshot_name):
        #zfs_vm_dataset='zfs-pool-libvirt-fyp/kvm-images/'
        zfs_vm_dataset='/'.join([Config.ZFS_POOL, Config.ZFS_DATASET, ''])
        #targetname=domain_name+'@'+snapshot_name
        targetname='@'.join([domain_name, snapshot_name])
        targetdataset=zfs_vm_dataset+targetname
        zfs_snapshot_result=subprocess.run(['zfs', 'snapshot', targetdataset],capture_output=True,universal_newlines=True)
        zfs_snapshot_output=str(zfs_snapshot_result.returncode)+', '+zfs_snapshot_result.stdout+', '+zfs_snapshot_result.stderr
        print(zfs_snapshot_output)
        if zfs_snapshot_result.returncode == 1:
            return False, "The snapshot already exist!"
        elif zfs_snapshot_result.returncode == 2:
            return False, "The VM doesn't exist!"
        return True, domain_name+"@"+snapshot_name
        
    def cmd_destroy_snapshot(self, domain_name, snapshot_name):
        zfs_vm_dataset='/'.join([Config.ZFS_POOL, Config.ZFS_DATASET, ''])
        #targetname=domain_name+'@'+snapshot_name
        targetname='@'.join([domain_name, snapshot_name])
        targetdataset=zfs_vm_dataset+targetname
        clone_result, clone_payload=self.internal_check_has_clones(domain_name)
        if clone_result == True:
            return False, "Clones found!, Please remove the following VMs before destroying snapshot:\n"+', '.join(clone_payload)
        elif clone_result is None:
            return False, "The specified domain name and the snapshot doesn't exist"
        zfs_destroy_result=subprocess.run(['zfs', 'destroy', targetdataset],capture_output=True,universal_newlines=True)
        zfs_destroy_output=str(zfs_destroy_result.returncode)+', '+zfs_destroy_result.stdout+', '+zfs_destroy_result.stderr
        print(zfs_destroy_output)
        if zfs_destroy_result.returncode != 0:
            return False, "The domain namesnapshot doesn't exist!"
        return True, domain_name+"@"+snapshot_name

    def internal_check_has_clones(self, domain_name):
        #zfs_vm_dataset='zfs-pool-libvirt-fyp/kvm-images/'
        zfs_vm_dataset='/'.join([Config.ZFS_POOL, Config.ZFS_DATASET, ''])
        targetname=domain_name
        targetdataset=zfs_vm_dataset+targetname
        #zfs get clones -H -o value zfs-pool-libvirt-fyp/kvm-images/vm-ubuntu-bionic-2-server-template-new@finish-install-20190311
        #parentresult,value=self.internal_check_has_parent(snapshot_name)
        #if parentresult is None:
        #    return False, "Clones has been found! Please remove clones first"
        #elif parentresult:
        zfs_snapshot_result=subprocess.run(['zfs', 'list', '-H', '-o', 'name', '-r', '-t', 'snapshot', targetdataset],capture_output=True,universal_newlines=True)
        zfs_snapshot_output=str(zfs_snapshot_result.returncode)+', '+zfs_snapshot_result.stdout+', '+zfs_snapshot_result.stderr
        snapshot_list_rstrip=str(zfs_snapshot_result.stdout).rstrip()
        snapshot_list=snapshot_list_rstrip.split('\n')
        for f in snapshot_list:
            zfs_clone_result=subprocess.run(['zfs', 'get', 'clones', '-H', '-o', 'value', f],capture_output=True,universal_newlines=True)
            zfs_clone_output=str(zfs_clone_result.returncode)+', '+zfs_clone_result.stdout+', '+zfs_clone_result.stderr
            print(zfs_clone_output)
            if zfs_clone_result.returncode == 0:
                if str(zfs_clone_result.stdout).rstrip() != "":
                    return True, "Snapshot found in "+domain_name
        return False, domain_name
    
    def internal_check_has_parent(self, domain_name):
        #zfs get origin -H -o value zfs-pool-libvirt-fyp/kvm-images/vm-ubuntu-bionic-test-clone-27
        #zfs_vm_dataset='zfs-pool-libvirt-fyp/kvm-images/'
        zfs_vm_dataset='/'.join([Config.ZFS_POOL, Config.ZFS_DATASET, ''])
        targetdataset=zfs_vm_dataset+domain_name
        zfs_parent_result=subprocess.run(['zfs', 'get', 'origin', '-H', '-o', 'value', targetdataset],capture_output=True,universal_newlines=True)
        zfs_parent_output=str(zfs_parent_result.returncode)+', '+zfs_parent_result.stdout+', '+zfs_parent_result.stderr
        print(zfs_parent_output)
        if zfs_parent_result.returncode == 0:
            if str(zfs_parent_result.stdout).rstrip() == '-':
                return False, domain_name
            else:
                return True, str(zfs_parent_result.stdout).rstrip()
        else:
            return None, str(zfs_parent_result.stderr).rstrip()
        # return True, 'test'
