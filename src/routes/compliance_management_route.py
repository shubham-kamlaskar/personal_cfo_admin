from flask import Blueprint, render_template

admin_compliance_bp = Blueprint('admin_compliance_bp', __name__, template_folder='templates', static_folder='static')

### compliance management routes ###

@admin_compliance_bp.route("/<client_id>/<employee_id>/admin/compliance", methods=["GET"])
def compliance(client_id: str, employee_id: str):
    return render_template("admin/compliance/admin_compliance_checker.html", client_id=client_id, employee_id=employee_id)