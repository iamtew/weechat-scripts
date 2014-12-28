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

IRCCAT_COMMAND = 'irccat'
IRCCAT_BUFFER  = 'irccat'

DEBUG = True

try:
    import weechat
    import_ok = True
except ImportError:
    print "This script must be run under WeeChat."
    print "Get WeeChat now at: https://weechat.org/"
    import_ok = False

try:
    import socket
except ImportError as message:
    print('Missing package(s) for %s: %s' % (SCRIPT_NAME, message))
    import_ok = False


irccat = {
    'socket':  None,
    'hook_fd': None,
    'buffer':  ''
}

irccat_settings_default = {
    'autostart': ('on', 'Start the listening socket on startup'),
    'address':   ('localhost', 'Address to listen to'),
    'port':      ('5234', 'Port to listen to (empty value = random free port)'),
    'buffer':    ('on', 'Enable the irccat buffer'),
}

irccat_settings = {}


def debug(str):
    if DEBUG:
        weechat.prnt('', '%sDEBUG: %s' % (weechat.prefix('error'), str))


def message_handler(addr, data):
    """
    Handle our message and do some stuff with it here
    """
    weechat.prnt(irccat['buffer'], 'meeh: %s %s ' % (data, addr))


def irccat_listener_fd_cb(data, fd):
    """
    Listener file descriptor callback
    """
    if not irccat['socket']:
        return weechat.WEECHAT_RC_OK

    conn, addr = irccat['socket'].accept()
    data = conn.recv(1024)

    message_handler(addr, data)
    # weechat.prnt(irccat['buffer'], 'Message from "%s" saying: %s' % (addr, data))

    conn.close()
    return weechat.WEECHAT_RC_OK


def irccat_listener_status():
    """
    Display listener status
    """
    global irccat

    if irccat['socket']:
        weechat.prnt(irccat['buffer'], 'Listening on %s' % str(irccat['socket'].getsockname()))
    else:
        weechat.prnt(irccat['buffer'], 'Listener not running')


def irccat_listener_start():
    """
    Start our listerner socket
    """
    global irccat
    global irccat_settings

    if irccat['socket']:
        weechat.prnt(irccat['buffer'], 'Listener already running')
        return

    port = 0
    try:
        port = int(irccat_settings['port'])
    except:
        port = 0

    irccat['socket'] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    irccat['socket'].setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        irccat['socket'].bind((irccat_settings['address'], port))
    except Exception as e:
        weechat.prnt('', '%sBind error: %s' % (weechat.prefix('error'), e))
        irccat['socket'] = None
        irccat_listener_status()
        return

    weechat.config_set_plugin('port', str(irccat['socket'].getsockname()[1]))
    irccat['socket'].listen(5)
    irccat['hook_fd'] = weechat.hook_fd(irccat['socket'].fileno(), 1, 0, 0, 'irccat_listener_fd_cb', '')
    irccat_listener_status()


def irccat_listener_stop():
    """
    Stop our listener
    """
    global irccat

    if irccat['socket']:
        irccat['socket'].close()
        irccat['socket'] = None

    weechat.prnt(irccat['buffer'], 'Listener stopped')


def irccat_listener_restart():
    """
    Restart the listener
    """
    irccat_listener_stop()
    irccat_listener_start


def irccat_socket_close():
    """
    Close our listening socket
    """
    weechat.prnt(irccat['buffer'], 'Closing socket')
    return weechat.WEECHAT_RC_OK


def irccat_buffer_input_cb(data, buffer, input_data):
    """
    Handle input in our buffer
    """
    # buffer_cmd(input_data)
    if ('show run', 'configuration') in input_data:
        buffer_command_show_run()

    return weechat.WEECHAT_RC_OK


def buffer_command_show_run():
    """
    Handle our input on the buffer
    """
    weechat.prnt(irccat['buffer'], 'irccat settings:')
    for key in irccat_settings:
        weechat.prnt(irccat['buffer'],
                     ' %s = %s' % (key, irccat_settings[key]))


def irccat_buffer_close_cb(data, buffer):
    """
    Buffer close callback
    """
    global irccat

    irccat['buffer'] = ''

    return weechat.WEECHAT_RC_OK


def irccat_buffer_open():
    """
    Open our buffer
    """
    global irccat

    if not irccat['buffer']:
        irccat['buffer'] = weechat.buffer_new(IRCCAT_BUFFER,
                                              'irccat_buffer_input_cb', '',
                                              'irccat_buffer_close_cb', '')

    if irccat['buffer']:
        weechat.buffer_set(irccat['buffer'],
                           'title',
                           '%s - %s'
                           % (SCRIPT_NAME, SCRIPT_DESC))

    weechat.buffer_set(irccat['buffer'], 'display', '1')

    return weechat.WEECHAT_RC_OK


def irccat_config_cb(data, key, value):
    """
    Configuration callback
    """
    global irccat_settings

    option = key.split('.')[-1]
    irccat_settings[option] = value

    return weechat.WEECHAT_RC_OK


def irccat_end():
    """
    Cleanup function
    """
    irccat_listener_stop()
    weechat.buffer_close(irccat['buffer'])

    return weechat.WEECHAT_RC_OK


def hash_channels():
    """
    Return hash of network and channels the client is on
    """
    result = {}
    irc_servers = weechat.infolist_get('irc_server', '', '')

    while weechat.infolist_next(irc_servers):
        current_server = weechat.infolist_string(irc_servers, 'name')
        result[current_server] = []

        irc_channels = weechat.infolist_get('irc_channel', '', current_server)
        while weechat.infolist_next(irc_channels):
            current_channel = weechat.infolist_string(irc_channels, 'name')
            result[current_server].append(current_channel)

    return result


if __name__ == '__main__' and import_ok and \
        weechat.register(SCRIPT_NAME,
                         SCRIPT_AUTHOR,
                         SCRIPT_VERSION,
                         SCRIPT_LICENSE,
                         SCRIPT_DESC,
                         'irccat_end',
                         'UTF-8'):

    # Set default options
    for option, value in irccat_settings_default.items():
        if weechat.config_is_set_plugin(option):
            irccat_settings[option] = weechat.config_get_plugin(option)
        else:
            weechat.config_set_plugin(option, value[0])
            irccat_settings[option] = value[0]

    # Check for configuration changes
    weechat.hook_config("plugins.var.python." + SCRIPT_NAME + ".*",
                        "irccat_config_cb", "")

    # Open our buffer
    irccat_buffer_open()

    # Start our listener socket
    if irccat_settings['autostart'] == 'on':
        irccat_listener_start()
