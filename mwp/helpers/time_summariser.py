import datetime
import re


class TimeSummariser(object):

    def summarise(self, reminder_info, now=None):
        """
        Given information parsed by parse_time_string, summarise it nicely
        Future examples:
            backlog groom in 2 hours
            backlog groom tomorrow at 10
            backlog groom Mar 25 at 10
        Past examples:
            backlog groom 2 hours ago
            backlog groom yesterday at 10
            backlog groom Mar 25 at 10
        """
        time_string = self._get_time_summary(reminder_info, now)
        if reminder_info['description']:
            return '{desc} {time_string}'.format(
                desc=reminder_info['description'],
                time_string=time_string
            )
        return time_string

    def _get_time_summary(self, reminder_info, now):
        """
        Given information parsed by parse_time_string, summarise the time information
        Future examples:
            in 2 hours
            tomorrow at 10
            Mar 25 at 10
        Past examples:
            2 hours ago
            yesterday at 10
            Mar 25 at 10
        """
        now = now or datetime.datetime.now()

        # Get the timedelta
        dt = reminder_info['datetime']
        diff = abs(dt - now)
        import math
        minutes = int(diff.days * 24 * 60 + math.floor(diff.seconds / 60.0))
        hours = int(math.floor(minutes / 60.0))
        days = int(math.floor(hours / 24.0))
        weeks = int(math.floor(days / 7.0))

        # Should we add 'in ' or ' ago'?
        if dt < now:
            time_string_format = '{time_string} ago'
        else:
            time_string_format = 'in {time_string}'

        # It was/is today, show hours or minutes
        if minutes <= 1:
            time_string_format = '{time_string}'
            time_string = 'now'
        elif minutes < 60:
            # Use minutes
            time_string = '{count} minutes'.format(
                count=minutes
            )
        elif hours == 1:
            # Use hours
            time_string = 'an hour'
        elif hours < 24:
            # Use hours
            time_string = '{count} hours'.format(
                count=hours
            )
        # elif days == 1:
        #     time_string_format = '{time_string}'
        #     if dt < now:
        #         time_string = 'yesterday'
        #     else:
        #         time_string = 'tomorrow'
        #     time_string += ' at {hour:02}:{minute:02}'.format(
        #         hour=dt.hour,
        #         minute=dt.minute,
        #     )
        elif days == 1:
            # Use days
            time_string = 'a day'
        elif days < 7:
            # Use days
            time_string = '{count} days'.format(
                count=days
            )
        elif weeks == 1:
            # Use weeks
            time_string = 'a week'
        else:
            # Use weeks
            time_string = '{count} weeks'.format(
                count=weeks
            )

        return time_string_format.format(
            time_string=time_string
        )


if __name__ == '__main__':
    ts = TimeSummariser()
    def check(dt, expected, description='', now=(2000,1,1,12,30)):
        print dt, description, '...',

        # Do it
        parsed_info = {
            'datetime': datetime.datetime(*dt),
            'description': description
        }
        summary = ts.summarise(parsed_info, now=datetime.datetime(*now))

        # Check what we got
        if expected != summary:
            print 'FAILED'
            print '    Expected: ', expected
            print '    Actual  : ', summary
        else:
            print 'SUCCESS'

    def check2(dt, expected):
        check(dt, expected, '')
        check(dt, 'I can haz description '+expected, 'I can haz description')

    check2((2000, 1, 1, 12, 29), 'now')
    check2((2000, 1, 1, 12, 30), 'now')
    check2((2000, 1, 1, 12, 31), 'now')

    check2((2000, 1, 1, 12, 45), 'in 15 minutes')
    check2((2000, 1, 1, 12, 15), '15 minutes ago')

    check2((2000, 1, 1, 13, 45), 'in an hour')
    check2((2000, 1, 1, 11, 15), 'an hour ago')

    check2((2000, 1, 1, 14, 15), 'in an hour')
    check2((2000, 1, 1, 10, 45), 'an hour ago')

    check2((2000, 1, 1, 14, 45), 'in 2 hours')
    check2((2000, 1, 1, 10, 15), '2 hours ago')

    # check2((2000, 1, 2, 12, 30), 'tomorrow at 12:30')
    # check2((1999, 12, 31, 12, 30), 'yesterday at 12:30')
    check2((2000, 1, 2, 12, 30), 'in a day')
    check2((1999, 12, 31, 12, 30), 'a day ago')

    check2((2000, 1, 3, 00, 01), 'in a day')
    check2((1999, 12, 30, 23, 59), 'a day ago')

    check2((2000, 1, 4, 00, 01), 'in 2 days')
    check2((1999, 12, 29, 23, 59), '2 days ago')

    check2((2000, 1, 4, 12, 30), 'in 3 days')
    check2((1999, 12, 29, 12, 30), '3 days ago')

    check2((2000, 1, 8, 12, 30), 'in a week')
    check2((1999, 12, 25, 12, 30), 'a week ago')

    check2((2000, 1, 9, 12, 30), 'in a week')
    check2((1999, 12, 24, 12, 30), 'a week ago')

    check2((2000, 1, 15, 12, 30), 'in 2 weeks')
    check2((1999, 12, 17, 12, 30), '2 weeks ago')

    check2((2001, 1, 1, 12, 30), 'in 52 weeks')
    check2((1999, 1, 1, 12, 30), '52 weeks ago')
