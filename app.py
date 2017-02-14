# encoding: utf-8

import hashlib

from flask import Flask, request, jsonify

app = Flask(__name__)

# user model:
#   - email(string, primary key)
#   - nick_name(string)
#   - password(string)
users = dict()  # email: `User`
# login tokens:
#   - key: token
#   - value: email
tokens = dict()  # token: email


class User(object):
    def __init__(self, email, password, nick_name):
        self.email = email
        self.password = password
        self.nick_name = nick_name

    def dict(self):
        return {
            "email": self.email,
            "password": self.password,
            "nick_name": self.nick_name,
        }


def make_response(status_code, data):
    resp = jsonify(data)
    resp.status_code = status_code
    return resp


@app.route("/register", methods=["POST"])
# TODO: use make response decorator
def register():
    body = request.get_json()
    if not body:
        return make_response(400, {"code": 1, "err_msg": "no body"})

    # check password
    password = body.get("password", "")
    password_repeat = body.get("password_repeat", "")
    if password == "":
        return make_response(400, {"code": 2, "err_msg": "no password"})
    elif password != password_repeat:
        return make_response(400, {"code": 4, "err_msg": "two passwords doesn't match"})

    # TODO: check email syntax
    email = body.get("email")
    if email is None or email == "":
        return make_response(400, {"code": 3, "err_msg": "email can not be empty"})
    nick_name = body.get("nick_name", "")

    if users.get(email) is not None:
        return make_response(400, {"code": 5, "err_msg": "email has registered"})

    users[email] = User(email, password, nick_name)  # save user to db

    # genereate users data
    users_data = []
    for email in users:
        users_data.append(users[email].dict())
    return make_response(200, {"result": "success", "code": 0, "users": users_data})


@app.route("/login", methods=["POST"])
def login():
    body = request.get_json()
    if not body:
        return make_response(400, {"code": 1, "err_msg": "no body"})

    # TODO:check email syntax
    email = body.get("email", "")
    if email == "":
        return make_response(400, {"code": 3, "err_msg": "email is empty"})
    password = body.get("password")
    if password is None:
        return make_response(400, {"code": 2, "err_msg": "no given password"})

    user = users.get(email)  # simluate that query user from db
    if user is None:
        return make_response(400, {"code": 6, "err_msg": "user not found"})
    elif user.password != password:
        return make_response(400, {"code": 7, "err_msg": "invalid user or password"})
    else:
        token = hashlib.sha256(email + password).hexdigest()
        tokens[token] = email  # note: consider concurrency safe
        resp = make_response(200, {"result": "success", "code": 0})
        resp.set_cookie("token", token)  # reference: http://flask.pocoo.org/docs/0.12/quickstart/#cookies
        return resp


@app.route("/profile", methods=["GET"])
def profile():
    token = request.cookies.get("token")
    if token is None or token not in tokens:
        return make_response(400, {"code": 8, "err_msg": "need login first"})

    email = tokens[token]
    user = users[email]
    return make_response(200, {"result": "success", "email": user.email, "nick_name": user.nick_name})


@app.route("/logout", methods=["POST"])
def logout():
    token = request.cookies.get("token")
    if token is None or token not in tokens:
        return make_response(400, {"code": 8, "err_msg": "need login first"})

    # expire token
    resp = make_response(200, {"result": "success"})
    resp.set_cookie("token", "", expires=0)
    return resp


@app.route("/edit", methods=["PUT"])
def edit():
    token = request.cookies.get("token")
    if token is None or token not in tokens:
        return make_response(400, {"code": 8, "err_msg": "need login first"})

    email = tokens[token]
    body = request.get_json()
    new_nick_name = body.get("new_nick_name", "")
    if new_nick_name == "":
        return make_response(400, {"code": 9, "err_msg": "no new_nick_name"})

    users[email].nick_name = new_nick_name

    return make_response(200, {"user": users[email].nick_name})


@app.route("/delete", methods=["POST"])
def delete():
    body = request.get_json()
    if not body:
        return make_response(400, {"code": 1, "err_msg": "no body"})

    email = body.get("email", "")
    del users[email]
    return make_response(200, {"result": "success", "code": 0})


def main():
    app.run(host="0.0.0.0", port=8080, debug=False)

if __name__ == "__main__":
    main()
