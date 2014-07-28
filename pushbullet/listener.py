__author__ = 'Igor Maculan <n3wtron@gmail.com>'

import logging
import time
import json
from threading import Thread

import requests
import websocket


log = logging.getLogger('pushbullet.Listener')

WEBSOCKET_URL = 'wss://stream.pushbullet.com/websocket/'
PUSHES_URL = 'https://api.pushbullet.com/v2/pushes'


class PushTypeNotProvided(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class Listener(Thread, websocket.WebSocketApp):
    def __init__(self, api_key,
                 on_push=None,
                 http_proxy_host=None,
                 http_proxy_port=None):
        """
        :param api_key: pushbullet Key
        :param on_push: function that get's called on all pushes
        :param http_proxy_host: host proxy (ie localhost)
        :param http_proxy_port: host port (ie 3128)
        """
        Thread.__init__(self)
        websocket.WebSocketApp.__init__(self, WEBSOCKET_URL + api_key,
                                        on_open=self.on_open,
                                        on_message=self.on_message,
                                        on_close=self.on_close)
        self.api_key = api_key
        self.connected = False
        self.last_update = time.time()

        # History
        self.history = None
        self.clean_history()

        # proxy configuration
        self.http_proxy_host = http_proxy_host
        self.http_proxy_port = http_proxy_port
        self.proxies = None
        if http_proxy_port is not None and http_proxy_port is not None:
            self.proxies = {
                "http": "http://" + http_proxy_host + ":" + str(http_proxy_port),
                "https": "http://" + http_proxy_host + ":" + str(http_proxy_port),
            }

    def clean_history(self):
        self.history = []

    def on_open(self, ws):
        self.connected = True
        self.last_update = time.time()

    def on_close(self, ws):
        log.debug('Listener closed')
        self.connected = False

    def on_message(self, ws, message):
        log.debug('Message received:' + message)
        try:
            json_message = json.loads(message)
            if json_message['type'] == 'tickle':
                self.on_push()
        except Exception as e:
            logging.exception(e)

    def run_forever(self, sockopt=None, sslopt=None, ping_interval=0, ping_timeout=None):
        websocket.WebSocketApp.run_forever(self, sockopt=sockopt, sslopt=sslopt, ping_interval=ping_interval,
                                           ping_timeout=ping_timeout,
                                           http_proxy_host=self.http_proxy_host,
                                           http_proxy_port=self.http_proxy_port)

    def run(self):
        self.run_forever()

