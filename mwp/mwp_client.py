# A send_notification implementation that accepts (some) arguments
from ac_flask.hipchat import clients


class MWPRoomClient(object):
    @staticmethod
    def send_notification(
            message,
            #html, text
            message_format='text',
            # yellow, green, red, purple, gray, random.
            color='purple',
            # True, False
            notify=False,
        ):
        url = '%s/room/%s/notification' % (clients.tenant.api_base_url, clients.tenant.room_id)
        token = clients.tenant.get_token(clients.redis)
        return clients.post(
            url,
            {
                'message': message,
                'message_format': message_format,
                'color': color,
                'notify': notify,
            },
            token
        )


mwp_room_client = MWPRoomClient()
