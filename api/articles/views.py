import logging

from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView

from api.decorators import admin_required, token_required
from api.models import Article


class ArticlesView(MethodView):
    """
    View to handle Articles
    """

    def get(self, article_id=None):
        if article_id:
            article = Article.find_first(id=article_id)
            if not article:
                response = {
                    'status': 'fail',
                    'message': 'Article does not exist'
                }
                return make_response(jsonify(response)), 404

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

    @token_required
    @admin_required
    def post(self, current_user):
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
            return make_response(jsonify(response)), 500

    @token_required
    @admin_required
    def put(self, current_user, article_id):
        kwargs = request.json
        kwargs.update({'id': article_id})
        article = Article.find_first(id=article_id)

        if not article:
            response = {
                'status': 'Fail',
                'message': 'Article does not exist'
            }
            return make_response(jsonify(response)), 404

        try:
            article.update(**kwargs)
            response = {
                'status': 'success',
                'message': f'Successfully updated {article.title}'
            }
            return make_response(jsonify(response)), 200

        except Exception as e:
            logging.error(f"An error has occurred  {e}")
            response = {
                'status': 'fail',
                'message': 'Failed to update Article.'
            }
            return make_response(jsonify(response)), 500

    @token_required
    @admin_required
    def delete(self, current_user, article_id):
        article = Article.find_first(id=article_id)

        if not article:
            response = {
                'status': 'Fail',
                'message': 'Article does not exist'
            }
            return make_response(jsonify(response)), 404

        try:
            article.delete()
            response = {
                'status': 'Success',
                'message': 'Deleted article'
            }
            return make_response(jsonify(response)), 200

        except Exception as e:
            logging.error(f"An error has occurred  {e}")
            response = {
                'status': 'fail',
                'message': 'Failed to delete article.'
            }
            return make_response(jsonify(response)), 500
