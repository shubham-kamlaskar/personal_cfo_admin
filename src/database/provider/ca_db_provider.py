import os
from dotenv import load_dotenv

from src.database.service.mongo_client import MongoDBClient
from src.util.datetime_helper import get_current_dt_in_milliseconds_precision
from src.util.generate_id import generate_client_id
from src.util.password_helper import PasswordHelper
from src.models.ca_object import LoginObject, CAInfo, PersonalInfo, CAServiceAgreement, CADocuments, CAProfessionalInfo, CASpecialization, ActiveStatus

load_dotenv()

class CADBProvider():
    def __init__(self):
        self.mongodb_client = MongoDBClient()
        self.password_helper = PasswordHelper()
        self.db_name = str(os.getenv("CLIENT_DB_NAME"))
        self.ca_collection = str(os.getenv("CA_COLLECTION"))
        self.ca_count = self.mongodb_client.count_all_records_from_collection(self.db_name, self.ca_collection)
        self.current_dt = get_current_dt_in_milliseconds_precision()
        self.client_id = "CA-" + "2600" + str(generate_client_id(self.ca_count))
    
    
    def add_new_ca_in_database(self, request, client_id, employee_id):
        form = request.form
        files = request.files
        update_login_data = LoginObject(
            client_id=client_id,
            employee_id = employee_id,
            email = form.get("email", None),
            password = self.password_helper.generate_password_hash(employee_id), # type: ignore
            rbac_role= ["ca", "employee"],
            createdAt= self.current_dt,
            updatedAt= self.current_dt
        )
        self.mongodb_client.insert_one_item_in_collection("user_info", "LoginInfo",
                                                    update_login_data.model_dump())
        
        update_ca_info = CAInfo(
                    client_id=client_id,
                    employee_id = employee_id,
                    personal_info= PersonalInfo(
                    title= form.get("title", None),
                    full_name = form.get("full_name", None),
                    alternate_email = form.get("alternate_email", None),
                    phone = form.get("phone", None),
                    whatsapp = form.get("whatsapp", None),
                    dob = form.get("dob", None),
                    gender = form.get("gender", None),
                    address = form.get("address", None),
                    city = form.get("city", None),
                    state = form.get("state", None),
                    pincode = form.get("pincode", None),
                    pan = form.get("pan", None),
                    aadhaar = form.get("aadhaar", None),
                    createdAt= self.current_dt,
                    updatedAt= self.current_dt,
                    ),
                    professional_info= CAProfessionalInfo(
                    icai_number= form.get("icai_number", None),
                    membership_type= form.get("membership_type", None),
                    qualification_date= form.get("qualification_date", None),
                    experience_years= form.get("experience_years", None),
                    cop_number= form.get("cop_number", None),
                    firm_name= form.get("firm_name", None),
                    firm_registration= form.get("firm_registration", None),
                    office_address= form.get("office_address", None),
                    office_city= form.get("office_city", None),
                    office_state= form.get("office_state", None),
                    office_pincode= form.get("office_pincode", None),
                    bio= form.get("bio", None),
                    createdAt= self.current_dt,
                    updatedAt= self.current_dt,
                ),
                    specialization= CASpecialization(
                    primary_specialization= form.get("primary_specialization", None),
                    client_size= form.get("client_size", None),
                    languages= form.get("languages", None),
                    additional_services= form.getlist("additional_services"),
                    tax_services= form.getlist("tax_services"),
                    industry_expertise= form.getlist("industry_expertise"),
                    createdAt= self.current_dt,
                    updatedAt= self.current_dt,
                    ),
                    documents= CADocuments(
                    icai_cert = files.get("icai_cert").filename if files.get("icai_cert") else None,
                    cop_cert = files.get("cop_cert").filename if files.get("cop_cert") else None,
                    pan_doc = files.get("pan_doc").filename if files.get("pan_doc") else None,
                    aadhaar_doc = files.get("aadhaar_doc").filename if files.get("aadhaar_doc") else None,
                    resume = files.get("resume").filename if files.get("resume") else None,
                    photo = files.get("photo").filename if files.get("photo") else None,
                    certs = files.get("certs").filename if files.get("certs") else None,
                    createdAt= self.current_dt,
                    updatedAt= self.current_dt,
            ),
                    service_agreement= CAServiceAgreement(
                    engagement_type= form.get("engagement_type", None) ,
                    rate_itr_individual= form.get("rate_itr_individual", None) ,
                    rate_itr_business= form.get("rate_itr_business", None) ,
                    rate_consultation= form.get("rate_consultation", None) ,
                    rate_gsts= form.get("rate_gst", None) ,
                    revenue_share= form.get("revenue_share", None) ,
                    payment_terms= form.get("payment_terms", None) ,
                    max_clients= form.get("max_clients", None) ,
                    response_time= form.get("response_time", None) ,
                    work_hours_from= form.get("work_hours_from", None) ,
                    work_hours_to= form.get("work_hours_to", None) ,
                    working_day= form.getlist("working_day") ,
                    bank_account_name= form.get("bank_account_name", None) ,
                    bank_name= form.get("bank_name", None) ,
                    bank_ifsc= form.get("bank_ifsc", None) ,
                    createdAt= self.current_dt,
                    updatedAt= self.current_dt,
                ),
                    actives_status= ActiveStatus(
                    is_approved= False,
                    is_active = True,
                    last_active_datetime= self.current_dt
                )
        )
        
        self.mongodb_client.insert_one_item_in_collection(self.db_name, self.ca_collection,
                                                    update_ca_info.model_dump())
        
    def fetch_ca_list_from_database(self):
        ca_list = self.mongodb_client.fetch_all_records_from_collection(self.db_name, self.ca_collection)
        return ca_list