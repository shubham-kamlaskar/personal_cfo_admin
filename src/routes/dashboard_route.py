import os
from dotenv import load_dotenv
from flask import Blueprint, render_template

from src.database.service.mongo_client import MongoDBClient
from src.util.password_helper import PasswordHelper

load_dotenv()


admin_dashboard_bp = Blueprint('admin_dashboard_bp', __name__, template_folder='templates', static_folder='static')

### dashboard management routes ###

@admin_dashboard_bp.route("/<client_id>/<employee_id>/admin/admin_dashboard", methods=["GET"])
def admin_dashboard(client_id: str, employee_id: str):
    return render_template("admin/dashboard/dashboard_panel.html", client_id=client_id, employee_id=employee_id)
