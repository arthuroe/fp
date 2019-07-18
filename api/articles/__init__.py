from flask import Blueprint

from api.articles.views import ArticlesView

articles_blueprint = Blueprint('articles', __name__, url_prefix='/api/v1')
articles_view = ArticlesView.as_view('articles_api')

articles_blueprint.add_url_rule(
    '/articles', view_func=articles_view, methods=['POST', 'GET'])
