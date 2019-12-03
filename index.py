from flask import Flask, render_template, Response, redirect, url_for, escape, request, make_response, Response, session, abort, g, flash, _app_ctx_stack, send_file, jsonify
import json, os, redis

r=redis.Redis(host='angler.redistogo.com',password='0566827014ab8c2c76bcad1ab98239a7',port=9285)

REDIS_URL="redis://redistogo:0566827014ab8c2c76bcad1ab98239a7@angler.redistogo.com:9285/"

# API keyE1hUaiUcOSiqc7
# BASE ID appOEjuG867PcJetu


app = Flask(__name__)

# @app.route('/', defaults={'path': ''})

@app.route('/', methods=['GET', 'POST'])
def daily__json():
#    return Response("It's the daily stuff")
    if request.method == 'GET':
        prms = {
            "user": "Bruce E. Gordon",
            "site": "http://appsmade4u.com"
        }
        resp = make_response( render_template('index.html',**prms), 200 )
        return resp

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
          rowOut = {}
          rowOut['name'] = row['name']
          rowOut['age'] = row['age']
          basisOut.append(rowOut)
      basisArray['records'] = basisOut
#      retVal = "%s(%s)" % (callback,json.dumps(basisArray))
      retVal = json.dumps(basisArray)
      return(retVal) 
    
@app.route('/<path:path>')
def catch_all(path):
    return Response("<h1>Flask on Now</h1><p>You visited: /%s</p>" % (path), mimetype="text/html")
