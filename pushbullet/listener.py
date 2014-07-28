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
                 device_id=None,
                 on_push=None,
                 http_proxy_host=None,
                 http_proxy_port=None):
        """
        :param api_key: pushbullet Key
        :param device_id: id of device to listen (if None listen all devices)
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
        self.device_id = device_id
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
        self.history = dict(note=list(),
                            link=list(),
                            address=list(),
                            list=list(),
                            file=list())

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
                pushes_url = PUSHES_URL + '?modified_after=' + str(self.last_update)
                logging.debug('calling:' + pushes_url)
                res = requests.get(pushes_url, auth=(self.api_key, ""), proxies=self.proxies)
                self.last_update = time.time()
                pushes = res.json()['pushes']
                for push in pushes:
                    log.debug(str(push))
                    if self.device_id is None or \
                            ('target_device_iden' in push and \
                                         push['target_device_iden'] == self.device_id):
                        if push['type'] not in self.history.keys():
                            raise PushTypeNotProvided('Type not provided:' + push['type'])
                        else:
                            # add the push to history
                            self.history[push['type']].append(push)
                            # call specific method/function
                            if push['type'] == 'note' and self.on_note is not None:
                                self.on_note(push)
                            if push['type'] == 'link' and self.on_link is not None:
                                self.on_link(push)
                            if push['type'] == 'address' and self.on_address is not None:
                                self.on_address(push)
                            if push['type'] == 'list' and self.on_list is not None:
                                self.on_list(push)
                            if push['type'] == 'file' and self.on_file is not None:
                                self.on_file(push)
                log.debug(str(self.history))
        except Exception as e:
            logging.exception(e)

    def run_forever(self, sockopt=None, sslopt=None, ping_interval=0, ping_timeout=None):
        websocket.WebSocketApp.run_forever(self, sockopt=sockopt, sslopt=sslopt, ping_interval=ping_interval,
                                           ping_timeout=ping_timeout,
                                           http_proxy_host=self.http_proxy_host,
                                           http_proxy_port=self.http_proxy_port)

    def run(self):
        self.run_forever()

