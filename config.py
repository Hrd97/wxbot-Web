import os
base_dir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI= 'sqlite:////' + os.path.join(base_dir, 'test.db')
# 设置每次请求结束后会自动提交数据库中的改动
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
SQLALCHEMY_TRACK_MODIFICATIONS = True
# 查询时会显示原始SQL语句
SQLALCHEMY_ECHO = True

