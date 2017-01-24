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
    return make_response(200, {"result": "success", "code": 0})


def main():
    app.run(host="0.0.0.0", port=8080, debug=True)


if __name__ == "__main__":
    main()
