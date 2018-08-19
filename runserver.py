#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : runserver.py.py
# @Author: harry
# @Date  : 18-8-19 下午5:56
# @Desc  : Run flask server

import os
from flask import Flask, request, jsonify
from gevent import pywsgi
import configparser
from generate_new import *
from gevent import monkey

monkey.patch_all()

app = Flask(__name__)
model = None
rhyme_style = ['AAAA', 'ABAB', '_A_A', 'ABBA']


@app.route('/generate/verse', methods=['GET'])
def index():
    # GET params
    text = request.args.get('text', '')
    num_sentence = int(request.args.get('num_sentence', ''))
    target_long = int(request.args.get('target_length', ''))
    rhyme_mode = int(request.args.get('rhyme_mode', '1'))
    rhyme_style_id = int(request.args.get('rhyme_style_id', '0'))

    model.user_input(
        text=text,
        sample_size=num_sentence,
        target_long=target_long,
        rhyme_mode=rhyme_mode,
        rhyme_style=rhyme_style[rhyme_style_id]
    )
    sentences = model.generator()
    return jsonify(list(sentences))


if __name__ == "__main__":
    # load model
    print("Loading model...")
    model = Gen()
    model.restore_model('./checkpoint')

    # load config from web.ini
    cp = configparser.ConfigParser()
    cp.read('web.ini')
    ip = str(cp.get('web', 'ip'))
    port = int(cp.get('web', 'port'))

    # start flask server
    print("Starting web server at {}:{}".format(ip, port))
    server = pywsgi.WSGIServer((ip, port), app)
    server.serve_forever()
