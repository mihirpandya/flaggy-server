#!/usr/bin/env python

import ssl
import json
import socket
import struct
import binascii
import os

from doppio.api.responses import success, error

TOKEN = '88afede99bd86b675e68d97caa1a936071ba4501b17fb17f0e9bb46d32831e38'

# Payload for test #
PAYLOAD = {
    'aps': {
        'alert': 'Hello Push!',
        'sound': 'default'
    }
}

def send_push(token, payload):
    try:
    # Your certificate file
        print "token: %s payload %s" % (token, payload)
        cert = os.path.join(os.path.abspath(os.path.dirname(__file__)), "ck_prod.pem")
        dev_cert = os.path.join(os.path.abspath(os.path.dirname(__file__)), "ck.pem")

    # APNS development server
        apns_address = ('gateway.push.apple.com', 2195)
        dev_apns_address = ('gateway.sandbox.push.apple.com', 2195)

    # Use a socket to connect to APNS over SSL
        s = socket.socket()
        dev_s = socket.socket()
        sock = ssl.wrap_socket(s, ssl_version=ssl.PROTOCOL_SSLv3, certfile=cert)
        sock_dev = ssl.wrap_socket(dev_s, ssl_version=ssl.PROTOCOL_SSLv3, certfile=dev_cert)
        sock.connect(apns_address)
        sock_dev.connect(dev_apns_address)

        # Generate a notification packet
        token = binascii.unhexlify(token)
        fmt = '!cH32sH{0:d}s'.format(len(payload))
        cmd = '\x00'
        message = struct.pack(fmt, cmd, len(token), token, len(payload), payload)
        sock.write(message)
        sock.close()
        sock_dev.write(message)
        sock_dev.close()

        res = success("Payload sent!")

    except Exception as inst:
        res = error("Error. %s" % inst)

    return res


#if __name__ == '__main__':
#    send_push(TOKEN, json.dumps(PAYLOAD))