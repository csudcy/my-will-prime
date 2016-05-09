from mwp.helpers.remindme import RemindMe
from mwp.mwp_client import mwp_room_client
from mwp.plugins.base_plugin import BasePlugin

HELP_MESSAGE = """
To set a reminder, say:<br/>
&nbsp;<b>{usage}</b><br/>
<br/>
For example:<br/>
<b>
{examples}
</b>
""".format(
    usage=RemindMe.USAGE_MESSAGE,
    examples='\n'.join([
        '&nbsp;{example}<br/>'.format(example=example)
        for example in RemindMe.EXAMPLES
    ])
)


class RemindMePlugin(BasePlugin):

    def __init__(self, *args, **kwargs):
        self.remindme = RemindMe()
        BasePlugin.__init__(self, *args, **kwargs)

    @BasePlugin.expose('^!remindme (?P<info>.+)$')
    def remindme_now(self, message_data, info):
        # "!remindme {how long} [{description}]: Send a reminder (say '!remindme help' for more info)"

        if info == 'help':
            mwp_room_client.send_notification(HELP_MESSAGE, html=True)
            return

        reminder_info = self.remindme.add_reminder(message_data, info)

        if not reminder_info:
            mwp_room_client.send_notification(
                'I\'m sorry @{md.user_mention_name}, I couldn\'t understand that! Say \'!remindme help\' for some examples.'.format(
                    md=message_data,
                )
            )
        else:
            mwp_room_client.send_notification(
                'Ok @{md.user_mention_name}, I\'ll remind you to {summary}'.format(
                    md=message_data,
                    summary=self.remindme.summarise(reminder_info),
                )
            )
