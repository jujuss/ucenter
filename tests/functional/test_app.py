# encoding: utf-8

import requests


URI = "http://localhost:8080"


def test_register_no_body():
    url = "%s/register" % URI
    resp = requests.post(url, json={
    })
    assert resp.status_code == 400
    resp_body = resp.json()
    assert resp_body["code"] == 1



def test_register_password_not_match():
    url = "%s/register" % URI
    resp = requests.post(url, json={
        "email": "notice@vipshop.com",
        "password": "notice",
        "password_repeat": "notice1",
        "nick_name": u"通知中心",
    })
    assert resp.status_code == 400
    resp_body = resp.json()
    assert resp_body["code"] == 4


def test_register_success():
    url = "%s/register" % URI
    resp = requests.post(url, json={
        "email": "notice@vipshop.com",
        "password": "notice",
        "password_repeat": "notice",
        "nick_name": u"通知中心",
    })
    assert resp.status_code == 200
    resp_body = resp.json()
    assert resp_body["result"] == "success"
