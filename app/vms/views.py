from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required
import time
from . import vms
from .forms import ModifyVMForm, SetUpVMForm, DeleteVMForm, CreateSnapshotForm
from ..libvirt_test import libvirt_test
from ..models import templates
from .. import db

@vms.route('/vm/detail/<vm_uuid>')
@login_required
def vm_detail(vm_uuid):
    """
    Render the details of the VM
    """
    run=libvirt_test()
    _, vm_detail=run.api_get_domain_detail(vm_uuid)
    return render_template('vm/vm_detail.html', title="VM Details for "+vm_detail[0], vm_detail=vm_detail)

@vms.route('/vm/start/<vm_uuid>')
@login_required
def vm_start(vm_uuid):
    """
    Render the details of the VM
    """
    run=libvirt_test()
    result, _=run.api_start_vm_uuid(vm_uuid)
    if result:
        _, vm_name=run.api_get_domain_name(vm_uuid)
        flash("VM "+vm_name+" is started.")
    else:
        flash("VM is missing! Possibly deleted manually?",category='error')
    return redirect(url_for('home.dashboard'))

@vms.route('/vm/shutdown/<vm_uuid>')
@login_required
def vm_shutdown(vm_uuid):
    """
    Render the details of the VM
    """
    run=libvirt_test()
    result, vm_detail=run.api_shutdown_vm_uuid(vm_uuid)
    if result:
        _, vm_name=run.api_get_domain_name(vm_uuid)
        flash("VM "+vm_name+" is shutting down.")
    time.sleep(3)
    return redirect(url_for('home.dashboard'))

@vms.route('/vm/poweroff/<vm_uuid>')
@login_required
def vm_poweroff(vm_uuid):
    """
    Render the details of the VM
    """
    run=libvirt_test()
    result, vm_detail=run.api_destroy_vm_uuid(vm_uuid)
    if result:
        _, vm_name=run.api_get_domain_name(vm_uuid)
        flash("VM "+vm_name+" is powering down.")
    time.sleep(3)
    return redirect(url_for('home.dashboard'))

@vms.route('/vm/modify/<vm_uuid>',methods=['POST','GET'])
@login_required
def vm_modify(vm_uuid):
    """
    Render the details of the VM
    """
    run=libvirt_test()
    form=ModifyVMForm()
    _,vm_detail=run.api_get_domain_detail(vm_uuid)
    if form.validate_on_submit():
        #department.name = form.name.data
        #department.description = form.description.data
        #db.session.commit()
        if int(form.vCPUs.data) != int(vm_detail[3]):
            result,_=run.api_set_vm_vcpu_count(vm_uuid,int(form.vCPUs.data))
            if result:
                flash('vCPU successfully set to '+str(form.vCPUs.data)+'!')
            else:
                flash("Failed to set vCPU count!",category='error')
        print(str(form.RAMSize.data)+", "+str(vm_detail[2]))
        if int(form.RAMSize.data) != int(vm_detail[2]):
            result,_=run.api_set_vm_ramsize_count(vm_uuid,int(form.RAMSize.data))
            if result:
                flash('RAM successfully set to '+str(form.RAMSize.data)+'!')
            else:
                flash("Failed to set memory size!",category='error')
        return redirect(url_for('vms.vm_modify',vm_uuid=vm_uuid, vm_name=vm_detail[0], title="Edit VM", form=form))
        #form.vCPUs.data = vm_detail[2]/1024
        #form.RAMSize.data = vm_detail[2]/1024
        # redirect to the departments page
        
    _,vm_detail=run.api_get_domain_detail(vm_uuid)
    form.vCPUs.data = str(vm_detail[3])
    form.RAMSize.data = str(vm_detail[2])
    return render_template('vm/vm_modify.html',vm_uuid=vm_uuid,vm_name=vm_detail[0],title='Edit VM',form=form)
    #return render_template('admin/departments/department.html', action="Edit", form=form,
    #                       title="Edit VM detail for "+ vm_detail[0])
    #run=libvirt_test()
    #result, vm_detail=run.api_destroy_vm_uuid(vm_uuid)
    #if result:
    #    _, vm_name=run.api_get_domain_name(vm_uuid)
    #    flash("VM "+vm_name+" is powering down")
    #time.sleep(3)
    #return redirect(url_for('home.dashboard'))

