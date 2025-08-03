from flask import request, session, flash, render_template, redirect, url_for
import requests
from date_time_conversion import calculate_time_difference
import time
import sys
import config

def infochk():
    headers1 = {
                  "X-CSRF-ZOSMF-HEADER": "dummy",
                  "Accept": "application/json",
                  "Content-Type": "text/plain"
               }
    headers2 = {
                  "X-CSRF-ZOSMF-HEADER": "dummy",
                  "Accept": "application/json",
                  "Content-Type": "application/json"
               }
    
    user = session.get('user')
    pwd = session.get('pwd')
    auth = (user, pwd)
    err=None
    if request.method=="POST":
       pname=request.form.get("pname").strip()
       
       findadd=request.form.get("findadd")
       if findadd != "find":
            dob=request.form.get("dob")
            sdtim=request.form.get("sdtim")

       headers3 = {
                  "X-CSRF-ZOSMF-HEADER": "dummy",
                  "Accept": "application/json",
                  "X-IBM-JCL-Symbol-PNAME": pname.upper()
               }

       if findadd=="find":
            iurl = "/restjobs/jobs"  
            url=config.burl+iurl
            indd="//'"+user+".JCLLIB(REXXDB2F)'"
            data = {
                        "file": f"{indd}"
                    }
            resfind = requests.put(url, json=data, headers=headers3, auth=auth, verify=False)
            if resfind.status_code > 204:
                error_reason=resfind.reason
                status_code=resfind.status_code
                err_desc=f"INFOCHK ERROR: REASON: {error_reason} WITH RETURN-CODE: {status_code}"
                return redirect(url_for("mytools_route", error_reason=error_reason, status_code=status_code, err_desc=err_desc)) 
            time.sleep(4)
            iurl="/restfiles/ds/"+user+".ADDOUT"
            url=config.burl+iurl
            resfind = requests.get(url, headers=headers1, auth=auth, verify=False)
            if resfind.status_code > 204:
                error_reason=resfind.reason
                status_code=resfind.status_code
                err_desc=f"INFOCHK ERROR: REASON: {error_reason} WITH RETURN-CODE: {status_code}"
                return redirect(url_for("mytools_route", error_reason=error_reason, status_code=status_code, err_desc=err_desc))
            time.sleep(4)
            db2_dob=resfind.text.strip()
            if db2_dob =='DOB':
                err="OOPS! DETAILS NOT FOUND IN DATABASE, PLEASE ADD YOUR DETAILS WITH ADD BUTTON"
                err1=''
                err=err+"<br>"+err1
                flash(err,category="danger")
                return render_template("infochk.html", pname=pname, dob="", disena="")
            else:
                err="DETAILS FETCHED SUCCESSFULLY!"
                err1=''
                err=err+"<br>"+err1
                flash(err,category="success")
                return render_template("infochk.html", pname=pname, dob=db2_dob, disena="disabled")         
          
       else:
            time_diff=0
            if sdtim:
                time_diff = calculate_time_difference(sdtim[0:10], sdtim[-5:])
                if time_diff == -1:
                    err="ERROR: THE SCHEDULED DATE/TIME IN PAST"
                    err1=''
                    err=err+"<br>"+err1
                    flash(err,category="danger")
                    return render_template("infochk.html", pname=pname, dob=dob)
            
            mf_data=(pname+"\n"+dob+"\n"+str(time_diff))
            mf_data=mf_data.upper()
       
            iurl=f"/restfiles/ds/{user}.ADDDATA"
            url=config.burl+iurl
            resadd = requests.put(url, data=mf_data, headers=headers1, auth=auth, verify=False)
            if resadd.status_code > 204:
                error_reason=resadd.json()
                error_reason=error_reason['message']
                status_code=resadd.status_code
                err_desc=f"INFOCHK ERROR: REASON: {error_reason} WITH RETURN-CODE: {status_code}"
                return redirect(url_for("mytools_route", error_reason=error_reason, status_code=status_code, err_desc=err_desc))
            
            time.sleep(1)
            iurl = "/restjobs/jobs"
            url=config.burl+iurl
            indd="//'"+user+".JCLLIB(CBLDB2A)'"
            data = {
                        "file": f"{indd}"
                    }
            resadd = requests.put(url, json=data, headers=headers2, auth=auth, verify=False)
            if resadd.status_code > 204:
                error_reason=resadd.json()
                error_reason=error_reason['message']
                status_code=resadd.status_code
                err_desc=f"INFOCHK ERROR: REASON: {error_reason} WITH RETURN-CODE: {status_code}"
                return redirect(url_for("mytools_route", error_reason=error_reason, status_code=status_code, err_desc=err_desc))
            time.sleep(2)
            if time_diff > 0:
                job_data=resadd.json()
                jid = job_data["jobid"]
                jnm = job_data["jobname"]
                sucess_message=f"THE JOB SCHEDULED TO ADD DOB WITH JOB DETAILS {jnm}({jid})"
                return redirect(url_for("mytools_route", jnm=jnm, jid=jid, sucess_message=sucess_message))

            time.sleep(8)
            iurl = "/restjobs/jobs?owner="f"{user}""&prefix=CBLDB2*"
            url=config.burl+iurl
            resadd = requests.get(url, headers=headers2, auth=auth, verify=False)
            if resadd.status_code > 204:
                error_reason=resadd.json()
                error_reason=error_reason['message']
                status_code=resadd.status_code
                err_desc=f"INFOCHK ERROR: REASON: {error_reason} WITH RETURN-CODE: {status_code}"
                return redirect(url_for("mytools_route", error_reason=error_reason, status_code=status_code, err_desc=err_desc))
            
            job_data=resadd.json()
            job_data=job_data[0]
            retcode=job_data["retcode"]
            if int(retcode[3:7]) <= 4:
                jid = job_data["jobid"]
                jnm = job_data["jobname"]
                sucess_message=f"THE DATE OF BIRTH ADDED FOR {pname} WITH JOB DETAILS {jnm}({jid})"
                return redirect(url_for("mytools_route", jnm=jnm, jid=jid, sucess_message=sucess_message))
            else:
                jid = job_data["jobid"]
                jnm = job_data["jobname"]
                error_reason=f"{jnm}({jid})" 
                status_code=retcode
                err_desc=f"INFOCHK ERROR: REASON: {error_reason} WITH RETURN-CODE: {status_code}"
                return redirect(url_for("mytools_route", error_reason=error_reason, status_code=status_code, err_desc=err_desc))

    else:

       return render_template("infochk.html", disena="disabled")

