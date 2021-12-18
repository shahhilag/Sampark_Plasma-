from flask import Flask, render_template, redirect, url_for, request, send_from_directory
import random
import string
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import timedelta, date, datetime
from validation import *
import os

app = Flask(__name__)
app.secret_key = "@@@12345@@@"
app.config['UPLOAD_FOLDER'] = '/home/site/wwwroot/appdata/prescription'

url = "mongodb+srv://Plasma:Plasma1234#@cluster0.53ruc.mongodb.net/plasmadetails?retryWrites=true&w=majority"
client = "mongodb+srv://contactdb:hrithik1234very@cluster0.e4fl5.mongodb.net/details?retryWrites=true&w=majority"
tcluster = MongoClient(client)
cluster = MongoClient(url)
db = cluster["plasmadetails"]
pcollection = db['Patient']
dcollection = db['Donor']
db1 = tcluster['details']
vol = db1['vol']
admin = db1['contact']

dmax = date.today() - timedelta(14)
dmin = date.today() - timedelta(104)

now = datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
d, t = dt_string.split(' ')


@app.route('/')
def consent():
    return render_template('consent.html')


@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/patient', methods=['GET', 'POST'])
def patient():
    if request.method == 'POST':
        data = request.form
        name = data['user_name'].upper()

        mob = data['user_mobile']
        email = data['email'].upper()
        age = data['age']
        gender = request.form.get('gender').upper()
        state = request.form.get('state')
        state.upper()
        city = request.form.get('city')
        city.upper()
        blood = request.form.get('blood-group')
        assign = "NO"
        modified = "NO"
        file = request.files['profile']
        msg = file.filename
        fmsg = msg.split('.')
        l = len(fmsg)
        appid = ''.join(random.sample(string.ascii_uppercase, 8))
        if (not checkAge(age) or not checkEmail(email) or not checkPhone(mob) or not checkName(name) or (fmsg[l - 1] not in ("jpg", "png", "jpeg"))):
            err = "Please fill all details correctly!"
            if(fmsg[l - 1] not in ("jpg", "png", "jpeg")):
                err = "Please Upload only jpeg, jpg or png"
            return render_template('patient.html', err=err)
            # return redirect()
        a = pcollection.find_one({"name": name, "mob": mob, "city": city, "blood": blood, "state": state})

        if a != None:
            if a['assign'] != "NO":
                objid = a['assign']
                data = dcollection.find_one({'_id': objid})

                m = "Donor is already assigned to you"
                return render_template("ddetails.html", allCon=data, m=m)
            else:

                return render_template("passign.html", appid=a['appid'], aid=a['_id'], blood=blood)

        c = dcollection.find_one({"city": city, "blood": blood})

        s = dcollection.find_one({"state": state, "blood": blood})
        if c != None:
            if (c['assign'] != "NO"):
                if s != None:
                    if (s['assign'] != "NO"):
                        now = datetime.now() + timedelta(hours=5)
                        now = now + timedelta(minutes=30)
                        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                        d, t = dt_string.split(' ')
                        pcollection.insert_one(
                            {"name": name, "mob": mob, "email": email, "age": age, 'gender': gender, "city": city,
                             'state': state, 'blood': blood, 'assign': assign, "appid": appid, "modified": modified,
                             "rdate": d})
                        a = pcollection.find_one(
                            {"name": name, "mob": mob, "email": email, "age": age, 'gender': gender, "city": city,
                             'state': state, 'blood': blood, 'assign': assign, "appid": appid})
                        path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                        file.save(path)
                        os.rename("/home/site/wwwroot/appdata/prescription/" + file.filename, "/home/site/wwwroot/appdata/prescription/" + str(a['appid']) + "." + fmsg[l - 1])
                        return render_template("passign.html", appid=a['appid'], aid=a['_id'], blood=blood)
                    else:
                        now = datetime.now() + timedelta(hours=5)
                        now = now + timedelta(minutes=30)
                        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                        d, t = dt_string.split(' ')
                        assign = s['_id']
                        pcollection.insert_one(
                            {"name": name, "mob": mob, "email": email, "age": age, 'gender': gender, "city": city,
                             'state': state, 'blood': blood, 'assign': assign, "appid": appid, "modified": modified,
                             "rdate": d})

                        tassign = pcollection.find_one(
                            {"name": name, "mob": mob, "email": email, "age": age, 'gender': gender, "city": city,
                             'state': state, 'blood': blood, 'assign': assign})

                        assign = tassign['_id']
                        s['assign'] = assign
                        dcollection.delete_one({"state": state, "blood": blood, "_id": s['_id']})
                        dcollection.insert_one(s)
                        path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                        file.save(path)
                        os.rename("/home/site/wwwroot/appdata/prescription/" + file.filename, "/home/site/wwwroot/appdata/prescription/" + str(tassign['appid']) + "." + fmsg[l - 1])
                        return redirect(url_for('sdonordetails', state=state, blood=blood, did=assign))
                else:
                    now = datetime.now() + timedelta(hours=5)
                    now = now + timedelta(minutes=30)
                    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                    d, t = dt_string.split(' ')
                    pcollection.insert_one(
                        {"name": name, "mob": mob, "email": email, "age": age, 'gender': gender, "city": city,
                         'state': state, 'blood': blood, 'assign': assign, "appid": appid, "modified": modified,
                         "rdate": d})
                    a = pcollection.find_one(
                        {"name": name, "mob": mob, "email": email, "age": age, 'gender': gender, "city": city,
                         'state': state, 'blood': blood, 'assign': assign, "appid": appid})
                    path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                    file.save(path)
                    os.rename("/home/site/wwwroot/appdata/prescription/" + file.filename, "/home/site/wwwroot/appdata/prescription/" + str(a['appid']) + "." + fmsg[l - 1])
                    return render_template("passign.html", appid=a['appid'], aid=a['_id'], blood=blood)

            assign = c['_id']
            now = datetime.now() + timedelta(hours=5)
            now = now + timedelta(minutes=30)
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            d, t = dt_string.split(' ')
            pcollection.insert_one(
                {"name": name, "mob": mob, "email": email, "age": age, 'gender': gender, "city": city, 'state': state,
                 'blood': blood, 'assign': assign, "appid": appid, "modified": modified, "rdate": d})

            tassign = pcollection.find_one(
                {"name": name, "mob": mob, "email": email, "age": age, 'gender': gender, "city": city, 'state': state,
                 'blood': blood, 'assign': assign})
            path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(path)
            os.rename("/home/site/wwwroot/appdata/prescription/" + file.filename, "/home/site/wwwroot/appdata/prescription/" + str(tassign['appid']) + "." + fmsg[l - 1])
            assign = tassign['_id']
            c['assign'] = assign
            dcollection.delete_one({"city": city, "blood": blood, "_id": c['_id']})
            dcollection.insert_one(c)

            return redirect(url_for('donordetails', city=city, blood=blood, did=assign))
        elif s != None:
            if (s['assign'] != "NO"):
                now = datetime.now() + timedelta(hours=5)
                now = now + timedelta(minutes=30)
                dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                d, t = dt_string.split(' ')
                pcollection.insert_one(
                    {"name": name, "mob": mob, "email": email, "age": age, 'gender': gender, "city": city,
                     'state': state, 'blood': blood, 'assign': assign, "appid": appid, "modified": modified,
                     "rdate": d})
                a = pcollection.find_one(
                    {"name": name, "mob": mob, "email": email, "age": age, 'gender': gender, "city": city,
                     'state': state, 'blood': blood, 'assign': assign, "appid": appid})
                path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(path)
                os.rename("/home/site/wwwroot/appdata/prescription/" + file.filename, "/home/site/wwwroot/appdata/prescription/" + str(a['appid']) + "." + fmsg[l - 1])
                return render_template("passign.html", appid=a['appid'], aid=a['_id'], blood=blood)
            assign = s['_id']
            now = datetime.now() + timedelta(hours=5)
            now = now + timedelta(minutes=30)
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            d, t = dt_string.split(' ')
            pcollection.insert_one(
                {"name": name, "mob": mob, "email": email, "age": age, 'gender': gender, "city": city, 'state': state,
                 'blood': blood, 'assign': assign, "appid": appid, "modified": modified, "rdate": d})
            tassign = pcollection.find_one(
                {"name": name, "mob": mob, "email": email, "age": age, 'gender': gender, "city": city, 'state': state,
                 'blood': blood, 'assign': assign})
            path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(path)
            os.rename("/home/site/wwwroot/appdata/prescription/" + file.filename, "/home/site/wwwroot/appdata/prescription/" + str(tassign['appid']) + "." + fmsg[l - 1])
            # os.rename("/home/site/wwwroot/appdata/prescription/" + file.filename, "/home/site/wwwroot/appdata/prescription/" + str(a['appid']) + "." + fmsg[l - 1])
            assign = tassign['_id']
            s['assign'] = assign
            dcollection.delete_one({"state": state, "blood": blood, "_id": s['_id']})
            dcollection.insert_one(s)

            return redirect(url_for('sdonordetails', state=state, blood=blood, did=assign))

        now = datetime.now() + timedelta(hours=5)
        now = now + timedelta(minutes=30)
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        d, t = dt_string.split(' ')
        pcollection.insert_one(
            {"name": name, "mob": mob, "email": email, "age": age, 'gender': gender, "city": city, 'state': state,
             'blood': blood, 'assign': assign, "appid": appid, "modified": modified, "rdate": d})
        a = pcollection.find_one(
            {"name": name, "mob": mob, "email": email, "age": age, 'gender': gender, "city": city,
             'state': state, 'blood': blood, 'assign': assign, "appid": appid})
        path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(path)
        os.rename("/home/site/wwwroot/appdata/prescription/" + file.filename, "/home/site/wwwroot/appdata/prescription/" + str(a['appid']) + "." + fmsg[l - 1])
        return render_template("passign.html", appid=a['appid'], aid=a['_id'], blood=blood)

    return render_template('patient.html')

