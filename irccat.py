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

try:
    import weechat
    from weechat import prnt
    WEECHAT_RC_OK = weechat.WEECHAT_RC_OK
    import_ok = True
except ImportError:
    print "This script must be run under WeeChat."
    print "Get WeeChat now at: https://weechat.org/"
    import_ok = False


def irccat_start():
    """Startup function"""
    buffer = weechat.buffer_new('irccat', '', '', '', '')
    weechat.buffer_set(buffer, 'title', '[irccat]')

    return buffer


def irccat_end():
    """Cleanup function"""
    weechat.buffer_close(irccat_buffer)
    return weechat.WEECHAT_RC_OK


if __name__ == '__main__' and import_ok and \
        weechat.register(SCRIPT_NAME,
                         SCRIPT_AUTHOR,
                         SCRIPT_VERSION,
                         SCRIPT_LICENSE,
                         SCRIPT_DESC,
                         'irccat_end',
                         'UTF-8'):

    irccat_buffer = irccat_start()


