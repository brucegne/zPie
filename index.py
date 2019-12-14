from flask import Flask, render_template, Response, redirect, url_for, escape, request, make_response, Response, session, abort, g, flash, _app_ctx_stack, send_file, jsonify
from bson import ObjectId
import json, os, redis
import time

r=redis.Redis(host='angler.redistogo.com',password='0566827014ab8c2c76bcad1ab98239a7',port=9285)

REDIS_URL="redis://redistogo:0566827014ab8c2c76bcad1ab98239a7@angler.redistogo.com:9285/"

app = Flask(__name__)

# @app.route('/', defaults={'path': ''})

@app.route('/', methods=['GET', 'POST'])
def ang_temp():
    prms={}
    resp = make_response( render_template('ang.html',**prms), 200 )
    return resp

@app.route('/addrec', methods=['GET'])
def add_rec():
    prms={
        "created": str(int(time.time())),
        "name": "",
        "age": "",
        "married": ""        
    }
    resp = make_response( render_template('addtest.html',**prms), 200 )
    return resp

@app.route('/modrec', methods=['GET'])
def mod_data():
    r=redis.Redis(host='angler.redistogo.com',password='0566827014ab8c2c76bcad1ab98239a7',port=9285)
    kv = request.args.get('kv')
    kv = str(kv)
    data = r.hget('Contacts',kv)
    row = json.dumps(data)
#    row = data
    prms={
        "created": row['created'],
        "name": row['name'],
        "age": row['age'],
        "married": row['married']
    }
    resp = make_response( render_template('addtest.html',**prms), 200 )
    return resp
        
@app.route('/adddata', methods=['POST'])
def add_data():
    r=redis.Redis(host='angler.redistogo.com',password='0566827014ab8c2c76bcad1ab98239a7',port=9285)
    kv = request.form['created']
    kv=str(kv)
#    row=r.hget('Contacts',kv)
#    row = row.decode('utf-8')
#    row=json.loads(row)
    recOut={}
    recOut['created'] = row['created']
    recOut['name'] = rowform['name']
    recOut['age'] = rowform['age']
    recOut['married']= 'Not Set'
    data = json.dumps(recOut)
    r.hset('Contacts',kv,data)
    return redirect("/", code=302)

@app.route('/deldata', methods=['GET'])
def del_data():
    kv=request.args.get('kv')
    r=redis.Redis(host='angler.redistogo.com',password='0566827014ab8c2c76bcad1ab98239a7',port=9285)
    res=r.hdel('Contacts',kv)
    return redirect("/", code=302)
           
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
    return(retVal) 
    
@app.route('/<path:path>')
def catch_all(path):
    return Response("<h1>Flask on Now</h1><p>You visited: /%s</p>" % (path), mimetype="text/html")