@app.route('/donor', methods=['GET', 'POST'])
def donor():
    if request.method == 'POST':
        data = request.form
        name = data['user_name'].upper()
        mob = data['user_mobile']
        email = data['email'].upper()
        age = data['age']
        gender = request.form.get('gender')
        state = request.form.get('state')
        state.upper()
        city = request.form.get('city')
        city.upper()
        blood = request.form.get('blood-group')
        date = data['date']
        assign = "NO"
        suffer = data['suffer'].upper()
        appid = ''.join(random.sample(string.ascii_uppercase, 8))
        modified = "NO"
        if (not checkAge(age) or not checkEmail(email) or not checkPhone(mob) or not checkName(name) or suffer == "NO"):
            err = "Please fill all details correctly!"
            if (suffer == "NO"):
                err = "You are not eligible to donate as per medical norms!"
            return render_template('donor.html', dmin=dmin, dmax=dmax, err=err)
        a = dcollection.find_one({"name": name, "mob": mob, "city": city, "blood": blood, "state": state})
        if a != None:
            if a['assign'] != "NO":
                objid = a['assign']
                data = pcollection.find_one({'_id': objid})

                m = "Patient is already assigned to you"
                return render_template('donor.html', dmin=dmin, dmax=dmax)
            else:

                return render_template("dassign.html", appid=a['appid'], aid=a['_id'])

        c = pcollection.find_one({"city": city, "blood": blood})

        s = pcollection.find_one({"state": state, "blood": blood})
        if c != None:
            if c['assign'] != "NO":
                if s != None:
                    if s['assign'] != "NO":
                        dcollection.insert_one(
                            {"name": name, "mob": mob, "email": email, "age": age, 'gender': gender, "city": city,
                             'state': state, 'blood': blood, 'date': date, 'assign': assign, "appid": appid,
                             "modified": modified})
                        a = dcollection.find_one(
                            {"name": name, "mob": mob, "email": email, "age": age, 'gender': gender, "city": city,
                             "state": state, 'blood': blood, "date": date, "assign": assign, "appid": appid})
                        return render_template("dassign.html", appid=a['appid'], aid=a['_id'], blood=blood)
                    else:
                        assign = s['_id']
                        dcollection.insert_one(
                            {"name": name, "mob": mob, "email": email, "age": age, 'gender': gender, "city": city,
                             'state': state, 'blood': blood, 'date': date, 'assign': assign, "appid": appid,
                             "modified": modified})

                        tassign = dcollection.find_one(
                            {"name": name, "mob": mob, "email": email, "age": age, 'gender': gender, "city": city,
                             'state': state, 'blood': blood, 'date': date, 'assign': assign})

                        assign = tassign['_id']

                        s['assign'] = assign
                        pcollection.delete_one({"state": state, "blood": blood, "_id": s['_id']})
                        pcollection.insert_one(s)

                        return redirect(url_for('spatientdetails', state=state, blood=blood, did=assign))
                else:
                    now = datetime.now() + timedelta(hours=5)
                    now = now + timedelta(minutes=30)
                    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                    d, t = dt_string.split(' ')
                    dcollection.insert_one(
                        {"name": name, "mob": mob, "email": email, "age": age, 'gender': gender, "city": city,
                         'state': state, 'blood': blood, 'date': date, 'assign': assign, 'appid': appid,
                         "modified": modified, "rdate": d})
                    a = dcollection.find_one(
                        {"name": name, "mob": mob, "email": email, "age": age, 'gender': gender, "city": city,
                         "state": state, 'blood': blood, "date": date, "assign": assign, "appid": appid})
                    return render_template("dassign.html", appid=a['appid'], aid=a['_id'], blood=blood)

            assign = c['_id']
            dcollection.insert_one(
                {"name": name, "mob": mob, "email": email, "age": age, 'gender': gender, "city": city, 'state': state,
                 'blood': blood, 'date': date, 'assign': assign, 'appid': appid, "modified": modified})
            tassign = dcollection.find_one(
                {"name": name, "mob": mob, "email": email, "age": age, 'gender': gender, "city": city, 'state': state,
                 'blood': blood, 'date': date, 'assign': assign})
            assign = tassign['_id']
            c['assign'] = assign
            pcollection.delete_one({"city": city, "blood": blood, "_id": s['_id']})
            pcollection.insert_one(c)
            return redirect(url_for('patientdetails', city=city, blood=blood, did=assign))
        elif s != None:
            if s['assign'] != "NO":
                dcollection.insert_one(
                    {"name": name, "mob": mob, "email": email, "age": age, 'gender': gender, "city": city,
                     'state': state, 'blood': blood, 'date': date, 'assign': assign, 'appid': appid,
                     "modified": modified})
                a = dcollection.find_one(
                    {"name": name, "mob": mob, "email": email, "age": age, 'gender': gender, "city": city,
                     "state": state, 'blood': blood, "date": date, "assign": assign, "appid": appid})
                return render_template("dassign.html", appid=a['appid'], aid=a['_id'], blood=blood)
            assign = s['_id']
            dcollection.insert_one(
                {"name": name, "mob": mob, "email": email, "age": age, 'gender': gender, "city": city,
                 'state': state, 'blood': blood, 'date': date, 'assign': assign, 'appid': appid, "modified": modified})

            tassign = dcollection.find_one(
                {"name": name, "mob": mob, "email": email, "age": age, 'gender': gender, "city": city,
                 'state': state, 'blood': blood, 'date': date, 'assign': assign})

            assign = tassign['_id']
            s['assign'] = assign
            pcollection.delete_one({"state": state, "blood": blood, "_id": s['_id']})
            pcollection.insert_one(s)

            return redirect(url_for('spatientdetails', state=state, blood=blood, did=assign))

        dcollection.insert_one(
            {"name": name, "mob": mob, "email": email, "age": age, 'gender': gender, "city": city, "state": state,
             'blood': blood, "date": date, "assign": assign, "appid": appid, "modified": modified})
        a = dcollection.find_one(
            {"name": name, "mob": mob, "email": email, "age": age, 'gender': gender, "city": city,
             "state": state, 'blood': blood, "date": date, "assign": assign, "appid": appid})
        return render_template("dassign.html", appid=a['appid'], aid=a['_id'], blood=blood)
    return render_template('donor.html', dmin=dmin, dmax=dmax)


