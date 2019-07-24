import logging

from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView

from api.models import Article


class ArticlesView(MethodView):

    def get(self, article_id):
        if article_id:
            article = Article.find_first(id=article_id)
            if not article:
                response = {
                    'status': 'fail',
                    'message': 'Article does not exist'
                }
                return make_response(jsonify(response)), 400

            response = {
                'status': 'success',
                'article': article.serialize()
            }
            return make_response(jsonify(response)), 200

        articles = Article.fetch_all()
        if not articles:
            response = {
                'status': 'success',
                'message': 'No articles have been added'
            }
            return make_response(jsonify(response)), 200

        response = {
            'status': 'success',
            'articles': [article.serialize() for article in articles]
        }
        return make_response(jsonify(response)), 200

    def post(self):
        pass
