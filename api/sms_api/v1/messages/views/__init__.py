from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/v1/messages')

from v1.messages.views.index import *

