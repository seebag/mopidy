from __future__ import unicode_literals

from mopidy.frontends.mpd.protocol import handle_request
from mopidy.frontends.mpd.exceptions import MpdNotImplemented


@handle_request(r'^disableoutput "(?P<outputid>\d+)"$')
def disableoutput(context, outputid):
    """
    *musicpd.org, audio output section:*

        ``disableoutput``

        Turns an output off.
    """
    pass


@handle_request(r'^enableoutput "(?P<outputid>\d+)"$')
def enableoutput(context, outputid):
    """
    *musicpd.org, audio output section:*

        ``enableoutput``

        Turns an output on.
    """
    outputs = context.core.playback.list_output().get()
    context.core.playback.set_output(outputs[int(outputid)])


@handle_request(r'^outputs$')
def outputs(context):
    """
    *musicpd.org, audio output section:*

        ``outputs``

        Shows information about all outputs.
    """
    outputs = context.core.playback.list_output().get()
    current_output = context.core.playback.get_current_output().get()
    mpd_outputs = []
    index = 0
    for out in outputs:
        mpd_outputs += (('outputid', index),)
        mpd_outputs += (('outputname', out),)
        if out == current_output:
            mpd_outputs += (('outputenabled', 1),)
        else:
            mpd_outputs += (('outputenabled', 0),)
        index += 1

    return mpd_outputs
