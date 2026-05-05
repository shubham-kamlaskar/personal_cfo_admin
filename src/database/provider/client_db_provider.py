import os
from dotenv import load_dotenv

from src.database.service.mongo_client import MongoDBClient
from src.util.datetime_helper import get_current_dt_in_milliseconds_precision
from src.util.generate_id import generate_client_id
from src.util.password_helper import PasswordHelper
from src.models.client_object import ClientInfo, ClientEmpInfo, ClientBillingInfo, ClientOnboarding, ClientSuperAdminInfo, ActiveStatus
from src.models.authentication_object import LoginObject

load_dotenv()

class ClientDBProvider():
    def __init__(self):
        self.mongodb_client = MongoDBClient()
        self.password_helper = PasswordHelper()
        self.db_name = str(os.getenv("CLIENT_DB_NAME"))
        self.client_onboarding_collection = str(os.getenv("CLIENT_ONBOARDING_COLLECTION"))
        self.client_count = self.mongodb_client.count_all_records_from_collection(self.db_name, self.client_onboarding_collection)
        self.current_dt = get_current_dt_in_milliseconds_precision()
        self.client_id = "CA-" + "2600" + str(generate_client_id(self.client_count))
        
    def fetch_client_list_from_database(self):
        client_list = self.mongodb_client.fetch_all_records_from_collection(self.db_name, self.client_onboarding_collection)
        return client_list
    
    def add_new_client_in_database(self, request, employee_id):
        client_count = self.mongodb_client.count_all_records_from_collection(self.db_name, self.client_onboarding_collection)
        client_id= "CLT-" + "2600" + str(generate_client_id(client_count))
        data = request.get_json()
        current_dt = get_current_dt_in_milliseconds_precision()
        if data:
            update_data = ClientInfo(
                client_id=client_id,
                client_onboarding= ClientOnboarding(
                    legal_name = data.get("legal_name", None),
                    short_name = data.get("short_name", None),
                    pan= data.get("pan", None),
                    gstin = data.get("gstin", None),
                    address = data.get("address", None),
                    city = data.get("city", None),
                    state = data.get("state", None),
                    pincode = data.get("pincode", None),
                    industry = data.get("industry", None),
                    notes = data.get("notes", None),
                    send_welcome_note = data.get("send_welcome_note", None),
                    client_added_by = employee_id,
                ),
            client_super_admin_info= ClientSuperAdminInfo(
                admin_name= data.get('admin_name', None),
                admin_email= data.get('admin_email', None),
                admin_phone= data.get('admin_phone', None),
                admin_designation= data.get('admin_designation', None),
                admin_department= data.get('admin_department', None),
            ),
            client_billing_info= ClientBillingInfo(
                plan = data.get('admin_name', None) ,
                payment_method= "",
                bank_account_name="",
                bank_account_number="",
                bank_ifsc_number="",
                billing_cycle= data.get('billing_cycle', None),
                billing_start_date= self.current_dt,
                next_billing_date= self.current_dt,
            ),
            client_emp_info = ClientEmpInfo(
                total_employees=data.get('billing_cycle', None),
                active_employees=data.get('billing_cycle', None)
            ),
            client_active_status= ActiveStatus(
                    is_approved= False,
                    is_active= False,
                    last_active_datetime= self.current_dt
            ),
            createdAt= self.current_dt,
            updatedAt= self.current_dt
            )
                    
            self.mongodb_client.insert_one_item_in_collection(self.db_name, self.client_onboarding_collection,
                                                        update_data.model_dump())
            
            # create super admin login
            update_login_data = LoginObject(
                client_id= client_id,
                employee_id= "EMP-" + "2600" + str(generate_client_id(0)),
                email = data.get("admin_email", None),
                password = self.password_helper.generate_password_hash("EMP-" + "2600" + str(generate_client_id(0))),  # type: ignore
                rbac_role= ["super_admin","Employee"],
                createdAt= self.current_dt,
                updatedAt= self.current_dt
            )
            
            self.mongodb_client.insert_one_item_in_collection("user_info", "LoginInfo",
                                                        update_login_data.model_dump())
            
        