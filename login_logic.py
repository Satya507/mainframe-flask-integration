from flask import request, session, flash, render_template, redirect, url_for
import requests
import base64
import config

def login():
    err=None
    if request.method=="POST":
        user=request.form["user"]
        pwd=request.form["pwd"]
        session['pwd'] = pwd
        session['user'] = user
        headers = {
                    "X-CSRF-ZOSMF-HEADER": "dummy",
                    "Accept": "application/json",
                    "Authorization": f"Basic {base64.b64encode(f'{user}:{pwd}'.encode('utf-8')).decode('utf-8')}",
                    "Content-Type": "application/x-www-form-urlencoded"
                }
        url=config.burl + "/services/authenticate"
        response = requests.post(url, headers=headers, verify=False)
        if response.status_code != 200:
            err="INVALID USER/PASSWORD!"
            err1=""
            err=err+"<br>"+err1
            flash(err, category="danger")
            return render_template("login.html", user=user, pwd='')
        else:
           return redirect(url_for("mytools_route"))       
    else:
       return render_template("login.html")
