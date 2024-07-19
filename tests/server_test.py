import json
from core import app
from core.libs.exceptions import FyleError
from marshmallow.exceptions import ValidationError
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import NotFound
import pytest

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_ready(client):
    response = client.get('/')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'ready'
    assert 'time' in data

def test_handle_fyle_error(client):
    @app.route('/test-fyle-error')
    def test_fyle_error():
        raise FyleError(message='This is a FyleError', status_code=418)

    response = client.get('/test-fyle-error')
    assert response.status_code == 418
    data = json.loads(response.data)
    assert data['error'] == 'FyleError'
    assert data['message'] == 'This is a FyleError'

def test_handle_validation_error(client):
    @app.route('/test-validation-error')
    def test_validation_error():
        # Raise ValidationError with a specific structure
        raise ValidationError({'field': ['This is a validation error']})

    response = client.get('/test-validation-error')
    assert response.status_code == 400
    data = json.loads(response.data)

    assert data['error'] == 'ValidationError'
    # Handle message as a nested dictionary
    assert 'This is a validation error' in data['message']['field']

def test_handle_integrity_error(client):
    @app.route('/test-integrity-error')
    def test_integrity_error():
        raise IntegrityError(statement='some statement', params=None, orig='Integrity constraint violation')

    response = client.get('/test-integrity-error')
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['error'] == 'IntegrityError'
    assert data['message'] == 'Integrity constraint violation'

def test_handle_http_exception(client):
    @app.route('/test-http-exception')
    def test_http_exception():
        raise NotFound(description='Resource not found')

    response = client.get('/test-http-exception')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data['error'] == 'NotFound'
    assert data['message'] == '404 Not Found: Resource not found'

def test_handle_generic_exception(client):
    @app.route('/test-generic-exception')
    def test_generic_exception():
        raise Exception('Generic error')

    with pytest.raises(Exception, match='Generic error'):
        client.get('/test-generic-exception')
