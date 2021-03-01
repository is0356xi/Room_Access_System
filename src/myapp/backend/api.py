from flask import Blueprint
from flask_restful import Api, Resource
import access_info

api_bp = Blueprint('api', __name__, url_prefix='/api')

class Test(Resource):
    def get(self):
        return [
                { 'x': 100, 'y': 182, 'value': .9 },
                { 'x': 120, 'y': 135, 'value': .9 },
                { 'x': 144, 'y': 276, 'value': .9 },
                { 'x': 196, 'y': 272, 'value': .9 },
                { 'x': 121, 'y': 240, 'value': .9 },
                { 'x': 150, 'y': 135, 'value': .9 },
                { 'x': 92, 'y': 135, 'value': .9 },
                { 'x': 96, 'y': 105, 'value': .9 },
                { 'x': 120, 'y': 132, 'value': .9 },
                { 'x': 140, 'y': 157, 'value': .9 },

                { 'x': 80, 'y': 144, 'value': .8 },
                { 'x': 127, 'y': 132, 'value': .8 },
                { 'x': 95, 'y': 148, 'value': .8 },
                { 'x': 94, 'y': 155, 'value': .8 },
                { 'x': 165, 'y': 140, 'value': .8 },
                { 'x': 125, 'y': 147, 'value': .8 },
                { 'x': 110, 'y': 265, 'value': .8 },
                { 'x': 135, 'y': 240, 'value': .8 },
                { 'x': 274, 'y': 376, 'value': .8 },
                { 'x': 245, 'y': 365, 'value': .8 },
                { 'x': 265, 'y': 365, 'value': .8 }
        ]

class Access(Resource):
    def get(self):
        access = access_info.access()
        user_list = access.access_user_search()

        print(user_list)

        return user_list

api = Api(api_bp)
api.add_resource(Test, '/test')
api.add_resource(Access, '/access')