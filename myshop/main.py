from aiohttp import web
import aiohttp_jinja2
import jinja2

from settings import config
from routes import setup_routes
from db import close_pg, init_pg

app = web.Application()
setup_routes(app)
app['config'] = config

# setup Jinja2 template renderer and static_root_url
aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('templates'))
app['static_root_url'] = '/static'

# create db connection on startup, shutdown on exit
app.on_startup.append(init_pg)
app.on_cleanup.append(close_pg)

web.run_app(app)
