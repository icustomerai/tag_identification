from api.router import tag_identification
from fastapi import FastAPI
# from entity_matching.full_system.run import lambda_handler
from mangum import Mangum


app = FastAPI(title='icustomer internal apis')


app.include_router(tag_identification.router,responses={404: {"description": "Not found"}},
                    tags=["tag identification"])

handler =Mangum(app)