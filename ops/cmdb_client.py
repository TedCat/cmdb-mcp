#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os

import requests
from pprint import pprint
import click

class CmdbClient:
    DEFAULT_BASE_URL = 'https://cmdb.example.com/cmdb-api'
    DEFAULT_TIMEOUT = 120

    def __init__(self, identity=None, secret=None, base_url=None):
        self.identity = identity or "test"
        self.secret = secret or os.getenv("CMDB_PASSWORD", "not-set")
        self.base_url = base_url or self.DEFAULT_BASE_URL
        self.timeout = self.DEFAULT_TIMEOUT
        self.token = self.initialize_token()

    def initialize_token(self):
        data = {
            'identity': self.identity,
            'secret': self.secret
        }
        resp = requests.post(self.base_url + '/user/get_token', timeout=self.timeout, json=data)
        resp.raise_for_status()
        if resp.json()['code'] != 200:
            print("An error occurred during token initialization:", resp.json())
            raise Exception("Failed to initialize token")
        self.token = resp.json()['data']['access_token']
        return self.token

    def get_assets(self, catalog, filters=None):
        self.initialize_token()
        params = {
            'catalog': catalog,
        }
        # 合并其它过滤条件(map)
        if filters is not None:
            params.update(filters)
        headers = {'Authorization': f'Bearer {self.token}'}
        try:
            resp = requests.get(self.base_url + '/query/assets',
                                params=params, headers=headers, timeout=self.timeout)
            resp.raise_for_status()
            return resp.json()
        except requests.exceptions.HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except requests.exceptions.RequestException as err:
            print(f'Request error occurred: {err}')
        return None

@click.group()
@click.option('--identity', default='test', help='CMDB identity')
@click.option('--secret', default='not-set', help='CMDB secret')
@click.pass_context
def cli(ctx, identity, secret):
    """CMDB Client CLI tool for querying assets."""
    ctx.ensure_object(dict)
    ctx.obj['client'] = CmdbClient(identity=identity, secret=secret)

@cli.command()
@click.option('--public-ip', help='Filter by public IP address')
@click.option('--private-ip', help='Filter by private IP address')
@click.pass_context
def vm(ctx, public_ip, private_ip):
    """Query virtual machine assets."""
    client = ctx.obj['client']
    filters = {}

    if public_ip:
        filters['public_ip_address'] = public_ip
    if private_ip:
        filters['private_ip_address'] = private_ip

    response = client.get_assets(catalog='vm', filters=filters)['data']['list']
    pprint(response[0])

if __name__ == '__main__':
    cli(obj={})