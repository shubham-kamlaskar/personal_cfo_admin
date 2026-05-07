from flask import Blueprint, render_template, request, jsonify

from src.database.provider.employee_db_provider import EmployeeDBProvider

employee_db_provider = EmployeeDBProvider()

admin_employee_bp = Blueprint('admin_employee_bp', __name__, template_folder='templates', static_folder='static')

### user management routes ###

@admin_employee_bp.route("/<client_id>/<employee_id>/admin/employee/add", methods=["GET"])
def employee_add(client_id: str, employee_id: str):
    return render_template("admin/employee/admin_employee_onboarding.html", client_id=client_id, employee_id=employee_id)

@admin_employee_bp.route("/<client_id>/<employee_id>/admin/employee/add/confirm", methods=["POST"])
def confirm_employee_add(client_id: str, employee_id: str):
    employee_db_provider.add_new_employee_in_database(request=request, client_id=client_id, employee_id=employee_id)
        
    return jsonify({
            "status": "success",
            "message": "Employee create successfully!"
        })
    

@admin_employee_bp.route("/<client_id>/<employee_id>/admin/employee/list", methods=["GET"])
def employee_list(client_id: str, employee_id: str):
    fetch_employee_info = employee_db_provider.fetch_employee_list_from_database()
    return render_template("admin/employee/admin_user_list.html", client_id=client_id, employee_id=employee_id, employees=fetch_employee_info)
