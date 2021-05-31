from flask import Blueprint

from api.articles.views import ArticlesView, ArticleView, HighlightsView

articles_blueprint = Blueprint('articles', __name__, url_prefix='/api/v1')
articles_view = ArticlesView.as_view('articles_api')
highlight_view = HighlightsView.as_view('highlights_api')
article_view = ArticleView.as_view('article_api')

articles_blueprint.add_url_rule(
    '/articles', view_func=articles_view, methods=['POST', 'GET'])
articles_blueprint.add_url_rule(
    '/articles/<article_id>', view_func=articles_view,
    methods=['GET', 'PUT', 'DELETE']
)

articles_blueprint.add_url_rule(
    '/highlight', view_func=highlight_view,
    methods=['GET']
)

articles_blueprint.add_url_rule(
    '/article', view_func=article_view,
    methods=['GET']
)
