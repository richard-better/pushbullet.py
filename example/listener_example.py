__author__ = 'Igor Maculan <n3wtron@gmail.com>'
import logging

from pushbullet import Listener, PushBullet


logging.basicConfig(level=logging.DEBUG)

API_KEY = ''  # YOUR API KEY

HTTP_PROXY_HOST = None
HTTP_PROXY_PORT = None


def on_push(message):
    print ('received push:' + str(message))

def main():
	pb = PushBullet(API_KEY)
	s = Listener(pb,on_push = on_push, http_proxy_host=HTTP_PROXY_HOST, http_proxy_port=HTTP_PROXY_PORT)
	try:
		s.run_forever()
	except KeyboardInterrupt:
		s.close()


if __name__ == '__main__':
	main()
