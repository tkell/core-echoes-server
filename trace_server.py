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
    print "hello?"
    val = redis.lrange(trace_list, 0, 0)
    print val
    return jsonify(val)

@app.route("/add_route", methods=['POST'])
def add_route():
    '''Add a new trace to the back of the queue'''
    redis.rpush(trace_list, request.data)
    return ''

@app.route("/delete_route", methods=['DELETE'])
def delete_route():
    '''Deletes the trace from the front of the queue'''
    val = redis.lpop(trace_list)
    return jsonify(val)

if __name__ == "__main__":
    app.run(debug=True)