@app.route('/patientdetails/<string:city>/<string:blood>/<string:did>', methods=['GET', 'POST'])
def patientdetails(city, blood, did):
    doc = pcollection.find_one({"city": city, "blood": blood, 'assign': ObjectId(did)})
    f = dcollection.find_one({'_id': ObjectId(did)})
    if doc == None:
        return render_template("dassign.html")
    if f==None:
        return render_template("passign.html")
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    for i in files:
        fpath = os.path.join((app.config['UPLOAD_FOLDER']), str(i))
        ssp = str(i)
        spath = ssp[0:8]
        if spath == str(doc['appid']):
            break

    # ff=fpath[1:]
    return render_template("pdetails.html", allCon=doc, a=f['appid'], val= fpath)


@app.route('/spatientdetails/<string:state>/<string:blood>/<string:did>',methods=['GET','POST'])
def spatientdetails(state,blood,did):
    doc = pcollection.find_one({"state": state, "blood": blood, 'assign': ObjectId(did)})
    f = dcollection.find_one({'_id': ObjectId(did)})
    fpath = "no"
    if doc==None:
        return render_template("dassign.html")
    if f==None:
        return render_template("passign.html")
    files=os.listdir(app.config['UPLOAD_FOLDER'])
    for i in files:
        fpath = os.path.join((app.config['UPLOAD_FOLDER']), str(i))
        ssp = str(i)
        spath = ssp[0:8]
        if spath == str(doc['appid']):
            break

    return render_template("pdetails.html", allCon=doc, a=f['appid'], val= fpath)




