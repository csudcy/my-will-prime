import datetime
import re


class TimeParser(object):
    TOMORROW_RE = r'^tomm?orr?ow(?P<remaining>.*)$'
    RELATIVE_RE = r'^(?P<next>next )?(?P<day>(mon|tues?|wednes|wed|thurs|thu|fri|satur|sat|sun)(day)?)(?P<remaining>.*)$'
    WEEKDAYS = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
    INTERVAL_RE = r'^(?P<count>(\d+|a)) ?(?P<interval>(minutes?|mins?|m|hours?|h|days?|d|weeks?|w|years?|y))(?P<remaining>.*)$'
    INTERVALS = {
        'm': 'minutes',
        'h': 'hours',
        'd': 'days',
        'w': 'weeks',
    }

    # TIME_RE = r'^at (?P<time>\d\d?:?\d?\d?(am|pm)?)(?P<remaining>.*)$'
    TIME_MIL_RE = '^(?P<hours>\d\d)(?P<mins>\d\d)(?P<remaining>.*)$'
    TIME_CLOCK_RE = '^(?P<hours>\d\d?)(:(?P<mins>\d\d?))?(?P<ampm>(a|p)m?)?( (?P<remaining>.*))?$'

    def parse_time_string(self, text, now=None):
        now = now or datetime.datetime.now()

        # Parse the date
        dt, description = self._parse_date(text, now)

        # Parse the time
        description = description.strip()
        if description[:3] == 'at ':
            dt, description = self._parse_time(description[3:], dt)
        else:
            # No time; check if it should be midday
            if dt.hour == 0 and dt.minute == 0:
                # Assume this was a "tomorrow" with no time; set it to midday
                dt = dt.replace(hour=12)

        # Check parsing didn't fail
        if dt == now:
            return None

        # Remove 'to ' from the description (if it's there)
        description = description.strip()
        if description[:3] == 'to ':
            description = description[3:].strip()

        # All done!
        return {
            'datetime': dt,
            'description': description,
        }

    def _parse_date(self, text, now):
        # Is this "tomorrow..."?
        match_tomorrow = re.match(self.TOMORROW_RE, text, re.IGNORECASE)
        if match_tomorrow:
            # Add on a day
            now += datetime.timedelta(days=1)
            # But start from midnight
            now = now.replace(hour=0, minute=0)
            return now, match_tomorrow.group(1)

        # Is this "[next] Tuesday..."?
        match_relative = re.match(self.RELATIVE_RE, text, re.IGNORECASE)
        if match_relative:
            match_relative_dict = match_relative.groupdict()

            # Move to the next day which matches
            day = match_relative_dict['day'][:3].lower()
            day_number = self.WEEKDAYS.index(day)
            days_to_add = (day_number - now.weekday() + 7) % 7
            if days_to_add == 0:
                # The day they want is the same as today (e.g. today is Tuesday & they want Monday)
                days_to_add += 7
            elif match_relative_dict['next']:
                # Move another week forward
                days_to_add += 7
            now += datetime.timedelta(days=days_to_add)
            assert now.weekday() == day_number

            return now, match_relative_dict['remaining']

        # Is this "[count] [interval]..."?
        match_interval = re.match(self.INTERVAL_RE, text, re.IGNORECASE)
        if match_interval:
            match_interval_dict = match_interval.groupdict()
            
            # Get the count
            if match_interval_dict['count'].lower() == 'a':
                count = 1
            else:
                count = int(match_interval_dict['count'])
            
            # Get the interval
            interval = match_interval_dict['interval'][:1].lower()

            # Do it
            if interval == 'y':
                # Handle years specially
                # See http://stackoverflow.com/questions/15741618/add-one-year-in-current-date-python
                """
                Return a date that's `years` years after the date (or datetime)
                object `d`. Return the same calendar date (month and day) in the
                destination year, if it exists, otherwise use the following day
                (thus changing February 29 to March 1).
                """
                try:
                    now = now.replace(year = now.year + count)
                except ValueError:
                    now += (datetime.date(now.year + count, 1, 1) - datetime.date(now.year, 1, 1))
            else:
                now += datetime.timedelta(**{
                    self.INTERVALS[interval]: count
                })

            return now, match_interval_dict['remaining']

        # Couldn't parse it
        return now, text

    def _parse_time(self, text, now):
        def set_hm(now, hours, minutes):
            if hours > 24:
                # Invalid, abort
                return now
            if mins >= 60:
                # Invalid, abort
                return now
            then = now.replace(hour=hours, minute=mins)
            if then < now:
                then += datetime.timedelta(days=1)
            return then

        # Is this "12[:34][pm]..."?
        match_clock = re.match(self.TIME_CLOCK_RE, text, re.IGNORECASE)
        if match_clock:
            match_clock_dict = match_clock.groupdict()
            
            # Work out hours
            hours = int(match_clock_dict['hours'])
            if match_clock_dict['ampm'] and match_clock_dict['ampm'][0].lower() == 'p':
                hours += 12

            # Work out the minutes
            mins = 0
            if match_clock_dict['mins']:
                mins = int(match_clock_dict['mins'])

            return set_hm(now, hours, mins), match_clock_dict['remaining'] or ''

        # Is this "1430..."?
        match_mil = re.match(self.TIME_MIL_RE, text, re.IGNORECASE)
        if match_mil:
            match_mil_dict = match_mil.groupdict()

            # Work out hours
            hours = int(match_mil_dict['hours'])
            mins = int(match_mil_dict['mins'])
            return set_hm(now, hours, mins), match_mil_dict['remaining']

        # Couldn't parse it
        return now, text


