#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import redis
from flask import Flask
from flask import jsonify
from flask.ext.cors import CORS 

app = Flask(__name__)
cors = CORS(app)

redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
redis = redis.from_url(redis_url)
trace_list = 'traces'

@app.route("/route", methods=['GET'])
def get_route():
    '''Gets the current trace'''
    val = redis.lrange(trace_list, 0, 1)
    route = {'data': val}
    res = json.dumps(route)
    return res

@app.route("/route", methods=['POST'])
def add_route():
    '''Add a new trace to the back of the queue'''
    print request.data, "HELLO"
    val = redis.rpush(trace_list, request.data)
    return val

@app.route("/route", methods=['DELETE'])
def delete_route():
    '''Deletes the trace from the front of the queue'''
    val = redis.lpop(trace_list)
    route = {'data': val}
    res = json.dumps(route)
    return res

if __name__ == "__main__":
    app.run(debug=True)

