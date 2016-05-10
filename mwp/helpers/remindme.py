import datetime

from time_parser import TimeParser
from time_summariser import TimeSummariser


class RemindMe(object):
    USAGE_MESSAGE = '!remindme {interval} [at {time}] [[to] {description}]'
    EXAMPLES = [
        '!remindme 30m',
        '!remindme tomorrow to Tell PO about new ticket',
        '!remindme next Thursday at 10am Move backlog grooming',
        '!remindme 1 year Jay\'s birthday!',
    ]


    def __init__(self, load_data, save_data):
        self.load_data = load_data
        self.save_data = save_data
        self.time_parser = TimeParser()
        self.time_summariser = TimeSummariser()

    def add_reminder(self, message_data, text, now=None):
        """
        Given an input that can be parsed by ParseTime, add that to the list of reminders
        and return the parsed info.
        """
        # Parse the reminder info
        reminder_info = self.time_parser.parse_time_string(text, now=now)

        # Setup the reminder
        if reminder_info:
            # Save some info about the message
            reminder_info['message'] = {
                'date': message_data.date,
                'user_id': message_data.user_id,
                'user_name': message_data.user_name,
                'user_mention_name': message_data.user_mention_name,
                'message_text': message_data.message_text,
                'room_id': message_data.room_id,
                'room_name': message_data.room_name,
            }

            # Add the reminder to the store
            store = self.load_data(default=[])
            store.append(reminder_info)
            self.save_data(store)

        # Let the callee know what we've done
        return reminder_info

    def summarise(self, reminder_info):
        """
        Summarise the given reminder in a human-readable way
        """
        return self.time_summariser.summarise(reminder_info)

    def get_reminders(self):
        """
        Get all the reminders I know about
        """
        return self.load_data(default=[])

    def get_past_reminders(self, now=None):
        """
        Get all the reminders that should have been done by now
        """
        now = now or datetime.datetime.now()
        store = self.load_data(default=[])
        return [
            reminder_info
            for reminder_info in store
            if reminder_info['datetime'] < now
        ]

    def remove_reminders(self, reminder_infos):
        """
        Remove the given reminders from my store
        """
        for reminder_info in reminder_infos:
            self.remove_reminder(reminder_info)

    def remove_reminder(self, reminder_info):
        """
        Remove the given reminder from my store
        """
        store = self.load_data(default=[])
        if reminder_info in store:
            index = store.index(reminder_info)
            del store[index]
        self.save_data(store)

    def clear(self):
        """
        Clear all reminders
        """
        self.save_data([])


if __name__ == '__main__':
    import pickle
    store = {}
    def load_data(default=None, key='default'):
        return pickle.loads(store.get(key, pickle.dumps(default)))
    def save_data(value, key='default'):
        store[key] = pickle.dumps(value)

    import collections
    MessageInfo = collections.namedtuple(
        'MessageInfo',
        (
            'date',
            'user_id',
            'user_name',
            'user_mention_name',
            'message_mentions',
            'message_text',
            'room_id',
            'room_name',
            'room_members_link',
            'room_participants_link',
        )
    )
    message_data = MessageInfo(
        date='date',
        user_id='user_id',
        user_name='user_name',
        user_mention_name='user_mention_name',
        message_mentions='message_mentions',
        message_text='message_text',
        room_id='room_id',
        room_name='room_name',
        room_members_link='room_members_link',
        room_participants_link='room_participants_link',
    )

    rm = RemindMe(load_data, save_data)

    def check_add(
            text,
            expected_datetime,
            expected_description,
            expected_store_count,
            now=(2000,1,1,12,30)
        ):
        print 'Add:', text, '...'
        reminder_info = rm.add_reminder(
            message_data,
            text,
            now=datetime.datetime(*now)
        )

        # Check the datetime
        expected_datetime = datetime.datetime(*expected_datetime)
        if expected_datetime != reminder_info['datetime']:
            print 'FAILED - Datetime'
            print '    Expected: ', expected_datetime
            print '    Actual  : ', reminder_info['datetime']

        # Check the descrition
        if expected_description != reminder_info['description']:
            print 'FAILED - Description'
            print '    Expected: ', expected_description
            print '    Actual  : ', reminder_info['description']

        # Check it was added to the store
        store = load_data()
        if store[-1] != reminder_info:
            print 'FAILED - Reminder not in store'
        if len(store) != expected_store_count:
            print 'FAILED - Store Count'
            print '    Expected: ', expected_store_count
            print '    Actual  : ', len(store)

        return reminder_info

    def check_remove(reminder_info, expected_store):
        print 'Remove:', reminder_info['description'], '...',
        rm.remove_reminder(reminder_info)

        # Check it was removed from the store
        store = load_data()
        if store != expected_store:
            print 'FAILED'
            print '    Expected: ', ' :: '.join([ri['description'] for ri in expected_store])
            print '    Actual  : ', ' :: '.join([ri['description'] for ri in store])
        else:
            print 'SUCCESS'

    def check_past(now, expected_past):
        print 'Past:', now, '...',
        past = rm.get_past_reminders(now=datetime.datetime(*now))

        # Check it was removed from the store
        if past != expected_past:
            print 'FAILED'
            print '    Expected: ', ' :: '.join([ri['description'] for ri in expected_past])
            print '    Actual  : ', ' :: '.join([ri['description'] for ri in past])
        else:
            print 'SUCCESS'

    rm_0 = check_add(
        'tomorrow at 2:30pm take out the trash',
        (2000,1,2,14,30),
        'take out the trash',
        1,
    )
    rm_1 = check_add(
        'tomorrow at 2:30pm take out the trash some more',
        (2000,1,2,14,30),
        'take out the trash some more',
        2,
    )
    rm_2 = check_add(
        'tomorrow at 10:30am to take out the trash earlier',
        (2000,1,2,10,30),
        'take out the trash earlier',
        3,
    )
    rm_3 = check_add(
        'tomorrow at 11:30am',
        (2000,1,2,11,30),
        '',
        4,
    )

    check_remove(
        rm_1,
        [rm_0, rm_2, rm_3]
    )

    check_past(
        (2000,1,2,9,45),
        []
    )
    check_past(
        (2000,1,2,10,45),
        [rm_2]
    )
    check_past(
        (2000,1,2,11,45),
        [rm_2, rm_3]
    )
    check_past(
        (2000,1,3,0,0),
        [rm_0, rm_2, rm_3]
    )

    check_remove(
        rm_3,
        [rm_0, rm_2]
    )
    check_remove(
        rm_0,
        [rm_2]
    )
    check_remove(
        rm_2,
        []
    )