@app.route("/home/site/wwwroot/appdata/prescription/<path:filename>")
def getimg(filename):
    return send_from_directory("/home/site/wwwroot/appdata/prescription",filename)


# return redirect(url_for("donor"))

@app.route('/donordetails/<string:city>/<string:blood>/<string:did>', methods=['GET', 'POST'])
def donordetails(city, blood, did):
    # if request.method== 'POST':

    allCon = dcollection.find_one({"city": city, "blood": blood, 'assign': ObjectId(did)})
    if allCon == None:
        return render_template("dassign.html")
    f = pcollection.find_one({'_id': ObjectId(did)})
    return render_template("ddetails.html", allCon=allCon, a=f['appid'])
    # return redirect(url_for("patient"))


@app.route('/sdonordetails/<string:state>/<string:blood>/<string:did>', methods=['GET', 'POST'])
def sdonordetails(state, blood, did):
    # if request.method== 'POST':

    allCon = dcollection.find_one({"state": state, "blood": blood, 'assign': ObjectId(did)})
    # files = os.listdir(Uplo)
    if allCon == None:
        return render_template("dassign.html")
    f = pcollection.find_one({'_id': ObjectId(did)})
    return render_template("ddetails.html", allCon=allCon, a=f['appid'])


# return redirect(url_for("patient"))


