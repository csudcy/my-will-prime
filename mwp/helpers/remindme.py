import datetime
import re

from mwp.helpers.time_parser import TimeParser
from mwp.helpers.time_summariser import TimeSummariser


class RemindMe(object):
    USAGE_MESSAGE = '!remindme {interval} [at {time}] [[to] {description}]'
    EXAMPLES = [
        '!remindme 30m',
        '!remindme tomorrow to Tell PO about new ticket',
        '!remindme next Thursday at 10am Move backlog grooming',
        '!remindme 1 year Jay\'s birthday!',
    ]


    def __init__(self, *args, **kwargs):
        self.time_parser = TimeParser()
        self.time_summariser = TimeSummariser()

    def add_reminder(self, message_data, text):
        """
        Given an input that can be parsed by ParseTime, add that to the list of reminders
        and return the parsed info.
        """
        # Parse the reminder info
        reminder_info = self.time_parser.parse_time_string(text)

        # Setup the reminder
        if reminder_info:
            pass

        # Let the callee know what we've done
        return reminder_info
    
    def summarise(self, reminder_info):
        return self.time_summariser.summarise(reminder_info)


if __name__ == '__main__':
    rm = RemindMe()
    rm.add_reminder('tomorrow at 2:30pm take out the trash')
