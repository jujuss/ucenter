# encoding: utf-8

from flask import Flask, request, jsonify

app = Flask(__name__)

users = dict()  # email: user

def make_response(status_code, data):
    resp = jsonify(data)
    resp.status_code = status_code
    return resp


@app.route("/register", methods=["POST"])
def register():
    body = request.get_json()
    if body is None:
        return make_response(400, {"err_msg": "no body"})

    # check password
    password = body.get("password", "")
    password_repeat = body.get("password_repeat", "")
    if password == "":
        return make_response(400, {"err_msg": "no password"})
    elif password != password_repeat:
        return make_response(400, {"err_msg": "two passwords doesn't match"})

    # TODO: check email syntax
    email = body.get("email")
    if email is None or email == "":
        return make_response(400, {"err_msg": "email can not be empty"})
    nick_name = body.get("nick_name", "")

    if users.get(email) is not None:
        return make_response(400, {"err_msg": "email has registered"})

    users[email] = {
        "nick_name": nick_name,
        "password": password,
    }
    return make_response(200, {"result": "success", "code": 0,"uses":users})

@app.route("/login", methods=["POST"])
def login():
    body = request.get_json()
    if body is None:
        return make_response(400, {"err_msg": "no body"})

    # TODO:check email
    email = body.get("email","")
    if users.get(email) is None:
        return make_response(400, {"err_msg": "email has not registered"})

    #TODO:check password
    password_check = body.get("password_check", "")
    if password_check == users[email]["password"]:
        return make_response(200, {"result": "success", "code": 0})
    elif password_check != users[email]["password"]:
        return make_response(400, {"err_msg": "passwords wrong"})

@app.route("/user",methods=["POST"])
def user():
    body = request.get_json()
    email = body.get("email", "")
    if email is None:
        return make_response(400, {"err_msg": "no email"})
    user = users[email]["nick_name"]
    return make_response(200,{"user":user})

@app.route("/edit",methods=["POST"])
def edit():
    body = request.get_json()
    if body is None:
        return make_response(400, {"err_msg": "no body"})
    email = body.get("email", "")
    new_nick_name = body.get("new_nick_name", "")
    if new_nick_name == "":
        return make_response(400, {"err_msg": "no new_nick_name"})

    users[email].update({"nick_name":new_nick_name})
    return make_response(200, {"user": users})

@app.route("/delete",methods=["POST"])
def delete():
    body = request.get_json()
    if body is None:
        return make_response(400, {"err_msg": "no body"})

    email = body.get("email","")
    del users[email]
    return make_response(200,{"result": "success", "code": 0})

def main():
    app.run(host="0.0.0.0", port=8080, debug=True)

if __name__ == "__main__":
    main()