@vms.route('/vm/snapshot/create/<vm_uuid>',methods=['POST','GET'])
@login_required
def vm_snapshot(vm_uuid):
    """
    Render the details of the VM
    """
    run=libvirt_test()
    form=CreateSnapshotForm()
    _,vm_detail=run.api_get_domain_detail(vm_uuid)
    if form.validate_on_submit():
        #department.name = form.name.data
        #department.description = form.description.data
        #db.session.commit()
        result,_=run.cmd_create_snapshot(vm_detail[0], form.snapshotName.data)
        """if int(form.vCPUs.data) != int(vm_detail[3]):
            result,_=run.api_set_vm_vcpu_count(vm_uuid,int(form.vCPUs.data))
            if result:
                flash('vCPU successfully set to '+str(form.vCPUs.data)+'!')
            else:
                flash("Failed to set vCPU count!",category='error')
        print(str(form.RAMSize.data)+", "+str(vm_detail[2]))
        if int(form.RAMSize.data) != int(vm_detail[2]):
            result,_=run.api_set_vm_ramsize_count(vm_uuid,int(form.RAMSize.data))
            if result:
                flash('RAM successfully set to '+str(form.RAMSize.data)+'!')
            else:
                flash("Failed to set memory size!",category='error')"""
        if result:
            try:
                template_object=templates(domain_name=vm_detail[0],snapshot_name=form.snapshotName.data,is_templates=False)
                db.session.add(template_object)
                db.session.commit()

                flash("Snapshot "+form.snapshotName.data+" for VM "+vm_detail[0]+" created!")
                return redirect(url_for('home.dashboard'))
            except:
                # in case department name already exists
                flash("Snapshot creation failed: snapshot name exists on database!",category='error')
                return redirect(url_for('vms.vm_snapshot',vm_uuid=vm_uuid))
        else:
            flash("Snapshot creation failed: snapshot name exists on storage!",category='error')
            return render_template('vm/vm_create_snapshot.html',vm_uuid=vm_uuid, vm_name=vm_detail[0], title="Edit VM", form=form)
        
        #form.vCPUs.data = vm_detail[2]/1024
        #form.RAMSize.data = vm_detail[2]/1024
        # redirect to the departments page
    form.snapshotName.data = vm_detail[0]+"-snapshot"
    return render_template('vm/vm_create_snapshot.html',vm_uuid=vm_uuid,vm_name=vm_detail[0],title='Edit VM',form=form)

@vms.route('/vm/create',methods=['POST','GET'])
@login_required
def vm_create():
    """
    Render the details of the VM
    """
    run=libvirt_test()
    limit=200
    result,vm_list=run.api_list_domains()
    snap_count=templates.query.filter_by(is_templates=False).count()
    if len(vm_list)>=limit:
        flash("Limit reached! Only up to "+str(limit)+" VMs can be created.",category='error')
        return redirect(url_for('home.dashboard'))
    return render_template('vm/vm_create.html',title='Create VM',snap_count=snap_count)

"""@vms.route('/vm/create/template',methods=['POST','GET'])
@login_required
def vm_create_template():"""
"""
    Render the details of the VM
    
    run=libvirt_test()
    form=ModifyVMForm()
    _,vm_detail=run.api_get_domain_detail(vm_uuid)
    if form.validate_on_submit():
        #department.name = form.name.data
        #department.description = form.description.data
        #db.session.commit()
        if int(form.vCPUs.data) != int(vm_detail[3]):
            result,_=run.api_set_vm_vcpu_count(vm_uuid,int(form.vCPUs.data))
            if result:
                flash('vCPU successfully set to '+str(form.vCPUs.data)+'!')
            else:
                flash("Failed to set vCPU count!",category='error')
        print(str(form.RAMSize.data)+", "+str(vm_detail[2]))
        if int(form.RAMSize.data) != int(vm_detail[2]):
            result,_=run.api_set_vm_ramsize_count(vm_uuid,int(form.RAMSize.data))
            if result:
                flash('RAM successfully set to '+str(form.RAMSize.data)+'!')
            else:
                flash("Failed to set memory size!",category='error')
        return redirect(url_for('vms.vm_modify',vm_uuid=vm_uuid, vm_name=vm_detail[0], title="Edit VM", form=form))
        #form.vCPUs.data = vm_detail[2]/1024
        #form.RAMSize.data = vm_detail[2]/1024
        # redirect to the departments page
        
    _,vm_detail=run.api_get_domain_detail(vm_uuid)
    form.vCPUs.data = str(vm_detail[3])
    form.RAMSize.data = str(vm_detail[2])
    return render_template('vm/vm_modify.html',vm_uuid=vm_uuid,vm_name=vm_detail[0],title='Edit VM',form=form)"""

