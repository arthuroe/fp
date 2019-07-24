import logging

from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView

from api.decorators import token_required
from api.models import Article


class ArticlesView(MethodView):
    """
    View to handle Articles
    """
    decorators = [token_required]

    def get(self, article_id=None):
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
        kwargs = request.json
        title = kwargs.get('title')
        body = kwargs.get('body')

        if not all([title, body]):
            response = {
                'status': 'fail',
                'message': 'Incomplete data. All fields are required'
            }
            return make_response(jsonify(response)), 400

        try:
            article = Article(**kwargs)
            article.save()
            response = {
                'status': 'success',
                'message': f'Successfully added {title}'
            }
            return make_response(jsonify(response)), 201

        except Exception as e:
            logging.error(f"An error has occurred  {e}")
            response = {
                'status': 'fail',
                'message': 'Failed to create Article.'
            }
            return make_response(jsonify(response)), 400

    def put(self, article_id):
        kwargs = request.json
        article = Article.find_first(id=article_id)

        if not article:
            response = {
                'status': 'Fail',
                'message': 'Article does not exist'
            }
            return make_response(jsonify(response)), 400

        try:

            article.update(**kwargs)
            response = {
                'status': 'success',
                'message': f'Successfully updated {title}'
            }
            return make_response(jsonify(response)), 200

        except Exception as e:
            logging.error(f"An error has occurred  {e}")
            response = {
                'status': 'fail',
                'message': 'Failed to update Article.'
            }
            return make_response(jsonify(response)), 400

    def delete(self):
        pass
