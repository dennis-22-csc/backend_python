from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/v1/oauth')

from v1.oauth.views.index import *
