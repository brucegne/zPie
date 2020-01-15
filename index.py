from flask import Flask, render_template, Response, redirect, jsonify, url_for, escape, request, make_response, Response, session, abort, g, flash, _app_ctx_stack, send_file, jsonify
from bson.json_util import dumps
from bson.objectid import ObjectId
import bcrypt
import json, os, redis
import time
from pymongo import MongoClient

r=redis.Redis(host='angler.redistogo.com',password='0566827014ab8c2c76bcad1ab98239a7',port=9285)

MONGO_URL="mongodb://brucegne:p2shiver@ds043368.mongolab.com:43368/demo?retryWrites=false"
REDIS_URL="redis://redistogo:0566827014ab8c2c76bcad1ab98239a7@angler.redistogo.com:9285/"

app = Flask(__name__)

client=MongoClient(MONGO_URL)

db = client.demo

"""
@app.route("/", methods=['POST'])
def insert_document():
    req_data = request.get_json()
    collection.insert_one(req_data).inserted_id
    return ('', 204)

@app.route('/')
def get():
    documents = collection.find()
    response = []
    for document in documents:
        document['_id'] = str(document['_id'])
        response.append(document)
    return json.dumps(response)

lim = int(request.args.get('limit', 10))
off = int(request.args.get('offset', 0))
results = db['ufo'].find().skip(off).limit(lim)
    
"""

def  prtDate(dTarg):
    d1 = time.localtime(dTarg)
    tOut = "%s/%s/%s" % ( d1[1],d1[2],d1[0] )
    return tOut

def  fmtDate(dTarg):
    d1 = time.localtime(dTarg)
    tOut = "%s-%s-%s" % ( d1[1],d1[2],d1[0] )
    return tOut

@app.route('/mdb', methods=['GET', 'POST'])
def index_json():
    coll = db.contacts
    cursor = coll.find()
    resp = make_response( render_template('index.html',data=cursor ), 200 )
    return(resp) 


@app.route('/', methods=['GET', 'POST'])
def indexxx_json():
    basisOut = []
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
    resp = make_response( render_template('index.html',data=basisOut ), 200 )
    return(resp) 

@app.route('/w3', methods=['GET'])
def w3():
    prms={}
    resp = make_response( render_template('w3.html',**prms), 200 )
    return resp
  
@app.route('/ang', methods=['GET'])
def ang():
    prms={}
    resp = make_response( render_template('ang.html',**prms), 200 )
    return resp
  
@app.route('/socks', methods=['GET'])
def sock_demo():
    prms={}
    resp = make_response( render_template('socket.html',**prms), 200 )
    return resp
  
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

@app.route('/angular', methods=['GET', 'POST'])
def angular_temp():
    prms={}
    resp = make_response( render_template('angular.html',**prms), 200 )
    return resp

@app.route('/testpost', methods=['GET', 'POST'])
def test_post():
    name = request.form['name']
    age = 18
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

@app.route('/postdata', methods=['POST'])
def post_data():
    r=redis.Redis(host='angler.redistogo.com',password='0566827014ab8c2c76bcad1ab98239a7',port=9285)
    kv = str(int(time.time()))
    kv=str(kv)
    recOut={}
    recOut['created'] = kv
    recOut['name'] = request.form['name']
    recOut['age'] = request.form['age']
    recOut['married']= request.form['married']
    data = json.dumps(recOut)
    print(data)
    r.hset('Contacts',kv,data)
    name = request.form['name']
    age = 18
    print(name)
    return jsonify('Saved')

  
@app.route('/deldata', methods=['GET'])
def del_data():
    kv=request.args.get('kv')
    r=redis.Redis(host='angler.redistogo.com',password='0566827014ab8c2c76bcad1ab98239a7',port=9285)
    res=r.hdel('Contacts',kv)
    return redirect("/", code=302)

@app.route('/mnames')
def mob_json():
    keyOut = []
    nameOut = []
    ageOut = []
    familyOut = []
    nameArray = []
    r=redis.Redis(host='angler.redistogo.com',password='0566827014ab8c2c76bcad1ab98239a7',port=9285)
    rkeys=r.hkeys('Contacts')
    for kv in rkeys:
      kv=kv.decode('utf-8')
      row=r.hget('Contacts',kv)
      row = row.decode('utf-8')
      row=json.loads(row)
      nameOut.append(row['name'])
      keyOut.append(row['created'])
      familyOut.append(row['married'])
      ageOut.append(row['age'])
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
    
@app.route('/mjson')
def mongo_json():
    basisOut = []
    basisArray = {}
    coll = db.contacts
    cursor = coll.find()
    for row in cursor:
      rowOut = {}
      rowOut['fname'] = row['fname']
      rowOut['lname'] = row['lname']
      rowOut['city'] = row['city']
      rowOut['address'] = row['address']
      rowOut['phone'] = row['phone']
      basisOut.append(rowOut)
    basisArray['records'] = basisOut
    retVal = json.dumps(basisArray)
    print(retVal)
    return(retVal) 

@app.route('/<path:path>')
def catch_all(path):
    return Response("<h1>Flask on Now</h1><p>You visited: /%s</p>" % (path), mimetype="text/html")




