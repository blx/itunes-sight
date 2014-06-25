from flask import Flask as Flask_orig
from werkzeug.datastructures import ImmutableDict

# Override the Flask class to add options to Jinja2 config.
class Flask(Flask_orig):
    jinja_options = ImmutableDict({
        'extensions': Flask_orig.jinja_options['extensions'],
        'trim_blocks': True,
        'lstrip_blocks': True,
        'line_statement_prefix': '$'
    })

app = Flask(__name__)


# Do this now that we've created the app object
import sight.routes