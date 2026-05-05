from flask import Blueprint, render_template

admin_analytics_bp = Blueprint('admin_analytics_bp', __name__, template_folder='templates', static_folder='static')

### analytics management routes ###

@admin_analytics_bp.route("/<client_id>/<employee_id>/admin/analytics", methods=["GET"])
def analytics(client_id: str, employee_id: str):
    return render_template("admin/analytics/admin_expense_analytics.html", client_id=client_id, employee_id=employee_id)
