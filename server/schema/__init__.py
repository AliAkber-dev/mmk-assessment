from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from server import db
from server.models import Account,PhoneNumber
class AccountSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Account
        include_relationships = True
        load_instance = True
        sqla_session = db.session

class PhoneNumberSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = PhoneNumber
        include_relationships = True
        load_instance = True
        include_fk = True
        sqla_session = db.session