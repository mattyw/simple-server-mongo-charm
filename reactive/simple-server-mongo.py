import gobinary

from charmhelpers.core import hookenv, host
from charmhelpers.core.templating import render
from charms.reactive import hook, when, when_not, is_state, set_state, remove_state
from charms.reactive.bus import get_states


@when('gobinary.started', 'database.database.available')
def simple_server_start(_):
    hookenv.open_port(8080)
    hookenv.status_set('active', 'Ready')


@when('website.available')
def configure_website(website):
    config = hookenv.config()
    website.configure(8080)


@when('gobinary.start')
@when_not('database.connected')
def missing_db():
    hookenv.log("%s" % (str(get_states())))
    remove_state('gobinary.start')
    hookenv.status_set('blocked', 'Please add relation to mongodb')


@when('database.connected')
@when_not('database.database.available')
def waiting_db(pg):
    hookenv.log("%s" % (str(get_states())))
    remove_state('gobinary.start')
    hookenv.status_set('waiting', 'Waiting for mongodb')


@when('database.connected', 'database.database.available')
def setup(db, _):
    bin_config = gobinary.config()

    remove_state('gobinary.start')
    if is_state('gobinary.started'):
        host.service_stop(bin_config['binary'])

    config = hookenv.config()
    render(source="config.yaml",
        target="/etc/myserver/config.yaml",
        owner="root",
        perms=0o644,
        context={
            'cfg': config,
            'db': db,
        })

    set_state('gobinary.start')
    if is_state('gobinary.started'):
        host.service_start(bin_config['binary'])
    else:
        hookenv.status_set('maintenance', 'Starting server')
