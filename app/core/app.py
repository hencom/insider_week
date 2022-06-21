from flask_openapi3 import OpenAPI, Info

info = Info(title='Insider week', version='1.0.0')
app = OpenAPI(__name__, doc_prefix='/insider_week/openapi', info=info)



