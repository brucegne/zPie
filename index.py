from flask import Flask, Response, redirect, url_for, escape, request, make_response, Response, session, abort, g, flash, _app_ctx_stack, send_file, jsonify
app = Flask(__name__)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return Response("<h1>Flask on Now</h1><p>You visited: /%s</p>" % (path), mimetype="text/html")