@app.route('/application', methods=['GET', 'POST'])
def application():
    if request.method == 'POST':
        data = request.form
        status = data['response'].upper()
        appid = data['aid'].upper()

        if status == "DONOR":
            a = dcollection.find_one({"appid": appid})

            if a != None:
                if a['assign'] == "NO":
                    message = "Sorry " + a['name'] + " No Patient is assigned to you till now having " + a[
                        'blood'] + " blood group in " + a['city']
                    message1 = "Please keep tracking your application every hour."
                    message2 = "We are trying our best to assign Plasma receiver to you as soon as possible."
                    return render_template("status.html", message=message, message1=message1, message2=message2)
                else:
                    aid = a['assign']
                    allCon = pcollection.find_one({"_id": aid})
                    files = os.listdir(app.config['UPLOAD_FOLDER'])
                    for i in files:
                        fpath = os.path.join((app.config['UPLOAD_FOLDER']), str(i))
                        # sspath = fpath.split(".")
                        ssp = str(i)
                        spath=ssp[0:8]
                        if spath == str(allCon['appid']):
                            break
                    return render_template("pdetails.html", allCon=allCon, a=a['appid'],val=fpath)
            else:
                message = "It seems you have not filled registration form till now."
                return render_template("status.html", message=message)
        else:
            a = pcollection.find_one({"appid": appid})
            if a != None:
                if a['assign'] == "NO":
                    message = "Sorry " + a['name'] + " No Donor is assigned to you till now having " + a[
                        'blood'] + " blood group in " + a['city']
                    message1 = "Please keep tracking your application every hour."
                    message2 = "We are trying our best to assign Donor for you as soon as possible."
                    return render_template("status.html", message=message, message1=message1, message2=message2)
                else:
                    aid = a['assign']
                    allCon = dcollection.find_one({"_id": aid})
                    return render_template("ddetails.html", allCon=allCon, a=a['appid'])
            else:
                message = "It seems you have not filled registration form till now."
                return render_template("status.html", message=message)
    return render_template("application.html")


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        data = request.form
        name = data['name']
        email = data['email']
        message = data['message']
        mob = data['mob']
        if (not checkName(name) or not checkEmail(email) or not checkPhone(mob)):
            err = "Please fill all the details correctly!"
            return render_template("contactus.html", err=err)
        assign = admin.find_one({"name": name, "email": email, "message": message, "mob": mob})
        if assign != None:
            mess = "Message already sent!"
            return render_template("contactus.html", mess=mess, name=name)
        admin.insert_one({"name": name, "email": email, "message": message, "mob": mob})
        mess = "Thankyou for contacting us, We will reach out you soon..."
        return render_template("contactus.html", mess=mess, name=name)

    return render_template("contactus.html")


