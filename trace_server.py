#!/usr/bin/env python
# -*- coding: utf-8 -*-


## Need to build /diagnostics!

import os
import json
import redis
from flask import Flask
from flask import jsonify
from flask import request
from flask.ext.cors import CORS 

app = Flask(__name__)
cors = CORS(app)

redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
redis = redis.from_url(redis_url)
trace_list = 'traces'
last_ip = 'last_ip'

@app.route("/status", methods=['GET'])
def status():
    '''returns the status'''
    count = redis.llen(trace_list)
    last_ip = redis.get(last_ip)
    return "Online:  %d traces in the db.  Last sent IP is %s" % count, last_ip

@app.route("/count", methods=['GET'])
def count():
    '''returns the number of traces currently stored'''
    count = redis.llen(trace_list)
    return jsonify({'count': count})

# Debug
#@app.route("/delete_all", methods=['GET'])
def delete_all():
    '''Debug:  clears the redis queue'''
    res = redis.ltrim(trace_list, 0, 0)
    res = redis.lpop(trace_list)
    count = redis.llen(trace_list)
    return jsonify({'count': count})

@app.route("/route", methods=['GET'])
def get_route():
    '''Gets the current trace'''
    val = redis.lrange(trace_list, 0, 0)
    if val:
        res = val[0]
    else:
        res = ''
    return res

@app.route("/add_route", methods=['POST'])
def add_route():
    '''Add a new trace to the back of the queue'''
    trace = request.data['trace']
    target = request.data['target']
    redis.rpush(trace_list, request.data)
    redis.set(last_ip, target)
    return ''

@app.route("/delete_route", methods=['DELETE'])
def delete_route():
    '''Deletes the trace from the front of the queue, and return the trace *after* that'''
    val = redis.lpop(trace_list)
    return get_route()

if __name__ == "__main__":
    app.run(debug=True)

