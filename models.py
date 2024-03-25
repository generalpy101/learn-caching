from .app import db


class Notes(db.Model):
    __tablename__ = "notes"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    body = db.Column(db.Text)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now()
    )

    def __init__(self, *args, **kwargs) -> None:
        for key in kwargs:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])

    def __repr__(self) -> str:
        return f"<Note {self.title}>"

    def to_dict(self) -> dict:
        res = {}
        for key in self.__mapper__.c.keys():
            if not key.startswith("_"):
                res[key] = getattr(self, key)

        return res
