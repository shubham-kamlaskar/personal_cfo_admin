import os
from dotenv import load_dotenv

from src.database.service.mongo_client import MongoDBClient
from src.util.datetime_helper import get_current_dt_in_milliseconds_precision
from src.util.generate_id import generate_client_id
from src.util.password_helper import PasswordHelper
from src.models.employee_object import EmployeeOnboarding
from src.models.authentication_object import LoginObject

load_dotenv()

class EmployeeDBProvider():
    def __init__(self):
        self.mongodb_client = MongoDBClient()
        self.password_helper = PasswordHelper()
        self.db_name = str(os.getenv("DB_NAME"))
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
            update_data = EmployeeOnboarding(
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
    
    def update_employee_in_database(self, target_id, request, employee_id):
        data = request.get_json()
        current_dt = get_current_dt_in_milliseconds_precision()
        if data and target_id:
            update_data = {
                "personal_info": {
                    "title": data.get("title", None),
                    "full_name": data.get("full_name", None),
                    "alternate_email": data.get("alternate_email", None),
                    "phone": data.get("phone", None),
                    "whatsapp": data.get("whatsapp", None),
                    "dob": data.get("dob", None),
                    "gender": data.get("gender", None),
                    "address": data.get("address", None),
                    "city": data.get("city", None),
                    "state": data.get("state", None),
                    "pincode": data.get("pincode", None),
                    "pan": data.get("pan", None),
                    "aadhaar": data.get("aadhaar", None),
                    "updatedAt": self.current_dt,
                },
                "professional_info": {
                    "icai_number":data.get("icai_number", None),
                    "membership_type":data.get("membership_type", None),
                    "qualification_date":data.get("qualification_date", None),
                    "experience_years":data.get("experience_years", None),
                    "cop_number":data.get("cop_number", None),
                    "firm_name":data.get("firm_name", None),
                    "firm_registration":data.get("firm_registration", None),
                    "office_address":data.get("office_address", None),
                    "office_city":data.get("office_city", None),
                    "office_state":data.get("office_state", None),
                    "office_pincode":data.get("office_pincode", None),
                    "bio":data.get("bio", None),
                    "updatedAt":self.current_dt,
                },
                "specialization": {
                    "primary_specialization":data.get("primary_specialization", None),
                    "client_size":data.get("client_size", None),
                    "languages":data.get("languages", None),
                    "additional_services":data.getlist("additional_services"),
                    "tax_services":data.getlist("tax_services"),
                    "industry_expertise":data.getlist("industry_expertise"),
                    "updatedAt":self.current_dt,
                },
                "documents": {
                    "icai_cert":request.filesget("icai_cert").filename if request.filesget("icai_cert") else None,
                    "cop_cert":request.filesget("cop_cert").filename if request.filesget("cop_cert") else None,
                    "pan_doc":request.filesget("pan_doc").filename if request.filesget("pan_doc") else None,
                    "aadhaar_doc":request.filesget("aadhaar_doc").filename if request.filesget("aadhaar_doc") else None,
                    "resume":request.filesget("resume").filename if request.filesget("resume") else None,
                    "photo":request.filesget("photo").filename if request.filesget("photo") else None,
                    "certs":request.filesget("certs").filename if request.filesget("certs") else None,
                    "updatedAt":self.current_dt,
                },
                "service_agreement": {
                    "engagement_type":data.get("engagement_type", None) ,
                    "rate_itr_individual":data.get("rate_itr_individual", None) ,
                    "rate_itr_business":data.get("rate_itr_business", None) ,
                    "rate_consultation":data.get("rate_consultation", None) ,
                    "rate_gsts":data.get("rate_gst", None) ,
                    "revenue_share":data.get("revenue_share", None) ,
                    "payment_terms":data.get("payment_terms", None) ,
                    "max_clients":data.get("max_clients", None) ,
                    "response_time":data.get("response_time", None) ,
                    "work_hours_from":data.get("work_hours_from", None) ,
                    "work_hours_to":data.get("work_hours_to", None) ,
                    "working_day":data.getlist("working_day") ,
                    "bank_account_name":data.get("bank_account_name", None) ,
                    "bank_name":data.get("bank_name", None) ,
                    "bank_ifsc":data.get("bank_ifsc", None) ,
                    "updatedAt":self.current_dt,
                }                     
            }
            
            filter_id = {'client_id': target_id}
            self.mongodb_client.update_one_item_in_collection(self.db_name, self.employee_collection  , filter_id, update_data)
        print("Item deleted successfully")
        
    def delete_employee_from_database(self, target_id):
        filter_id = {'ca_id': target_id}
        self.mongodb_client.delete_one_item_from_collection(self.db_name, self.employee_collection, filter_id)
        
    def fetch_single_employee_from_database(self, employee_id):
        filter_items = {'employee_id': employee_id}
        client_data = self.mongodb_client.find_one_item_from_collection(self.db_name, self.employee_collection, filter_items)
        return client_data
            
        