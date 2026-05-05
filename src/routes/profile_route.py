import os
from dotenv import load_dotenv
import logging

from flask import Blueprint, render_template, request, redirect, url_for
from src.database.service.mongo_client import MongoDBClient
from src.util.app_constants import VariableConstant
from src.database.provider.edit_profile_strategy import update_profile_in_db
# from src.util.access_provider import login_required

load_dotenv()
mongodb_client = MongoDBClient()
user_info_collection = str(os.getenv('USER_INFO_COLLECTION'))
db_name = str(os.getenv('DB_NAME'))
EMPLOYEE_ID_FIELD_DB =  VariableConstant.EMPLOYEE_ID_FIELD_DB
logger = logging.getLogger(__name__)

user_profile_bp = Blueprint('user_profile_bp', __name__, template_folder='templates', static_folder='static')

@user_profile_bp.route('/<client_id>/<employee_id>/profile', methods=["GET"])
# @login_required
def profile(client_id: str, employee_id: str):
    try:
        filter_items = {"client_id": client_id, 'employee_id': employee_id}
        fetch_user_info = mongodb_client.find_one_item_from_collection(db_name, user_info_collection, filter_items)
        return render_template("employee/profile/profile.html", user=fetch_user_info, client_id= client_id, employee_id=employee_id)
    except Exception as e:
        logger.error(f"An error occured in profile route: {str(e)}")
        return "An error occurred while loading the profile.", 500
        
@user_profile_bp.route('/<client_id>/<employee_id>/edit_profile', methods=["GET", "POST"])
# @login_required
def edit_profile(client_id: str, employee_id: str):
    try:
        filter_items = {"client_id": client_id, 'employee_id': employee_id}
        fetch_user_info = mongodb_client.find_one_item_from_collection(db_name, user_info_collection, filter_items)
        if request.method == "POST":
            data = request.form
            if data:
                update_profile_in_db(data, client_id, employee_id, fetch_user_info)
            
            return redirect(url_for('user_profile_bp.profile', client_id=client_id, employee_id=employee_id))

        return render_template('profile/edit_profile.html', user=fetch_user_info, client_id=client_id, employee_id=employee_id)
    except Exception as e:
        logger.error(f"An error occured in edit_profile route: {str(e)}")
        return "An error occurred while processing the edit profile request.", 500