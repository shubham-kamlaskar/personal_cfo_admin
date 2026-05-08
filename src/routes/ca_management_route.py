from flask import Blueprint, render_template, request, jsonify, url_for, redirect

from src.database.provider.ca_db_provider import CADBProvider

ca_db_provider = CADBProvider()

admin_ca_bp = Blueprint('admin_ca_bp', __name__, template_folder='templates', static_folder='static')

### ca management routes ###

@admin_ca_bp.route("/<client_id>/<employee_id>/admin/ca/add", methods=["GET"])
def add_ca(client_id: str, employee_id: str):
    return render_template("admin/ca/admin_add_ca.html", client_id=client_id, employee_id=employee_id)

@admin_ca_bp.route("/<client_id>/<employee_id>/admin/ca/add/confirm", methods=["POST"])
def confirm_add_ca(client_id: str, employee_id: str):
    target_id = request.args.get('target_id')
    if target_id:
        # Update existing client
        ca_db_provider.update_client_in_database(target_id=target_id, request=request, employee_id=employee_id)
        return jsonify({
            "status": "success",
            "message": "Client updated successfully!"
        })
    else:
        # Add new client
        ca_db_provider.add_new_ca_in_database(request, client_id=client_id, employee_id=employee_id) 
        return jsonify({
            "status": "success",
            "message": "Client created successfully!"
        })

@admin_ca_bp.route("/<client_id>/<employee_id>/admin/ca/list", methods=["GET"])
def ca_list(client_id: str, employee_id: str):
    fetch_ca_info = ca_db_provider.fetch_ca_list_from_database()
    return render_template("admin/ca/admin_ca_list.html", client_id=client_id, employee_id=employee_id, cas=fetch_ca_info)

@admin_ca_bp.route("/<client_id>/<employee_id>/admin/ca/remove", methods=["GET", "POST"])
def remove_ca(client_id: str, employee_id: str):
    target_id = request.args.get('target_id') or request.form.get('target_id')
    confirm = request.args.get('confirm') or request.form.get('confirm')
    if confirm == 'yes' and target_id:
        ca_db_provider.delete_ca_from_database(target_id=target_id)
        if request.method == 'POST':
            return jsonify({
                "status": "success",
                "redirect": url_for('admin_ca_bp.list_client', client_id=client_id, employee_id=employee_id)
            })
        return redirect(url_for('admin_ca_bp.list_ca', client_id=client_id, employee_id=employee_id))
    return redirect(url_for('admin_ca_bp.list_ca', client_id=client_id, employee_id=employee_id))

@admin_ca_bp.route("/<client_id>/<employee_id>/admin/ca/modify", methods=["GET"])
def modify_ca(client_id: str, employee_id: str):
    target_id = request.args.get('target_id')
    if target_id:
        ca_data = ca_db_provider.fetch_single_ca_from_database(target_id)
        return render_template("admin/ca/admin_add_ca.html", client_id=client_id, employee_id=employee_id, target_id=target_id, ca=ca_data)
    return render_template("admin/ca/admin_add_ca.html", client_id=client_id, employee_id=employee_id)

