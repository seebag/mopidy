from __future__ import unicode_literals

import logging

from mopidy.frontends.mpd import dispatcher, protocol
from mopidy.utils import formatting, network

logger = logging.getLogger('mopidy.frontends.mpd')


class MpdSession(network.LineProtocol):
    """
    The MPD client session. Keeps track of a single client session. Any
    requests from the client is passed on to the MPD request dispatcher.
    """

    terminator = protocol.LINE_TERMINATOR
    encoding = protocol.ENCODING
    delimiter = r'\r?\n'

    def __init__(self, connection, core=None):
        super(MpdSession, self).__init__(connection)
        self.dispatcher = dispatcher.MpdDispatcher(session=self, core=core)

    def on_start(self):
        logger.info('New MPD connection from [%s]:%s', self.host, self.port)
        self.send_lines(['OK MPD %s' % protocol.VERSION])

    def on_line_received(self, line):
        logger.debug('Request from [%s]:%s: %s', self.host, self.port, line)

        response = self.dispatcher.handle_request(line)
        if not response:
            return

        logger.debug(
            'Response to [%s]:%s: %s', self.host, self.port,
            formatting.indent(self.terminator.join(response)))

        self.send_lines(response)

    def on_idle(self, subsystem):
        self.dispatcher.handle_idle(subsystem)

    def decode(self, line):
        try:
            return super(MpdSession, self).decode(line.decode('string_escape'))
        except ValueError:
            logger.warning(
                'Stopping actor due to unescaping error, data '
                'supplied by client was not valid.')
            self.stop()

    def close(self):
        self.stop()
