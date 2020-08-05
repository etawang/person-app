from app import db

PERSON_KEYS = ["id", "first_name", "middle_name", "last_name", "email", "age"]

class Person(db.Model):
    # We autoincrement explicitly to ensure that ids are never reused.
    # Reusing ids would break the association between the person_archive and person table.
    __table_args__ = {"sqlite_autoincrement": True}

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), nullable=False)
    middle_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(256), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    version = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "middle_name": self.middle_name,
            "last_name": self.last_name,
            "email": self.email,
            "age": self.age,
            "version": self.version,
        }

    def to_person(self):
        self_dict = self.to_dict()
        return {k: self_dict[k] for k in PERSON_KEYS}

    def __repr__(self):
        return str(self.to_dict())


class PersonArchive(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey("person.id"), nullable=False)
    first_name = db.Column(db.String(64), nullable=False)
    middle_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(256), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    version = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "person_id": self.person_id,
            "first_name": self.first_name,
            "middle_name": self.middle_name,
            "last_name": self.last_name,
            "email": self.email,
            "age": self.age,
            "version": self.version,
        }

    def to_person(self):
        self_dict = self.to_dict()
        self_dict["id"] = self_dict["person_id"]
        return {k: self_dict[k] for k in PERSON_KEYS}

    def __repr__(self):
        return str(self.to_dict())
