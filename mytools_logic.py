from flask import request, session, flash, render_template, redirect, url_for
import requests

def mytools():
    err=None
    user = session.get('user')
    pwd = session.get('pwd')
    if request.method=="POST":
        tool=request.form["tool_name"]
        if tool.strip()=="":
            err="INVALID SELECTION!"
            err1="PLEASE SELECT A TOOL"
            err=err+"<br>"+err1
            flash(err, category="danger")
            return render_template("mytools.html", op=tool)
        if tool.strip()=="infochk":
            return redirect(url_for("infochk_route"))
        else:
            # return redirect(url_for("pftp_route"))
            return render_template("mytools.html")
    else:
        error_reason=request.args.get("error_reason")
        status_code=request.args.get("status_code")
        err_desc=request.args.get("err_desc")
        jid=request.args.get("jid")
        jnm=request.args.get("jnm")
        sucess_message=request.args.get("sucess_message")
        if error_reason!=None and status_code!=None:
            err=err_desc
            err1=""
            err=err+"<br>"+err1
            if "ERROR" in err_desc:
               flash(err, category="danger")
               return redirect(url_for("mytools_route"))
        elif sucess_message!=None:
            flash(sucess_message, category="success") 
            return redirect(url_for("mytools_route"))
        else:
            return render_template("mytools.html")