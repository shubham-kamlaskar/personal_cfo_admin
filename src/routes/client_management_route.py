from flask import Blueprint, render_template, request, jsonify, redirect, url_for

from src.database.provider.client_db_provider import ClientDBProvider

client_db_provider = ClientDBProvider()

admin_client_bp = Blueprint('admin_client_bp', __name__, template_folder='templates', static_folder='static')

### client management routes ###

@admin_client_bp.route("/<client_id>/<employee_id>/admin/client/list", methods=["GET"])
def list_client(client_id: str, employee_id: str):
    fetch_client_onboarding = client_db_provider.fetch_client_list_from_database()
    return render_template("admin/client/admin_client_list.html", client_id=client_id, employee_id=employee_id, clients=fetch_client_onboarding)

@admin_client_bp.route("/<client_id>/<employee_id>/admin/client/add", methods=["GET"])
def add_client(client_id: str, employee_id: str):
    return render_template("admin/client/admin_add_client.html", client_id=client_id, employee_id=employee_id)

@admin_client_bp.route("/<client_id>/<employee_id>/admin/client/add/confirm", methods=["POST"])
def confirm_add_client(client_id: str, employee_id: str):
    target_id = request.args.get('target_id')
    if target_id:
        # Update existing client
        client_db_provider.update_client_in_database(target_id=target_id, request=request, employee_id=employee_id)
        return jsonify({
            "status": "success",
            "message": "Client updated successfully!"
        })
    else:
        # Add new client
        client_db_provider.add_new_client_in_database(request=request, employee_id=employee_id)    
        return jsonify({
            "status": "success",
            "message": "Client created successfully!"
        })
        

@admin_client_bp.route("/<client_id>/<employee_id>/admin/client/remove", methods=["GET", "POST"])
def remove_client(client_id: str, employee_id: str):
    target_id = request.args.get('target_id') or request.form.get('target_id')
    confirm = request.args.get('confirm') or request.form.get('confirm')
    if confirm == 'yes' and target_id:
        client_db_provider.delete_client_from_database(target_id=target_id)
        if request.method == 'POST':
            return jsonify({
                "status": "success",
                "redirect": url_for('admin_client_bp.list_client', client_id=client_id, employee_id=employee_id)
            })
        return redirect(url_for('admin_client_bp.list_client', client_id=client_id, employee_id=employee_id))
    return redirect(url_for('admin_client_bp.list_client', client_id=client_id, employee_id=employee_id))

@admin_client_bp.route("/<client_id>/<employee_id>/admin/client/modify", methods=["GET"])
def modify_client(client_id: str, employee_id: str):
    target_id = request.args.get('target_id')
    if target_id:
        client_data = client_db_provider.fetch_single_client_from_database(target_id)
        return render_template("admin/client/admin_add_client.html", client_id=client_id, employee_id=employee_id, target_id=target_id, client=client_data)
    return render_template("admin/client/admin_add_client.html", client_id=client_id, employee_id=employee_id)
