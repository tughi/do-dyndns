import logging

import requests
from flask import Flask
from flask import request

from config import API_TOKEN
from config import DOMAIN
from config import RECORDS

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

app = Flask(__name__)


@app.cli.command('list-all-records')
def command():
    api_response = requests.get(
        f'https://api.digitalocean.com/v2/domains/{DOMAIN}/records',
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {API_TOKEN}'
        }
    )
    api_response.raise_for_status()

    for record in api_response.json().get('domain_records'):
        record_type = record['type']
        if record_type in ('A', 'AAAA'):
            record_name = record['name']
            if record_name != '@':
                logger.info(f"{record_name}: id={record['id']}, addr={record['data']}")


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
