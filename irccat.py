# coding=utf-8
"""
irccat.py - Network socket listener
Copyright (c) 2014 Mikael Sörlin <iamtew@asylunatic.se>
Licensed under the MIT License.

https://github.com/iamtew/weechat-scripts
"""

SCRIPT_NAME    = "irccat"
SCRIPT_AUTHOR  = "Mikael Sörlin <iamtew@asylunatic.se>"
SCRIPT_VERSION = "0.1.dev1"
SCRIPT_LICENSE = "MIT"
SCRIPT_DESC    = "Network socket listener"

IRCCAT_ADDR = 'localhost'
IRCCAT_PORT = 5234

try:
    import weechat
    from weechat import prnt
    WEECHAT_RC_OK = weechat.WEECHAT_RC_OK
    import_ok = True
except ImportError:
    print "This script must be run under WeeChat."
    print "Get WeeChat now at: https://weechat.org/"
    import_ok = False


import socket


def irccat_socket_open(addr, port):
    """
    Open our listener socket.

    :return: socket pointer
    """
    prnt(irccat_buffer, 'Opening socket on ' + str(addr) + ':' + str(port))
    rsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    rsocket.bind((addr, int(port)))
    rsocket.listen(5)

    return rsocket


def irccat_readmsg():
    while True:
        conn, addr = irccat_socket.accept()
        data = conn.recv(1024)
        prnt(irccat_buffer, 'Message: ' + data)
        conn.close()


def irccat_socket_close(socket):
    """
    Close our listening socket
    """
    prnt(irccat_buffer, 'Closing socket')


def irccat_load_config():
    """
    Load our configuration
    """
    prnt(irccat_buffer, 'Loading configuration')


def irccat_start():
    """
    Startup function

    :return: irccat buffer pointer
    """
    buffer = weechat.buffer_new('irccat', '', '', '', '')
    weechat.buffer_set(buffer, 'title', '[irccat]')

    return buffer


def irccat_end():
    """
    Cleanup function

    :return: weechat OK
    """
    irccat_socket_close(irccat_socket)
    weechat.buffer_close(irccat_buffer)

    return WEECHAT_RC_OK


if __name__ == '__main__' and import_ok and \
        weechat.register(SCRIPT_NAME,
                         SCRIPT_AUTHOR,
                         SCRIPT_VERSION,
                         SCRIPT_LICENSE,
                         SCRIPT_DESC,
                         'irccat_end',
                         'UTF-8'):

    irccat_buffer = irccat_start()
    irccat_socket = irccat_socket_open(IRCCAT_ADDR, IRCCAT_PORT)

    conn, addr = irccat_socket.accept()
    data = conn.recv(1024)
    prnt(irccat_buffer, 'Message: ' + data)
    conn.close()
