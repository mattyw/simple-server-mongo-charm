import gobinary

from charmhelpers.core import hookenv
from charms.reactive import when


@when('gobinary.started')
def simple_server_start():
    hookenv.open_port(8080)
    hookenv.status_set('active', 'Ready')


@when('website.available')
def configure_website(website):
    config = hookenv.config()
    website.configure(8080)
