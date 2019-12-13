from app.database import db

class Groupmsg(db.Model):
    __tablename__ = 'msg'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userid = db.Column(db.Integer, db.ForeignKey('user.id'))
    groupName = db.Column(db.String(80), unique=True, nullable=False)
    groupMember_actualname = db.Column(db.String(80), unique=True, nullable=False)
    groupMember_Nickname = db.Column(db.String(80), unique=True, nullable=True)
    message = db.Column(db.TEXT, nullable=False)
    msgtime = db.Column(db.DATETIME, nullable=False)



    def __init__(self, groupName, groupMember_actualname, groupMember_Nickname, message, msgtime):
        self.groupMember_actualname = groupMember_actualname
        self.groupName = groupName
        self.groupMember_Nickname = groupMember_Nickname
        self.message = message
        self.msgtime = msgtime

    def __repr__(self):
        return '<msg %r>' % self.message

class Users(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    phonenum = db.Column(db.String(11), unique=True, nullable=False)
    password = db.Column(db.TEXT, nullable=False)
    msgrefer = db.relationship('Groupmsg', backref='user')

    def __init__(self, phonenum,password):
        self.phonenum = phonenum
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.phonenum






