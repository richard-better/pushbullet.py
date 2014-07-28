__author__ = 'Igor Maculan <n3wtron@gmail.com>'
import logging

from pushbullet import Listener


logging.basicConfig(level=logging.DEBUG)

API_KEY = ''  # YOUR API KEY
DEVICE_ID = ''  # id of device if None the listener listen all pushes
HTTP_PROXY_HOST = None
HTTP_PROXY_PORT = None


def on_link(lnk):
    print ('received link:' + lnk['url'])


def main():
    s = Listener(API_KEY,
                 device_id=DEVICE_ID,
                 on_link=on_link,
                 http_proxy_host=HTTP_PROXY_HOST,
                 http_proxy_port=HTTP_PROXY_PORT)
    try:
        s.run_forever()
    except KeyboardInterrupt:
        s.close()


if __name__ == '__main__':
    main()