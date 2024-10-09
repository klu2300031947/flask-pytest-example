import json
from flask import Flask
from flask_pytest_example.handlers.routes import configure_routes

def test_base_route():
    """Test the base route (GET request to '/')"""
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/'

    # Test the base route
    response = client.get(url)
    assert response.get_data() == b'Hello, World!'
    assert response.status_code == 200


def test_post_route__success():
    """Test successful POST request to /post/test"""
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/post/test'

    # Mock request headers and data for a successful request
    mock_request_headers = {
        'authorization-sha256': '123'
    }

    mock_request_data = {
        'request_id': '123',
        'payload': {
            'py': 'pi',
            'java': 'script'
        }
    }

    response = client.post(url, data=json.dumps(mock_request_data), headers=mock_request_headers)
    assert response.status_code == 200
    response_json = json.loads(response.data)
    assert response_json['message'] == 'Success'
    assert response_json['data'] == mock_request_data['payload']


def test_post_route__failure__unauthorized():
    """Test POST request failure due to missing authorization header"""
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/post/test'

    # No authorization header
    mock_request_headers = {}

    mock_request_data = {
        'request_id': '123',
        'payload': {
            'py': 'pi',
            'java': 'script'
        }
    }

    response = client.post(url, data=json.dumps(mock_request_data), headers=mock_request_headers)
    assert response.status_code == 401
    response_json = json.loads(response.data)
    assert response_json['message'] == 'Unauthorized'


def test_post_route__failure__bad_request():
    """Test POST request failure due to bad request (missing data)"""
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/post/test'

    # Valid authorization header, but bad request data
    mock_request_headers = {
        'authorization-sha256': '123'
    }

    mock_request_data = {}

    response = client.post(url, data=json.dumps(mock_request_data), headers=mock_request_headers)
    assert response.status_code == 400
    response_json = json.loads(response.data)
    assert response_json['message'] == 'Bad Request'
