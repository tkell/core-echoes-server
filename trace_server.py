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

@app.route("/route")
def get_route():
    # get the sound from our database
    redis.rpush(trace_list, "this one!")
    redis.rpush(trace_list, "not this one")
    val = redis.lpop(trace_list)
    route = [{'a': 'yes', 'b': 'no'}, {'c': val}]
    res = json.dumps(route)
    return res

if __name__ == "__main__":
    app.run(debug=True)

