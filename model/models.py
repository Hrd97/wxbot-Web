from app import db

class msg(db.model):
    id = db.Column(db.Integer, primary_key=True)
    groupName = db.Column(db.String(80), unique=True, nullable=False)
    groupMember_actualname = db.Column(db.String(80), unique=True, nullable=False)
    groupMember_Nickname = db.Column(db.String(80), unique=True, nullable=True)
    message = db.Column(db.TEXT, nullable=False)
    msgtime = db.Column(db.TEXT, nullable=False)

    # def __repr__(self):
    #     return '<User %r>' % self.

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phonenum = db.column(db.String(12), unique=True, nullable=False)
    password = db.Column(db.TEXT, unique=True, nullable=False)

    # def __repr__(self):
    #     return '<User %r>' % self.phonenum






