import os
from dotenv import load_dotenv

from src.database.service.mongo_client import MongoDBClient
from src.util.datetime_helper import get_current_dt_in_milliseconds_precision
from src.util.generate_id import generate_client_id
from src.util.password_helper import PasswordHelper
from src.models.employee_object import InternalEmployeeInfo
from src.models.authentication_object import LoginObject

load_dotenv()

class EmployeeDBProvider():
    def __init__(self):
        self.mongodb_client = MongoDBClient()
        self.password_helper = PasswordHelper()
        self.db_name = str(os.getenv("CLIENT_DB_NAME"))
        self.employee_collection = str(os.getenv("EMPLOYEE_COLLECTION"))
        self.client_count = self.mongodb_client.count_all_records_from_collection(self.db_name, self.employee_collection)
        self.current_dt = get_current_dt_in_milliseconds_precision()
        self.client_id = "CA-" + "2600" + str(generate_client_id(self.client_count))
        
    def fetch_employee_list_from_database(self):
        client_list = self.mongodb_client.fetch_all_records_from_collection(self.db_name, self.employee_collection)
        return client_list
    
    def add_new_employee_in_database(self, request, client_id, employee_id):
        emp_count = self.mongodb_client.count_all_records_from_collection(self.db_name, self.employee_collection)
        employee_id= "EMP-" + "2600" + str(generate_client_id(emp_count))
        data = request.get_json()
        if data:
            update_data = InternalEmployeeInfo(
            client_id=client_id,
            employee_id= employee_id,
            employee_name= data.get('legal_name', None),
            employee_initials=data.get('display_name', None),
            dob = data.get('dob'),
            doj = data.get('doj'),
            pan=data.get('pan', None),
            aadhar=data.get('aadhar', None),
            registered_address=data.get('address', None),
            city=data.get('city', None),
            state=data.get('state', None),
            pincode=data.get('pincode', None),
            manager_name=data.get('manager_name', None),
            manager_id= data.get('manager_id', None),
            department=data.get('department', None),
            designation=data.get('designation', None),
            role=data.get('role', None),
            employee_added_by= employee_id,
            createdAt=get_current_dt_in_milliseconds_precision(),
            updatedAt=get_current_dt_in_milliseconds_precision()
        )
        
        self.mongodb_client.insert_one_item_in_collection(self.db_name, self.employee_collection,
                                                     update_data.model_dump())
        
        # create super admin login
        update_login_data = LoginObject(
                client_id= client_id,
                employee_id= employee_id,
                email = data.get("admin_email", None),
                password = self.password_helper.generate_password_hash("EMP-" + "2600" + str(generate_client_id(0))),  # type: ignore
                rbac_role= ["super_admin","Employee"],
                createdAt= self.current_dt,
                updatedAt= self.current_dt
            )
            
        self.mongodb_client.insert_one_item_in_collection("user_info", "LoginInfo",
                                                        update_login_data.model_dump())
    