import pytest
import os
from hivery import create_app
from hivery.models import db, load_db_from_resources


@pytest.fixture(scope='session')
def app():
    app = create_app()
    with app.app_context():
        db.create_all()
        load_db_from_resources(os.path.join('hivery', 'tests', 'data'))
    return app


@pytest.fixture()
def client(app):
    client = app.test_client()

    return client


def test_status(client):
    """Check that the app is running by pinging the status endpoint"""
    rv = client.get('/status')
    assert rv.status_code == 200


class TestCompanyEmployees:
    LIST_ENDPOINT = "/api/company/"
    ENDPOINT = "/api/company/{}/employees"

    def test_invalid_company_id(self, client):
        """Invalid company id should 404"""
        ep = self.ENDPOINT.format(99999999999)
        rv = client.get(ep)
        assert rv.status_code == 404
    
    def test_no_employees(self, client):
        """Company with no employees should return empty list"""
        ep = self.ENDPOINT.format(0)
        rv = client.get(ep)
        assert rv.status_code == 200
        json = rv.get_json()
        assert isinstance(json, list)
        assert len(json) == 0

    def test_employees(self, client):
        """Company with any employees should return them in a list"""
        ep = self.ENDPOINT.format(1)
        rv = client.get(ep)
        assert rv.status_code == 200
        json = rv.get_json()
        assert isinstance(json, list)
        assert len(json) > 0


class TestPersonCommonFriends:
    ENDPOINT = "/api/person/{}/common_friends/{}"

    @staticmethod
    def _check_structure(data, person_a, person_b):
        assert data['person_a']['index'] == person_a
        assert data['person_b']['index'] == person_b
        assert isinstance(data['friends'], list)

    def test_invalid_ids(self, client):
        """If either id is invalid 404"""
        ep = self.ENDPOINT.format(9999999, 1)
        rv = client.get(ep)
        assert rv.status_code == 404

        ep = self.ENDPOINT.format(1, 9999999)
        rv = client.get(ep)
        assert rv.status_code == 404
    
    def test_no_filters(self, client):
        """Test that mutual friends appear without query arg filters"""
        person_a = 0
        person_b = 1
        ep = self.ENDPOINT.format(person_a, person_b)
        rv = client.get(ep)
        assert rv.status_code == 200

        data = rv.get_json()
        self._check_structure(data, person_a, person_b)
        assert len(data['friends']) > 0
    
    def test_filters(self, client):
        """Test that query arg filters work"""
        person_a = 0
        person_b = 2
        ep = self.ENDPOINT.format(person_a, person_b) + '?eye_color=brown&has_died=false'
        rv = client.get(ep)
        assert rv.status_code == 200

        data = rv.get_json()
        self._check_structure(data, person_a, person_b)
        friends = data['friends']
        assert len(friends) == 1
        for friend in friends:
            ep_friend = '/api/person/{}'.format(friend['index'])
            rv_friend = client.get(ep_friend)
            json = rv_friend.get_json()
            assert json['eyeColor'] == 'brown'
            assert json['has_died'] == False


class TestFavouriteFoods:
    ENDPOINT = "/api/person/{}/favourite_foods"

    def test_invalid_person(self, client):
        ep = self.ENDPOINT.format(9999999)
        rv = client.get(ep)
        assert rv.status_code == 404

    def test_no_food(self, client):
        person_id = 0
        ep = self.ENDPOINT.format(person_id)
        rv = client.get(ep)
        assert rv.status_code == 200

        data = rv.get_json()
        for key in ['fruits', 'vegetables']:
            assert key in data
            assert isinstance(data[key], list)
            assert len(data[key]) == 0
    
    def test_food(self, client):
        person_id = 1
        ep = self.ENDPOINT.format(person_id)
        rv = client.get(ep)
        assert rv.status_code == 200

        data = rv.get_json()
        expected = {
            'fruits': ['apple', 'banana'],
            'vegetables': ['beetroot', 'carrot', 'celery'],
        }
        for key in expected:
            assert key in data
            assert isinstance(data[key], list)
            assert len(data[key]) == len(expected[key])
            for item in data[key]:
                assert item in expected[key]