@vms.route('/vm/create/<create_type>',methods=['POST','GET'])
@login_required
def vm_create_type(create_type):
    #template_list=templates.query.all()
    if create_type=="template":
        template_list=templates.query.filter_by(is_templates=True).all()
        
    elif create_type=="snapshot":
        #if templates.query.first
        template_list=templates.query.filter_by(is_templates=False).all()
    print(template_list)
    return render_template("vm/vm_select_type.html",title="Select "+create_type, create_type=create_type, template_list=template_list)
    """
    Render the details of the VM
    """
    """run=libvirt_test()
    form=ModifyVMForm()
    _,vm_detail=run.api_get_domain_detail(vm_uuid)
    if form.validate_on_submit():
        #department.name = form.name.data
        #department.description = form.description.data
        #db.session.commit()
        if int(form.vCPUs.data) != int(vm_detail[3]):
            result,_=run.api_set_vm_vcpu_count(vm_uuid,int(form.vCPUs.data))
            if result:
                flash('vCPU successfully set to '+str(form.vCPUs.data)+'!')
            else:
                flash("Failed to set vCPU count!",category='error')
        print(str(form.RAMSize.data)+", "+str(vm_detail[2]))
        if int(form.RAMSize.data) != int(vm_detail[2]):
            result,_=run.api_set_vm_ramsize_count(vm_uuid,int(form.RAMSize.data))
            if result:
                flash('RAM successfully set to '+str(form.RAMSize.data)+'!')
            else:
                flash("Failed to set memory size!",category='error')
        return redirect(url_for('vms.vm_modify',vm_uuid=vm_uuid, vm_name=vm_detail[0], title="Edit VM", form=form))
        #form.vCPUs.data = vm_detail[2]/1024
        #form.RAMSize.data = vm_detail[2]/1024
        # redirect to the departments page
        
    _,vm_detail=run.api_get_domain_detail(vm_uuid)
    form.vCPUs.data = str(vm_detail[3])
    form.RAMSize.data = str(vm_detail[2])
    return render_template('vm/vm_modify.html',vm_uuid=vm_uuid,vm_name=vm_detail[0],title='Edit VM',form=form)"""

@vms.route('/vm/create/<create_type>/<int:id>',methods=['POST','GET'])
@login_required
def vm_create_setup(create_type,id):
    """
    Render the details of the VM
    """
    run=libvirt_test()
    form=SetUpVMForm()
    template_info = templates.query.get_or_404(id)
    result,old_vm_uuid=run.api_get_uuid(template_info.domain_name)
    _,old_vm_detail=run.api_get_domain_detail(old_vm_uuid)
    if old_vm_detail[5]!=5:
        flash("Cannot create clones: VM "+old_vm_detail[0]+" is still running.",category="error")
        return redirect(url_for('home.dashboard'))
    if form.validate_on_submit():
        #department.name = form.name.data
        #department.description = form.description.data
        #db.session.commit()
        result,output=run.cmd_create_vm(template_info.domain_name,template_info.snapshot_name,form.newVMName.data)
        print(str(result)+", "+output)
        if result:
            result_string=""
            _,new_vm_uuid=run.api_get_uuid(form.newVMName.data)
            _,new_vm_detail=run.api_get_domain_detail(new_vm_uuid)
            if int(form.vCPUs.data) != int(old_vm_detail[3]):
                result,_=run.api_set_vm_vcpu_count(new_vm_detail[4],int(form.vCPUs.data))
                if result:
                    #flash('vCPU successfully set to '+str(form.vCPUs.data)+'!')
                    #result_string+='vCPU successfully set to '+str(form.vCPUs.data)+'!'
                    pass
                else:
                    flash("Failed to set vCPU count!",category='error')
                    return redirect(url_for('vms.vm_create_setup',create_type=create_type, id=id))
            
            if int(form.RAMSize.data) != int(old_vm_detail[2]):
                result,_=run.api_set_vm_ramsize_count(new_vm_detail[4],int(form.RAMSize.data))
                if result:
                    #flash('vCPU successfully set to '+str(form.RAMSize.data)+'!')
                    #'vCPU successfully set to '+str(form.vCPUs.data)+'!'
                    pass
                else:
                    flash("Failed to set memory size!",category='error')
                    return redirect(url_for('vms.vm_create_setup',create_type=create_type, id=id))
            flash("VM "+form.newVMName.data+" has been successfully created!")
            return redirect(url_for('home.dashboard'))
        else:
            flash("Error! The selected VM has already existed!. Please try again.",category='error')
            return redirect(url_for('vms.vm_create_setup',create_type=create_type, id=id))
        return render_template('vm/vm_modify.html',vm_uuid=old_vm_uuid,vm_name=old_vm_detail[0],title='Edit VM',form=form)
        #form.vCPUs.data = vm_detail[2]/1024
        #form.RAMSize.data = vm_detail[2]/1024
        # redirect to the departments page
        
    _,vm_detail=run.api_get_domain_detail(old_vm_uuid)
    form.vCPUs.data = str(vm_detail[3])
    form.RAMSize.data = str(vm_detail[2])
    form.newVMName.data=template_info.domain_name+"-new"
    return render_template('vm/vm_modify.html',vm_uuid=vm_detail[4],vm_name=vm_detail[0],title='Edit VM',form=form)

