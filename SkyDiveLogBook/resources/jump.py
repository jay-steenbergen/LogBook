from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.jump import jumpModel

class Jump(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('number', 
            required=True,
            help="This field cannot be empty!"
        )
    parser.add_argument('dropZone', 
            type=str,
            required=True,
            help="This field cannot be empty!"
        )
    parser.add_argument('logs_id', 
            type=str,
            required=True,
            help="Every jump need a log id"
        )

    @jwt_required()
    def get(self,number):
        jump = jumpModel.find_by_number(number)
        if jump:
            return jump.json()       
        return {"message": "Jump was not found"}, 404

    def post(self,number):
        jump = jumpModel.find_by_number(number)
        if jump:
            return {'message': "Jump '{}' already exists.".format(number)}, 400
               
        data = Jump.parser.parse_args()

        jump = jumpModel(number, data['dropZone'], data['logs_id'])

        try:
            jump.save_to_db()
        except:
            return {"message": "An error occured inserting the jump."}, 500 #internal server error

        return jump.json(), 201

    def delete(self,number):        
        jump = jumpModel.find_by_number(number)
        if jump:
            jump.delete_from_db()
        return {'message': 'Jump deleted'}

    def put(self,number):        
        data = Jump.parser.parse_args()

        jump = jumpModel.find_by_number(number)

        if jump is None:
            jump = jumpModel(number, data['dropZone'], data['logs_id'])
        else:
            jump.dropZone = data['dropZone']

        jump.save_to_db()
        return jump.json()


class JumpList(Resource):
    def get(self):
        return {'jumps': [jump.json() for jump in jumpModel.query.all()]}