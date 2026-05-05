from flask import Blueprint, render_template

admin_finance_bp = Blueprint('admin_finance_bp', __name__, template_folder='templates', static_folder='static')

### billing management routes ###

@admin_finance_bp.route("/<client_id>/<employee_id>/admin/billing", methods=["GET"])
def billing(client_id: str, employee_id: str):
    return render_template("admin/billing/admin_client_billing.html", client_id=client_id, employee_id=employee_id)