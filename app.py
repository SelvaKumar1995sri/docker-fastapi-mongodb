import pymongo
from flask import Flask,  request
from flask_restful import Resource, Api


def get_db():
    client = pymongo.MongoClient(host='user_mongodb',
                         port=27017, 
                         username='username', 
                         password='pass',
                        authSource="admin")
    db = client["user_db"]
    return db


app=Flask(__name__)

api = Api(app)

def auth_api(func):
    def wrapper(*args,**kwargs):
        print("started")
        resp=func(*args,**kwargs)
        print("stoped")
        return resp
    return wrapper

class User(Resource):

    @auth_api
    def get(self):
        return {"message": "Hello World"}

    @auth_api
    def post(self):
        try:
            db=get_db()
            x= db.user_db.find({},{"_id":0})
            return [i for i in x]      
        except Exception as e:
            print("error on get_stu_details :" +str(e))

    @auth_api
    def post(self):
        try:
            db=get_db()
            stu=request.get_json()
            print(stu)
            db.user_db.insert_one(stu)
            return "Successfully added"
        except Exception as e:
            print("error on get_stu_details :" +str(e))

    @auth_api
    def delete():
        try:
            db=get_db()
            Rno = request.get_json()
            db.user_db.delete_one(Rno)
            return "deleted successfully"
        except Exception as e:
            print("error"+str(e))

    @auth_api
    def put():
        try:
            db=get_db()
            Rno = request.args.get("Rno")
            data=request.get_json()
            db.user_db.find_one_and_update({"Rno":Rno},{"$set":data})
            return "success"
        except Exception as e:
            print("error on updation :" +str(e))

api.add_resource(User, '/')


if __name__=='__main__':
    app.run(debug=True)