@vms.route('/vm/snapshot/list', methods=['GET', 'POST'])
@login_required
def vm_list_snapshot():
    """
    List all departments
    """
    """check_admin()

    departments = Department.query.all()

    return render_template('admin/departments/departments.html',
                           departments=departments, title="Departments")"""
    template_list=templates.query.all()
    return render_template("vm/vm_list_snapslate.html",snapslate_list=template_list,title="Template and Snapshot Management")

@vms.route('/vm/snapshot/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def vm_delete_snapshot(id):
    """
    Delete a department from the database
    """
    """check_admin()

    department = Department.query.get_or_404(id)
    db.session.delete(department)
    db.session.commit()
    flash('You have successfully deleted the department.')

    # redirect to the departments page
    return redirect(url_for('admin.list_departments'))

    return render_template(title="Delete Department")"""
    template=templates.query.get_or_404(id)
    run=libvirt_test()
    result,_=run.cmd_destroy_snapshot(template.domain_name,template.snapshot_name)
    if result:
        #template = templates.query.get_or_404(id)
        db.session.delete(template)
        db.session.commit()
        flash("Template/snapshot is deleted.")
        return redirect(url_for('vms.vm_list_snapshot'))
    else:
        flash("Error deleting template/snapshot: Not found.",category='error')
        return redirect(url_for('vms.vm_list_snapshot'))

@vms.route('/vm/snapshot/toggle/<int:id>', methods=['GET', 'POST'])
@login_required
def vm_toggle_snapshot(id):
    """
    Delete a department from the database
    """
    """check_admin()

    department = Department.query.get_or_404(id)
    db.session.delete(department)
    db.session.commit()
    flash('You have successfully deleted the department.')

    # redirect to the departments page
    return redirect(url_for('admin.list_departments'))

    return render_template(title="Delete Department")"""
    template=templates.query.get_or_404(id)
    template.is_templates=not(template.is_templates)
    try:
        db.session.flush()
        db.session.commit()
        flash("Snapshot "+template.snapshot_name+" type toggled successfully!")
        return redirect(url_for('vms.vm_list_snapshot'))
    except:
        flash("Error deleting template/snapshot: Not found.",category='error')
        return redirect(url_for('vms.vm_list_snapshot'))


@vms.route('/vm/delete/<vm_uuid>',methods=['GET','POST'])
@login_required
def vm_delete(vm_uuid):
    """
    Render the details of the VM
    """
    form=DeleteVMForm()
    run=libvirt_test()
    print("debug_check")
    result, vm_detail=run.api_get_domain_detail(vm_uuid)

    if form.validate_on_submit():
        #department.name = form.name.data
        #department.description = form.description.data
        #db.session.commit()
        #if form.pleasedeletemyvm.data=="Yes, please delete this VM now.":
        if form.pleasedeletemyvm.data==vm_detail[0]:
            
            result,_=run.api_delete_vm(vm_uuid)
            if result:
                db.session.query(templates).filter_by(domain_name=vm_detail[0]).delete()
                db.session.commit()
                flash("VM "+vm_detail[0]+" has been deleted.")
                return redirect(url_for('home.dashboard'))
        else:
            flash("You did not provide the correct sentence!")
            return redirect(url_for("vms.vm_delete",vm_uuid=vm_uuid))
            #return render_template("vm/vm_delete.html", vm_name=str(vm_detail[0]), title="Delete VM", form=form)
        
        #form.vCPUs.data = vm_detail[2]/1024
        #form.RAMSize.data = vm_detail[2]/1024
        # redirect to the departments page
    result,_=run.internal_check_has_clones(vm_detail[0])
    if result:
        flash("VM "+vm_detail[0]+" has at least one template or snapshots.",category='error')
        return redirect(url_for('home.dashboard'))
    return render_template("vm/vm_delete.html", vm_name=str(vm_detail[0]), title="Delete VM", form=form)
#@home.route('/admin/dashboard')
#@login_required
#def admin_dashboard():
#    if not current_user.is_admin:
#        abort(403)
#    return render_template('home/admin_dashboard.html', title='Dashboard')

#@home.route('/dashboard')
#@login_required
#def dashboard():
#    """
#    Render the dashboard template on the /dashboard route
#    """
#    run=libvirt_test()
#    result,vm_list=run.api_list_domains()
#    return render_template('home/dashboard.html', title="Dashboard",vm_list=vm_list)