if __name__ == '__main__':
    tp = TimeParser()
    def check(text, dt=None, description='', now=(2000,1,1,12,30)):
        print text, '...',
        parsed = tp.parse_time_string(text, now=datetime.datetime(*now))

        # Work out what we're expecting
        if dt is None:
            expected = None
        else:
            expected = {
                'datetime': datetime.datetime(*dt),
                'description': description
            }

        # Check what we got
        if expected != parsed:
            print 'FAILED'
            print '    Expected: ', expected
            print '    Actual  : ', parsed
        else:
            print 'SUCCESS'

    def check2(text, dt):
        check(text, dt, '')
        check(text+' I can haz description', dt, 'I can haz description')

    # Fail
    check('This is not a datetime')

    # Relative
    check2('tomorrow', (2000,1,2,12,00))
    check2('Tommorow', (2000,1,2,12,00))
    check2('Sunday', (2000,1,2,12,30))
    check2('Tuesday', (2000,1,4,12,30))
    check2('Saturday', (2000,1,8,12,30))
    check2('NEXT Sunday', (2000,1,9,12,30))
    check2('NEXT Tuesday', (2000,1,11,12,30))
    check2('NEXT Saturday', (2000,1,8,12,30))

    # Interval
    check2('15m', (2000,1,1,12,45))
    check2('15 Min', (2000,1,1,12,45))
    check2('15mins', (2000,1,1,12,45))
    check2('15 MINUTES', (2000,1,1,12,45))
    check2('525600m', (2000,12,31,12,30))
    check2('1h', (2000,1,1,13,30))
    check2('24h', (2000,1,2,12,30))
    check2('1d', (2000,1,2,12,30))
    check2('7d', (2000,1,8,12,30))
    check2('1w', (2000,1,8,12,30))
    check2('52w', (2000,12,30,12,30))
    check2('1y', (2001,1,1,12,30))
    check2('10y', (2010,1,1,12,30))

    # Clock times
    check2('at 2pm', (2000,1,1,14,00))
    check2('at 2:45pm', (2000,1,1,14,45))
    check2('at 02pm', (2000,1,1,14,00))
    check2('at 02:45pm', (2000,1,1,14,45))
    check2('at 14', (2000,1,1,14,00))
    check2('at 14:45', (2000,1,1,14,45))
    check2('at 2am', (2000,1,2,2,00))
    check2('at 2:45am', (2000,1,2,2,45))
    check2('at 2', (2000,1,2,2,00))
    check2('at 2:45', (2000,1,2,2,45))
    check2('at 02am', (2000,1,2,2,00))
    check2('at 02:45am', (2000,1,2,2,45))
    check2('at 02', (2000,1,2,2,00))
    check2('at 02:45', (2000,1,2,2,45))
    check('at 25')
    check('at 23:60')
    check('at 13:00pm')

    # Military times
    check('at 1445', (2000,1,1,14,45))
    check('at 1000', (2000,1,2,10,00))
    check('at 2500')
    check('at 2360')

    # Complex examples
    check2(
        'tomorrow at 10:30',
        (2000,1,2,10,30)
    )
    check(
        'tomorrow to Tell PO about new ticket',
        (2000,1,2,12,00),
        'Tell PO about new ticket'
    )
    check(
        'next Saturday at 5:45pm Get ready to party',
        (2000,1,8,17,45),
        'Get ready to party'
    )
    check(
        'Thursday at 10am Move backlog grooming',
        (2000,1,7,10,00),
        'Move backlog grooming'
    )
    check(
        '1 year Jay\'s birthday!',
        (2001,1,1,12,30),
        'Jay\'s birthday!'
    )
