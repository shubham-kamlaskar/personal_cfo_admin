from flask import Blueprint, render_template, request, jsonify

from src.database.provider.ca_db_provider import CADBProvider

ca_db_provider = CADBProvider()

admin_ca_bp = Blueprint('admin_ca_bp', __name__, template_folder='templates', static_folder='static')

### ca management routes ###

@admin_ca_bp.route("/<client_id>/<employee_id>/admin/ca/add", methods=["GET"])
def add_ca(client_id: str, employee_id: str):
    return render_template("admin/ca/admin_add_ca.html", client_id=client_id, employee_id=employee_id)

@admin_ca_bp.route("/<client_id>/<employee_id>/admin/ca/add/confirm", methods=["POST"])
def confirm_add_ca(client_id: str, employee_id: str):
    ca_db_provider.add_new_ca_in_database(request, client_id=client_id, employee_id=employee_id)
    
    return jsonify({
        "status": "success",
        "message": "CA created successfully!"
    })

@admin_ca_bp.route("/<client_id>/<employee_id>/admin/ca/list", methods=["GET"])
def ca_list(client_id: str, employee_id: str):
    fetch_ca_info = ca_db_provider.fetch_ca_list_from_database()
    return render_template("admin/ca/admin_ca_list.html", client_id=client_id, employee_id=employee_id, cas=fetch_ca_info)