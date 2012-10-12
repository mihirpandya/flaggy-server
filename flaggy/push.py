#!/usr/bin/env python

import ssl
import json
import socket
import struct
import binascii

TOKEN = '88afede9 9bd86b67 5e68d97c aa1a9360 71ba4501 b17fb17f 0e9bb46d 32831e38'

# Payload for test #
PAYLOAD = {
    'aps': {
        'alert': 'Hello Push!',
        'sound': 'default'
    }
}


def send_push(token, payload):
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


if __name__ == '__main__':
    send_push(TOKEN, json.dumps(PAYLOAD))