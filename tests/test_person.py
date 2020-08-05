from unittest import TestCase

from app import app, db
from models import Person, PersonArchive


class TestPerson(TestCase):

    TEST_DB_URI = "sqlite:///person-test.db"
    TESTING = True
    NUM_PERSONS = 5

    def _format_name(self, i):
        return "Name{}".format(i)

    def _make_person(self, first_name, version):
        return Person(
            first_name=first_name,
            last_name="lastname",
            email="email",
            age=100,
            version=version,
        )

    def _make_person_archive(self, first_name, person_id, version):
        return PersonArchive(
            first_name=first_name,
            last_name="lastname",
            email="email",
            age=100,
            version=version,
            person_id=person_id,
        )

    def _init_data(self):
        # Test data:
        # These are person rows with names formatted as "Name<i>".
        # Each person has i+1 versions. The previous versions had "Name<j>" where j is the version number.
        for i in range(self.NUM_PERSONS):
            p = self._make_person(self._format_name(i), i + 1)
            db.session.add(p)
            db.session.flush()
            db.session.add(self._make_person_archive(p.first_name, p.id, p.version))
            for j in range(1, i + 1):
                db.session.add(self._make_person_archive(self._format_name(j), p.id, j))
        db.session.commit()

    def setUp(self):
        app.config["SQLALCHEMY_DATABASE_URI"] = self.TEST_DB_URI
        self.app = app.test_client()
        db.create_all()
        self._init_data()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_list_all_persons(self):
        response = self.app.get("/persons")
        assert response.status_code == 200
        assert set(map(lambda p: p["id"], response.json)) == set(
            range(1, self.NUM_PERSONS + 1)
        )

    def test_create_person(self):
        person_data = {"first_name": "E"}
        response = self.app.post("/persons", json=person_data)
        assert response.status_code == 400

        person_data = {"first_name": "E", "last_name": "", "email": "", "age": 0}
        response = self.app.post("/persons", json=person_data)
        assert response.status_code == 201

        p = Person.query.get(response.json["id"])
        assert p.first_name == "E"
        assert p.version == 1
        p_archive_all = PersonArchive.query.filter_by(person_id=p.id).all()
        assert len(p_archive_all) == 1
        p_archive = p_archive_all[0]
        assert p_archive != None
        assert p_archive.first_name == p.first_name
        assert p_archive.version == p.version
        assert p_archive.person_id == p.id

    def test_read_person(self):
        for i in range(self.NUM_PERSONS):
            response = self.app.get("/persons/{}".format(i + 1))
            assert response.status_code == 200
            assert response.json["id"] == i + 1
            assert response.json["first_name"] == self._format_name(i)
        response = self.app.get("/persons/100")
        assert response.status_code == 404

    def test_read_person_version(self):
        for version in range(1, self.NUM_PERSONS):
            response = self.app.get("/persons/{}/{}".format(self.NUM_PERSONS, version))
            assert response.status_code == 200
            assert response.json["id"] == self.NUM_PERSONS
            assert response.json["first_name"] == self._format_name(version)
        response = self.app.get("/persons/100/1")
        assert response.status_code == 404

    def test_put_person(self):
        person_data = {"first_name": "E"}
        response = self.app.put("/persons/1", json=person_data)
        assert response.status_code == 400

        person_data = {"first_name": "E", "last_name": "", "email": "", "age": 0}
        old_version = Person.query.get(1).version
        response = self.app.put("/persons/1", json=person_data)
        assert response.status_code == 204
        p = Person.query.get(1)
        assert p.first_name == "E"
        assert p.last_name == ""
        assert p.age == 0
        assert p.version == old_version + 1
        p_archive = PersonArchive.query.filter_by(
            person_id=1, version=p.version
        ).first()
        assert p_archive.first_name == p.first_name
        assert p_archive.version == p.version
        p_archive_prev = PersonArchive.query.filter_by(
            person_id=1, version=old_version
        ).first()
        assert p_archive_prev.first_name == self._format_name(0)

    def test_patch_person(self):
        old_version = Person.query.get(1).version
        old_age = Person.query.get(1).age
        response = self.app.patch("/persons/1", json={"first_name": "E"})
        assert response.status_code == 204
        p = Person.query.get(1)
        assert p.first_name == "E"
        assert p.age == old_age
        assert p.version == old_version + 1
        p_archive = PersonArchive.query.filter_by(
            person_id=1, version=p.version
        ).first()
        assert p_archive.first_name == p.first_name
        assert p_archive.version == p.version
        p_archive_prev = PersonArchive.query.filter_by(
            person_id=1, version=old_version
        ).first()
        assert p_archive_prev.first_name == self._format_name(0)

    def test_delete_then_create(self):
        old_highest_id = Person.query.get(self.NUM_PERSONS).id
        response = self.app.delete("/persons/{}".format(self.NUM_PERSONS))
        assert response.status_code == 204
        person_data = {"first_name": "E"}
        response = self.app.post("/persons", json=person_data)
        assert Person.query.filter_by(id=old_highest_id).first() == None
        assert PersonArchive.query.filter_by(person_id=old_highest_id).first() != None


if __name__ == "__main__":
    unittest.main()