@app.route('/team')
def team():
    return render_template("team.html")


@app.route('/volunteer', methods=['POST', 'GET'])
def volunteer():
    if request.method == 'POST':
        data = request.form
        name = data['user_name'].upper()
        mob = data['user_mobile']
        email = data['email'].upper()
        gender = request.form.get('gender')
        state = request.form.get('state')
        state.upper()
        city = request.form.get('city')
        city.upper()
        if (not checkName(name) or not checkPhone(mob) or not checkEmail(email) or not state or not city):
            err = "Something missing! Please check your form"
            return render_template("volunteer.html", err=err)
        assign = vol.find_one(
            {"name": name, "mob": mob, "email": email, "gender": gender, "state": state, "city": city})
        if assign != None:
            mess = "Message already sent!"
            return render_template("volunteer.html", mess=mess, name=name)
        vol.insert_one(
            {"name": name, "mob": mob, "email": email, "gender": gender.upper(), "state": state, "city": city})
        mess = "Thankyou for contacting us, We will reach out you soon..."
        return render_template("volunteer.html", mess=mess, name=name)

    return render_template("volunteer.html")


@app.route('/printDonor/<string:id>')
def donorPrint(id):
    now = datetime.now() + timedelta(hours=5)
    now = now + timedelta(minutes=30)
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    d, t = dt_string.split(' ')
    a = dcollection.find_one({'_id': ObjectId(id)})
    return render_template('print.html', name=a['name'], blood=a['blood'], city=a['city'], appid=a['appid'],
                           state=a['state'], dateP=d, timeP=t)


@app.route('/printPatient/<string:id>')
def patientPrint(id):
    now = datetime.now() + timedelta(hours=5)
    now = now + timedelta(minutes=30)
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    d, t = dt_string.split(' ')
    a = pcollection.find_one({'_id': ObjectId(id)})
    return render_template('print.html', name=a['name'], blood=a['blood'], city=a['city'], appid=a['appid'],
                           state=a['state'], dateP=d, timeP=t)

@app.route('/pnothelpful/<string:appid>')
def pnothelpful(appid):
    a = pcollection.find_one({'appid': appid})
    b = dcollection.find_one({'_id':a['assign']})
    pcollection.delete_one({'appid':appid})
    dcollection.delete_one({'_id': a['assign']})
    a['assign'] = "NO"
    a['modified'] = "Self"
    b['assign'] = "NO"
    b['modified'] = appid
    pcollection.insert_one(a)
    dcollection.insert_one(b)
    return render_template("thank.html",val="Donor",appid=appid)

@app.route('/dnothelpful/<string:appid>')
def dnothelpful(appid):
    a = dcollection.find_one({'appid': appid})
    b = pcollection.find_one({'_id':a['assign']})
    dcollection.delete_one({'appid':appid})
    pcollection.delete_one({'_id': a['assign']})
    a['assign'] = "NO"
    b['modified'] = appid
    b['assign'] = "NO"
    a['modified'] = "Self"
    pcollection.insert_one(b)
    dcollection.insert_one(a)
    return render_template("thank.html",val="Patient",appid=appid)


@app.route('/sponsors')
def sponsor():
    return render_template('sponsors.html')


@app.route('/adgjl')
def adgjl():
    return render_template('maintenance.html')


if __name__ == '__main__':
    app.run(debug=True)