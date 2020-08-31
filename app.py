from flask import Flask,request,jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from datetime import datetime



from utils import auth,util



app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = 'secret'

bcrypt = Bcrypt(app)
jwt = JWTManager(app)

@app.route('/',methods=['GET','POST'])
def index():
    return '<h1>welcome to the ToDo List app </h2>'



@app.route('/users/register', methods=['POST'])
def register():
    print('here')
    name = request.args.get('username')
    email = request.args.get('email')
    password = request.args.get('password')
    password = bcrypt.generate_password_hash(password).decode('utf-8')
    resp = auth.signUP(email, name, password)
	
    result = {
		'name' : name,
		'email' : email,
		'password' : password
	}
    result['message'] = resp['message']
    return jsonify({'result' : result})
	



@app.route('/users/login', methods=['POST'])
def login():
    email = request.args.get('email')
    password = request.args.get('password')
    result = ""
    rv = auth.signIN(email)
    print(rv)
    if bcrypt.check_password_hash(rv[-1], password):
        access_token = create_access_token(identity = {'name': rv[2], 'email': rv[1]})
        result = jsonify(access_token=access_token), 200
    else:
        result = jsonify({"error":"Invalid username or password"})
    return result




@app.route('/user/addtask', methods=['PUT'])
@jwt_required
def add_task():
    task = request.args.get('task')
    current_user = get_jwt_identity()
    user_email=current_user['email']
    resp = util.addTask(user_email,task)
    return resp



@app.route('/user/gettask', methods=['GET'])
@jwt_required
def get_task():
    current_user = get_jwt_identity()
    user_email=current_user['email']
    resp = util.getTasks(user_email)
    return resp



@app.route('/user/updatetask',methods=['PATCH'])
@jwt_required
def update_task():
    ntask = request.args.get('newtask')
    id_oldtask = request.args.get('oldtaskid')
    current_user = get_jwt_identity()
    user_email=current_user['email']
    resp = util.updateTask(user_email,ntask,id_oldtask)
    return resp


@app.route('/user/deletetask',methods=['DELETE'])
@jwt_required
def delete_task():
    current_user = get_jwt_identity()
    user_email=current_user['email']
    task_id = request.args.get('taskid')
    resp = util.deleteTask(user_email,task_id)
    return resp


if __name__ == "__main__":
    util.run_sql()
    app.run(debug=True)