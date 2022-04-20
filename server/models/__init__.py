from server import db
class Account(db.Model):
    __tablename__ = "account"
    id=db.Column(db.Integer, primary_key= True)
    auth_id = db.Column(db.String(40))
    username = db.Column(db.String(30))
    def __init__(self, auth_id, username):
        self.auth_id = auth_id
        self.username = username

class PhoneNumber(db.Model):
    __tablename__ = "phone_number"
    id=db.Column(db.Integer, primary_key= True)
    number = db.Column(db.String(40))
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    account = db.relationship("Account",backref="phone_number")
    def __init__(self, number, account_id):
        self.number = number
        self.account_id = account_id