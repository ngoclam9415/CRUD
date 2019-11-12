from sqlalchemy import func
from app import db


def get_count(models):
    count = db.session.execute(models.query.statement.with_only_columns([
                               func.count()]).order_by(None)).scalar()
    return count
