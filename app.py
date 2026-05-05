from flask import Flask
from src.routes.analytics_management_route import admin_analytics_bp
from src.routes.client_management_route import admin_client_bp
from src.routes.dashboard_route import admin_dashboard_bp
from src.routes.ca_management_route import admin_ca_bp
from src.routes.compliance_management_route import admin_compliance_bp
from src.routes.employee_management_route import admin_employee_bp
from src.routes.finance_management_route import admin_finance_bp
from src.routes.support_management_route import admin_support_bp
# from src.routes.engineering_management_route
# from src.routes.marketing_management_route
# from src.routes.product_management_route
# from src.routes.sales_management_route
from src.routes.authentication_route import authentication_bp


app = Flask(__name__)
app.secret_key = "secret_key"

app.register_blueprint(admin_dashboard_bp)
app.register_blueprint(admin_analytics_bp)
app.register_blueprint(admin_client_bp)
app.register_blueprint(admin_ca_bp)
app.register_blueprint(admin_compliance_bp)
app.register_blueprint(admin_employee_bp)
app.register_blueprint(admin_finance_bp)
app.register_blueprint(admin_support_bp)
app.register_blueprint(authentication_bp)
# app.register_blueprint()
# app.register_blueprint()
# app.register_blueprint()

if __name__ == "__main__":
    app.run(debug=True)