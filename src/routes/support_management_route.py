from flask import Blueprint, render_template

admin_support_bp = Blueprint('admin_support_bp', __name__, template_folder='templates', static_folder='static')

### support management routes ###

@admin_support_bp.route("/<client_id>/<employee_id>/admin/support", methods=["GET"])
def support(client_id: str, employee_id: str):
    return render_template("admin/support/admin_support_ticket.html", client_id=client_id, employee_id=employee_id)
