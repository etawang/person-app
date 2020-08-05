import copy

from app import db
from models import Person, PersonArchive


class PersonService:
    def create(self, params):
        params["version"] = 1
        p = Person(**params)
        db.session.add(p)
        db.session.flush()

        p_archive = PersonArchive(**params)
        p_archive.person_id = p.id
        db.session.add(p_archive)
        db.session.commit()
        return {"id": p.id}

    def read(self, person_id):
        return Person.query.get_or_404(person_id).to_person()

    def read_all(self):
        return list(map(lambda p: p.to_person(), Person.query.all()))

    def read_version(self, person_id, version):
        return (
            PersonArchive.query.filter_by(person_id=person_id, version=version)
            .first_or_404()
            .to_person()
        )

    def overwrite(self, person_id, params):
        p = Person.query.get_or_404(person_id)
        p.first_name = params["first_name"]
        p.middle_name = params.get("middle_name", None)
        p.last_name = params["last_name"]
        p.email = params["email"]
        p.age = params["age"]
        p.version += 1
        p_archive = PersonArchive(**params)
        p_archive.version = p.version
        p_archive.person_id = p.id
        db.session.add(p_archive)
        db.session.commit()
        return

    def _update_fields(self, p, params):
        for k, v in params.items():
            if k == "first_name":
                p.first_name = v
            elif k == "middle_name":
                p.middle_name = v
            elif k == "last_name":
                p.last_name = v
            elif k == "email":
                p.email = v
            elif k == "age":
                p.age = v

    def update(self, person_id, params):
        p = Person.query.get_or_404(person_id)
        p.version += 1
        self._update_fields(p, params)

        p_archive = PersonArchive(**p.to_dict())
        p_archive.id = None
        p_archive.person_id = p.id
        db.session.add(p_archive)
        db.session.commit()
        return

    def delete(self, person_id):
        p = Person.query.get_or_404(person_id)
        db.session.delete(p)
        db.session.commit()
        return
