from app.extensions import db
from app.models import Major


class MajorRepository:

    @staticmethod
    def get_by_id(major_id):
        return db.session.get(
            Major,
            major_id
        )