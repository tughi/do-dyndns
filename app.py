import logging

import requests
from flask import Flask
from flask import request

from config import API_TOKEN
from config import DOMAIN
from config import RECORDS

logger = logging.getLogger(__file__)

app = Flask(__name__)


@app.errorhandler(404)
def page_not_found(error):
    return 'Ups...', 404, {'Content-Type': 'text/plain'}


@app.route('/refresh/<node>')
def update_record(node):
    if node in RECORDS:
        logger.info(f"Defined node: {node}")

        api_response = requests.put(
            f'https://api.digitalocean.com/v2/domains/{DOMAIN}/records/{RECORDS[node]}',
            json={
                'data': request.remote_addr,
            },
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {API_TOKEN}'
            }
        )

        logger.info(api_response.content)
    else:
        logger.warning(f"Unknown node: {node}")

    return page_not_found(None)
