from mwp_client import mwp_room_client


def process_message(message_data):
    # Process the message through my plugins
    mwp_room_client.send_notification(
        'TODO: Process room_message ({md.message_text})'.format(
            md=message_data
        )
    )


def load_plugins():
    # TODO: Load all plugins in this directory
    pass
