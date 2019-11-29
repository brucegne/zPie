from flask import Flask, render_template, Response, redirect, url_for, escape, request, make_response, Response, session, abort, g, flash, _app_ctx_stack, send_file, jsonify
app = Flask(__name__)

@app.route('/', defaults={'path': ''})

@app.route('/dailyjson', methods=['GET', 'POST'])
def daily__json():
#    return Response("It's the daily stuff")
    if request.method == 'GET':
        prms = {
        }
        resp = make_response( render_template('index.html',**prms), 200 )
        return resp

@app.route('/<path:path>')
def catch_all(path):
    return Response("<h1>Flask on Now</h1><p>You visited: /%s</p>" % (path), mimetype="text/html")
