"""
Initialize Flask app

"""
import os
import sys

ROOT_PATH = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
LIB_PATH = os.path.join(os.path.dirname(ROOT_PATH), 'lib')
SITEPACKAGES_PATH = os.path.join(LIB_PATH, 'site-packages')
sys.path.insert(0, LIB_PATH)
sys.path.insert(0, SITEPACKAGES_PATH)


print sys.path

from flask import Flask

from flask_debugtoolbar import DebugToolbarExtension
from gae_mini_profiler import profiler, templatetags
from werkzeug.debug import DebuggedApplication


app = Flask('application')
app.config.from_object('application.settings')

# Enable jinja2 loop controls extension
app.jinja_env.add_extension('jinja2.ext.loopcontrols')

@app.context_processor
def inject_profiler():
    return dict(profiler_includes=templatetags.profiler_includes())

# Pull in URL dispatch routes
import urls
import views

# Flask-DebugToolbar (only enabled when DEBUG=True)
# toolbar = DebugToolbarExtension(app)

# Werkzeug Debugger (only enabled when DEBUG=True)
if app.debug:
    app = DebuggedApplication(app, evalex=True)

# GAE Mini Profiler (only enabled on dev server)
app = profiler.ProfilerWSGIMiddleware(app)

