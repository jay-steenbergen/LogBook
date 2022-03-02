from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenicate, identity
from resources.user import UserRegister
from resources.jump import Jump, JumpList
from resources.logs import Logs, LogsList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///LogBook.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'jay'
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWT(app, authenicate, identity) # /auth

api.add_resource(Logs, '/log/<string:name>')
api.add_resource(Jump, '/jump/<int:number>')
api.add_resource(JumpList, '/jumps')
api.add_resource(LogsList, '/logs')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True) 