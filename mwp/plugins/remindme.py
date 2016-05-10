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
        self.remindme = RemindMe(self.load_data, self.save_data)
        BasePlugin.__init__(self, *args, **kwargs)

    @BasePlugin.expose('^!remindme (?P<info>.+)$')
    def remindme_now(self, message_data, info):
        # "!remindme {how long} [{description}]: Send a reminder (say '!remindme help' for more info)"

        if info == 'help':
            mwp_room_client.send_notification(HELP_MESSAGE, html=True)
            return

        if info == '!stats':
            mwp_room_client.send_notification(self._get_stats_message(), html=True)
            return

        if info == '!clear':
            self.remindme.clear()
            mwp_room_client.send_notification('Reminders cleared!', html=True)
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

    def _get_stats_message(self):
        reminder_infos = self.remindme.get_reminders()

        if not reminder_infos:
            mwp_room_client.send_notification(
                'There are no reminders set yet!'
            )
        else:
            output = ['These are the reminders I know about:']
            for reminder_info in reminder_infos:
                output.append(
                    ' :: '.join([
                        reminder_info['message']['user_mention_name'],
                        reminder_info['message']['room_name'],
                        reminder_info['description'],
                        reminder_info['datetime'].isoformat(),
                        self.remindme.summarise(reminder_info),
                    ])
                )

            mwp_room_client.send_notification(
                '<br/>\n'.join(output),
                html=True
            )
