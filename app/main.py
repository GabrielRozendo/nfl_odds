import json
import requests
import sys
import logging
from types import SimpleNamespace
from flask import Flask
from json2html import json2html
from datetime import datetime
import os

from .process_results import Results

app = Flask(__name__)


@app.route('/odds')
def odds():
    api_key = os.environ.get('APIKEY')
    sport_key = 'americanfootball_nfl'
    region = 'us'

    odds_response = requests.get('https://api.the-odds-api.com/v3/odds/?', params={
        'api_key': api_key,
        'sport': sport_key,
        'region': region,
        'dateFormat': 'iso',
    })

    odds_json = json.loads(odds_response.text)

    if not odds_json['success']:
        return 'There was a problem with the sports request: ' + odds_json['msg']

    else:
        data = odds_json['data']
        req_remaining = odds_response.headers['x-requests-remaining']
        req_used = odds_response.headers['x-requests-used']
        return (data, req_used, req_remaining)


@app.route('/')
def index():
    result = odds()
    data = result[0]
    results = [json.loads(json.dumps(
        i), object_hook=lambda d: SimpleNamespace(**d)) for i in data]
    processed = Results(results).process()

    html = '<html><head><link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css"></head><body>'
    html += '<div class="w3-container w3-padding-16" style="background-color: #013369; color: #fff"><h1>NFL Odds</h1></div><br />'

    now = datetime.now().strftime("%b %d %Y %H:%M")
    footer = f'<br /><div class="w3-container w3-padding-16" style="background-color: #D50A0A; color: #fff">'
    footer += f'<p>{now} -- Requests {result[1]} and {result[2]} remaining</p>'
    footer += '</div></body></html>'

    output = json2html.convert(
        json=processed, table_attributes='class="w3-table-all w3-centered w3-hoverable w3-card-4 w3-large"')

    return html + output + footer
