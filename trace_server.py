#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

@app.route("/route", methods=['GET'])
def get_route():
    '''Gets the current trace'''
    val = redis.lrange(trace_list, 0, 0)
    route = {'data': val}
    res = json.dumps(route)
    return res

@app.route("/add_route", methods=['POST'])
def add_route():
    '''Add a new trace to the back of the queue'''
    print "HELLO", request, request.data
    redis.rpush(trace_list, "wombat")
    return ''

@app.route("/delete_route", methods=['DELETE'])
def delete_route():
    '''Deletes the trace from the front of the queue'''
    val = redis.lpop(trace_list)
    route = {'data': val}
    res = json.dumps(route)
    return res

if __name__ == "__main__":
    app.run(debug=True)

