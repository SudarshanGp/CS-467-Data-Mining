#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys

sys.path.insert(2, '/usr/local/lib/python2.7/site-packages')
from flask import Flask, render_template, request, jsonify
import json


app = Flask(__name__)
data_2014 = []
data_2015 = []
data_2016 = []

data = []
user_map = {}
user_list = []
user_add_list = []
curr_user_data = []
curr_users = ""


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    """
    The index function is called when the a user makes a request to the ip address at which
    the website is hosted. It returns the base.html template and is rendered by jinja2
    :return: Return the base.html template when the root / or /index is requested
    """
    # Name = user I'm talking to
    # Value = pos/neg sentiment value
    # parent = Positive or Negative
    # month  = 01 - 12
    global data
    global curr_users
    global curr_user_data
    user_data = []
    add_flag = False
    if path is "":
        add_flag = False
        user = 'Aadhya Gupta'
    elif 'ADD' in path:
        path = str(path)
        temp_path = path.strip('_')
        user = user_map[str(temp_path[0])]
        add_flag = True
    else:
        add_flag = False
        user = user_map[str(path)]
    if add_flag is False:
        print("IN FALSE")
        for key, value in enumerate(data):
            users = value['users'].split(', ')
            if 'Sudarshan' in users[0]:
                other = users[1]
            else:
                other = users[0]
            other = str(other)

            if user in other:
                for key, val in value['data'].iteritems():
                    temp = key.split(' ')
                    new_date = temp[0] + '/' +  temp[1].zfill(2)
                    user_data.append({"month" : new_date, "name":other, "Sentiment" : val['p_pos'], "parent" : "Positive"})
        user_data = sorted(user_data, key=lambda k: k['month'])
        curr_user_data = user_data
        curr_users = user
    elif add_flag is True:
        for key, value in enumerate(data):
            users = value['users'].split(', ')
            if 'Sudarshan' in users[0]:
                other = users[1]
            else:
                other = users[0]
            other = str(other)

            if user in other:
                for key, val in value['data'].iteritems():
                    temp = key.split(' ')
                    new_date = temp[0] + '/' +  temp[1].zfill(2)
                    curr_user_data.append({"month" : new_date, "name":other, "Sentiment" : val['p_pos'], "parent" : "Positive"})
        curr_user_data = sorted(curr_user_data, key=lambda k: k['month'])
        curr_users += ' , ' + user

    return render_template('base.html', sample_data = curr_user_data, user = curr_users, user_list = user_list, user_add_list= user_add_list)

@app.errorhandler(Exception)
def exception_handler(error):
    """
    Handles exceptions that are raised by the program during run time
    :param error: Error code that is raised
    :return: Error information
    """
    return 'ERROR ' + repr(error)


if __name__ == '__main__':
    with open('static/data/data_sentiment_user_formatted_bayes.json') as data_file:
        data = json.load(data_file)
    for key, value in enumerate(data):
        users = value['users'].split(', ')
        if 'Sudarshan' in users[0]:
            other = users[1]
        else:
            other = users[0]
        other = str(other)
        user_map[str(key)] = other
        user_list.append({"name":other, "href":str(key)})
        user_add_list.append({"name":other, "href":str(key) + "_ADD"})
    app.run()