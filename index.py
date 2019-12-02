from flask import Flask, render_template, Response, redirect, url_for, escape, request, make_response, Response, session, abort, g, flash, _app_ctx_stack, send_file, jsonify
from flask_redis import FlaskRedis

REDIS_URL="redis://redistogo:0566827014ab8c2c76bcad1ab98239a7@angler.redistogo.com:9285/"
# API keyE1hUaiUcOSiqc7
# BASE ID appOEjuG867PcJetu
from airtable import airtable
at = airtable.Airtable('appOEjuG867PcJetu', keyE1hUaiUcOSiqc7')


app = Flask(__name__)
redis_client = FlaskRedis(app)


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

@app.route('/air')
def air_fetch():
    at.get('Family')
    for r in self.at.iterate(self.Family):
        print r
                       
@app.route('/<path:path>')
def catch_all(path):
    return Response("<h1>Flask on Now</h1><p>You visited: /%s</p>" % (path), mimetype="text/html")
