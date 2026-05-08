from flask import Blueprint, render_template, request, jsonify, redirect, url_for

from src.database.provider.employee_db_provider import EmployeeDBProvider

employee_db_provider = EmployeeDBProvider()

admin_employee_bp = Blueprint('admin_employee_bp', __name__, template_folder='templates', static_folder='static')

### user management routes ###

@admin_employee_bp.route("/<client_id>/<employee_id>/admin/employee/add", methods=["GET"])
def add_employee(client_id: str, employee_id: str):
    return render_template("admin/employee/admin_employee_onboarding.html", client_id=client_id, employee_id=employee_id)

@admin_employee_bp.route("/<client_id>/<employee_id>/admin/employee/add/confirm", methods=["POST"])
def confirm_add_employee(client_id: str, employee_id: str):
    employee_db_provider.add_new_employee_in_database(request=request, client_id=client_id, employee_id=employee_id)
        
    return jsonify({
            "status": "success",
            "message": "Employee create successfully!"
        })
    

@admin_employee_bp.route("/<client_id>/<employee_id>/admin/employee/list", methods=["GET"])
def employee_list(client_id: str, employee_id: str):
    fetch_employee_info = employee_db_provider.fetch_employee_list_from_database()
    return render_template("admin/employee/admin_employee_list.html", client_id=client_id, employee_id=employee_id, employees=fetch_employee_info)

@admin_employee_bp.route("/<client_id>/<employee_id>/admin/employee/remove", methods=["GET", "POST"])
def remove_employee(client_id: str, employee_id: str):
    target_id = request.args.get('target_id') or request.form.get('target_id')
    confirm = request.args.get('confirm') or request.form.get('confirm')
    if confirm == 'yes' and target_id:
        employee_db_provider.delete_employee_from_database(target_id=target_id)
        if request.method == 'POST':
            return jsonify({
                "status": "success",
                "redirect": url_for('admin_employee_bp.list_client', client_id=client_id, employee_id=employee_id)
            })
        return redirect(url_for('admin_employee_bp.list_employee', client_id=client_id, employee_id=employee_id))
    return redirect(url_for('admin_employee_bp.list_employee', client_id=client_id, employee_id=employee_id))

@admin_employee_bp.route("/<client_id>/<employee_id>/admin/employee/modify", methods=["GET"])
def modify_employee(client_id: str, employee_id: str):
    target_id = request.args.get('target_id')
    if target_id:
        employee_data = employee_db_provider.fetch_single_employee_from_database(target_id)
        return render_template("admin/employee/admin_add_employee.html", client_id=client_id, employee_id=employee_id, target_id=target_id, employee=employee_data)
    return render_template("admin/employee/admin_add_employee.html", client_id=client_id, employee_id=employee_id)

