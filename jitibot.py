#!/bin/python3

from mastodon   import Mastodon
from time       import sleep
from getpass    import getpass
from webbrowser import open_new_tab
from signal     import signal


jiti_instance = "https://jitsi.tildeverse.org/"

instance  = input("Instance name:\n")
email     = input("email:\n")
password  = getpass("Password:")
jiti_name = jiti_instance + input("Name for the jiti:\n")

toot_message = f"its time for another fucken jiti!!!\n\
                 {jiti_name}\n\
                 join now or die!!!!!"

if instance[:8] != "https://":
    instance = "https://" + instance

Mastodon.create_app(
    'jitibot',
    api_base_url=instance,
    to_file='jitibot_clientcred.secret'
)

mastodon = Mastodon(
    client_id='jitibot_clientcred.secret',
    api_base_url=instance
)

mastodon.log_in(
    email,
    password,
    to_file='jitibot_usercred.secret'
)

mastodon = Mastodon(
    access_token='jitibot_usercred.secret',
    api_base_url=instance
)

open_new_tab(jiti_name)

data = mastodon.status_post(status=toot_message, in_reply_to_id=None, media_ids=None, sensitive=False, visibility='private', spoiler_text=None, language=None, idempotency_key=None, content_type=None, scheduled_at=None, poll=None, quote_id=None)

def deletetoot(id):
    mastodon.status_delete(id)


signal(signal.SIGINT, deletetoot(data['id']))

while True:
    sleep(30)
    mastodon.status_reblog(id=data['id'])
