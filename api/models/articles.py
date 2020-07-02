from api.models import db, ModelMixin


class Article(ModelMixin):
    """
    Article model attributes
    """
    __tablename__ = 'articles'

    title = db.Column(db.String(120), nullable=False)
    body = db.Column(db.String(8000))
    is_highlight = db.Column(db.Boolean, default=False)
    image = db.Column(db.String(180))
