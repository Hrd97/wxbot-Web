import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from database import db
import config
from models import *

base_dir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config.from_object(config)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////test.sqlite'
'''
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + os.path.join(base_dir, 'test.db')
# 设置每次请求结束后会自动提交数据库中的改动
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# 查询时会显示原始SQL语句
app.config['SQLALCHEMY_ECHO'] = True
'''
db.init_app(app)
# wxbot.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:////' + os.path.join(base_dir, 'data.sqlite')
# wxbot.config["SQLALCHEMY_COMMIT_ON_TEARDOWN"] = True
# SQLALCHEMY_DATABASE_URI = 'sqlite:////test.db' #此为相对路径
# SQLALCHEMY_TRACK_MODIFICATIONS = False
#
# db = SQLAlchemy(app)
#
#db.create_all()
# user = Users("hj", "ghvhj")
# db.session.add(user)
# db.session.commit()
#
# import auth
#
# app.register_blueprint(auth.bp)
# app.register_blueprint(blog.bp)
@app.route('/')
def index():
    db.create_all() #根据模型创建表
    try:
        a = Users('aa', 'ii')
        db.session.add(a)
        db.session.commit()
    except Exception as e:
        print(e)
    else:
        return '1'
    finally:
        return '0'


if __name__ == '__main__':

    print("here")
    app.run(host="0.0.0.0", debug=True)
