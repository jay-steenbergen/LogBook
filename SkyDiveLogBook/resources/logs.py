from flask_restful import Resource
from models.logs import logsModel

class Logs(Resource):
    def get(self, name):
        log = logsModel.find_by_name(name)
        if log:
            return log.json()
        return {'message': 'Log not found'}, 404
    
    def post(self, name):
        if logsModel.find_by_name(name):
            return {'message': "A log with the name '{}' already exists.".format(name)}, 400

        log = logsModel(name)
        try:
            log.save_to_db()
        except:
            return{'message': 'An error occurred while creating the store.'}, 500

        return log.json(), 201

    def delete(self, name):
        log = logsModel.find_by_name(name)
        if log:
            log.delete_from_db()

        return {'message': 'Log deleted'}

class LogsList(Resource):

    def get(self):
        return {'logs': [log.json() for log in logsModel.query.all()]}