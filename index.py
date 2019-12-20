from flask import Flask, render_template, Response, redirect, jsonify, url_for, escape, request, make_response, Response, session, abort, g, flash, _app_ctx_stack, send_file, jsonify
import bcrypt
import json, os, redis
import time

r=redis.Redis(host='angler.redistogo.com',password='0566827014ab8c2c76bcad1ab98239a7',port=9285)

REDIS_URL="redis://redistogo:0566827014ab8c2c76bcad1ab98239a7@angler.redistogo.com:9285/"

app = Flask(__name__)

# @app.route('/', defaults={'path': ''})

@app.route('/', methods=['GET', 'POST'])
def red_json():
    basisOut = []
    basisArray = {}
    r=redis.Redis(host='angler.redistogo.com',password='0566827014ab8c2c76bcad1ab98239a7',port=9285)
    rkeys=r.hkeys('Contacts')
    for kv in rkeys:
      kv=kv.decode('utf-8')
      row=r.hget('Contacts',kv)
      row = row.decode('utf-8')
      row=json.loads(row)
      rowOut = {}
      rowOut['created'] = row['created']
      rowOut['name'] = row['name']
      rowOut['age'] = row['age']
      try:
        rowOut['married'] = row['married']
      except:
        rowOut['married'] = "Not Set"
      basisOut.append(rowOut)
    basisArray['records'] = basisOut
    retVal = json.dumps(basisArray)
    resp = make_response( render_template('index.html',data=retVal), 200 )
    return(resp) 


@app.route('/register', methods=['GET','POST'])
def register():
    rs=redis.Redis(host='angler.redistogo.com',password='0566827014ab8c2c76bcad1ab98239a7',port=9285)
    username = b'brucegne@gmail.com'
    password = 'Ye110wsn0w'
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    rs.hset('Users',username.decode(),hashed)
    return str(hashed)

@app.route('/login', methods=['GET','POST'])
def check_login():
    rs=redis.Redis(host='angler.redistogo.com',password='0566827014ab8c2c76bcad1ab98239a7',port=9285)
    username = b'brucegne@gmail.com'
    password = 'Ye110wsn0w'
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    hashed = rs.hget('Users',username.decode())
    if bcrypt.checkpw(password.encode(), hashed):
      return('Verified')
    else:
      return('Failed')
  
@app.route('/about', methods=['GET', 'POST'])
def about_temp():
    prms={}
    resp = make_response( render_template('about.html',**prms), 200 )
    return resp


@app.route('/testpost', methods=['GET', 'POST'])
def test_post():
    name = request.args.get('name')
    print(name)
    return jsonify(request.json)
      
@app.route('/addrec', methods=['GET'])
def add_rec():
    prms={
        "created": str(int(time.time())),
        "name": "",
        "age": "",
        "married": "",
        "mode": "Add"
    }
    resp = make_response( render_template('addtest.html',remote=prms), 200 )
    return resp

@app.route('/modrec', methods=['GET'])
def mod_data():
    r=redis.Redis(host='angler.redistogo.com',password='0566827014ab8c2c76bcad1ab98239a7',port=9285)
    kv = request.args.get('kv')
    kv = str(kv)
    print(kv)
    data = r.hget('Contacts',kv)
    data = data.decode('utf-8')
    print(data)
    row = json.loads(data)
#    row = data
    rname = row['name']
    rcreated = row['created']
    prms={
        "created": row['created'],
        "name": row['name'],
        "age": row['age'],
        "married": row['married'],
        "mode": "Update"
    }
    print(prms)
    resp = make_response( render_template('addtest.html',remote=prms) )
    return resp
        
@app.route('/adddata', methods=['POST'])
def add_data():
    r=redis.Redis(host='angler.redistogo.com',password='0566827014ab8c2c76bcad1ab98239a7',port=9285)
    kv = request.form['created']
    kv=str(kv)
    recOut={}
    recOut['created'] = request.form['created']
    recOut['name'] = request.form['name']
    recOut['age'] = request.form['age']
    recOut['married']= request.form['married']
    data = json.dumps(recOut)
    print(data)
    r.hset('Contacts',kv,data)
    return redirect("/", code=302)

@app.route('/deldata', methods=['GET'])
def del_data():
    kv=request.args.get('kv')
    r=redis.Redis(host='angler.redistogo.com',password='0566827014ab8c2c76bcad1ab98239a7',port=9285)
    res=r.hdel('Contacts',kv)
    return redirect("/", code=302)

@app.route('/mnames')
def mob_json():
    nameOut = []
    nameArray = []
    r=redis.Redis(host='angler.redistogo.com',password='0566827014ab8c2c76bcad1ab98239a7',port=9285)
    rkeys=r.hkeys('Contacts')
    for kv in rkeys:
      kv=kv.decode('utf-8')
      row=r.hget('Contacts',kv)
      row = row.decode('utf-8')
      row=json.loads(row)
      nameOut.append(row['name'])
      nameArray.append(row['created'])
    data = "|".join(nameOut)
    return Response(data, status=201, mimetype='application/json')

@app.route('/json')
def red_json():
    basisOut = []
    basisArray = {}
    r=redis.Redis(host='angler.redistogo.com',password='0566827014ab8c2c76bcad1ab98239a7',port=9285)
    rkeys=r.hkeys('Contacts')
    for kv in rkeys:
      kv=kv.decode('utf-8')
      row=r.hget('Contacts',kv)
      row = row.decode('utf-8')
      row=json.loads(row)
      rowOut = {}
      rowOut['created'] = row['created']
      rowOut['name'] = row['name']
      rowOut['age'] = row['age']
      try:
        rowOut['married'] = row['married']
      except:
        rowOut['married'] = "Not Set"
      basisOut.append(rowOut)
    basisArray['records'] = basisOut
#      retVal = "%s(%s)" % (callback,json.dumps(basisArray))
    retVal = json.dumps(basisArray)
    print(retVal)
    return(retVal) 
    
@app.route('/<path:path>')
def catch_all(path):
    return Response("<h1>Flask on Now</h1><p>You visited: /%s</p>" % (path), mimetype="text/html")
