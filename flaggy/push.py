#!/usr/bin/env python

import ssl
import json
import socket
import struct
import binascii
from doppio.api.controllers import success, error

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
        cert = 'ck.pem'

    # APNS development server
        apns_address = ('gateway.sandbox.push.apple.com', 2195)

    # Use a socket to connect to APNS over SSL
        s = socket.socket()
        sock = ssl.wrap_socket(s, ssl_version=ssl.PROTOCOL_SSLv3, certfile=cert)
        sock.connect(apns_address)

        # Generate a notification packet
        token = binascii.unhexlify(token)
        fmt = '!cH32sH{0:d}s'.format(len(payload))
        cmd = '\x00'
        message = struct.pack(fmt, cmd, len(token), token, len(payload), payload)
        sock.write(message)
        sock.close()

        res = success("Payload sent!")

    except Exception as inst:
        res = error("Error. %s" % inst)

    return res


if __name__ == '__main__':
    send_push(TOKEN, json.dumps(PAYLOAD))