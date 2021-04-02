__author__ = "Igor Maculan <n3wtron@gmail.com>"

import json
import logging
import time
from threading import Thread

import websocket

log = logging.getLogger("pushbullet.Listener")

WEBSOCKET_URL = "wss://stream.pushbullet.com/websocket/"


class Listener(Thread, websocket.WebSocketApp):
    def __init__(self, account, on_push=None, on_error=None, http_proxy_host=None, http_proxy_port=None):
        """
        :param account: Pushbullet object
        :param on_push: Function that gets called on all pushes. It takes one parameter as an argument - the data
            published on the push
        :param on_error: Function called upon application or websocket error. It takes one parameter as an argument -
            the exception triggered by the application
        :param http_proxy_host: Host proxy (ie localhost)
        :param http_proxy_port: Host port (ie 3128)
        """
        self._account = account
        self._api_key = self._account.api_key
        self.on_error = on_error

        Thread.__init__(self)
        websocket.WebSocketApp.__init__(
            self,
            WEBSOCKET_URL + self._api_key,
            on_open=self._on_open(),
            on_error=self._on_error(),
            on_message=self._on_message(),
            on_close=self._on_close(),
        )

        self.connected = False
        self.last_update = time.time()

        self.on_push = on_push

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

    def _on_open(self):
        def callback(*_):
            self.connected = True
            self.last_update = time.time()
        return callback

    def _on_close(self):
        def callback(*_):
            log.debug("Listener closed")
            self.connected = False
        return callback

    def _on_message(self):
        def callback(*args):
            message = args[1] if len(args) > 1 else args[0]
            log.debug("Message received:" + message)
            try:
                json_message = json.loads(message)
                if json_message["type"] != "nop":
                    self.on_push(json_message)
            except Exception as e:
                logging.exception(e)
        return callback

    def _on_error(self):
        def callback(*args):
            err = args[1] if len(args) > 1 else args[0]
            try:
                self.on_error(err)
            except Exception as e:
                logging.exception(e)
        return callback

    def run_forever(self, sockopt=None, sslopt=None, ping_interval=0, ping_timeout=None, *args, **kwargs):
        websocket.WebSocketApp.run_forever(
            self,
            sockopt=sockopt,
            sslopt=sslopt,
            ping_interval=ping_interval,
            ping_timeout=ping_timeout,
            http_proxy_host=self.http_proxy_host,
            http_proxy_port=self.http_proxy_port,
        )

    def run(self):
        self.run_forever()
