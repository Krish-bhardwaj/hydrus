"""
This file (test_auth.py) contains the functional tests for the collection endpoints
with respect to authentication.
"""


import json

import pytest


def test_wrong_id_get(test_client, constants, headers_with_wrong_id, collection_names):
    """
    GIVEN a Flask application
    WHEN a collection endpoint has a GET request with wrong user id in header
    THEN check that a '401' or '400' status code is returned
    """
    API_NAME = constants["API_NAME"]
    response = test_client.get(f"/{API_NAME}")
    endpoints = json.loads(response.data.decode('utf-8'))
    for endpoint in endpoints:
        if endpoint in collection_names:
            response = test_client.get(endpoints[endpoint])
            headers_with_wrong_id['X-Authentication'] = response.headers['X-Authentication']
            response_get = test_client.get(
                endpoints[endpoint], headers=headers_with_wrong_id)
            assert response_get.status_code == 401 or response_get.status_code == 400


def test_wrong_id_post(test_client, constants, collection_names, headers_with_wrong_id):
    """
    GIVEN a Flask application
    WHEN a collection endpoint has a POST request with wrong user id in header
    THEN check that a '401' or '400' status code is returned
    """
    API_NAME = constants["API_NAME"]
    response = test_client.get(f"/{API_NAME}")
    endpoints = json.loads(response.data.decode('utf-8'))
    for endpoint in endpoints:
        if endpoint in collection_names:
            response = test_client.get(endpoints[endpoint])
            headers_with_wrong_id['X-Authentication'] = response.headers['X-Authentication']
            response_post = test_client.post(endpoints[endpoint],
                                             headers=headers_with_wrong_id,
                                             data=json.dumps(dict(foo="bar")))
            assert response_post.status_code == 401 or response_post.status_code == 400


def test_wrong_pass_get(test_client, constants, collection_names, headers_with_wrong_pass):
    """
    GIVEN a Flask application
    WHEN a collection endpoint has a GET request with wrong user passphrase in header
    THEN check that a '401' status code is returned
    """
    API_NAME = constants["API_NAME"]
    response = test_client.get(f"/{API_NAME}")
    endpoints = json.loads(response.data.decode('utf-8'))
    for endpoint in endpoints:
        if endpoint in collection_names:
            response = test_client.get(endpoints[endpoint])
            headers_with_wrong_pass['X-Authentication'] = response.headers['X-Authentication']
            response_get = test_client.get(
                endpoints[endpoint], headers=headers_with_wrong_pass)
            assert response_get.status_code == 401


def test_wrong_pass_post(test_client, constants, collection_names, headers_with_wrong_pass):
    """
    GIVEN a Flask application
    WHEN a collection endpoint has a POST request with wrong user passphrase in header
    THEN check that a '401' status code is returned
    """
    API_NAME = constants["API_NAME"]
    response = test_client.get(f"/{API_NAME}")
    endpoints = json.loads(response.data.decode('utf-8'))
    for endpoint in endpoints:
        if endpoint in collection_names:
            response = test_client.get(endpoints[endpoint])
            headers_with_wrong_pass['X-Authentication'] = response.headers['X-Authentication']
            response_post = test_client.post(endpoints[endpoint],
                                             headers=headers_with_wrong_pass,
                                             data=json.dumps(dict(foo="bar")))
            assert response_post.status_code == 401


def test_wrong_nonce_get(test_client, constants, collection_names,
                         headers_with_correct_pass_and_id):
    """
    GIVEN a Flask application
    WHEN a collection endpoint has a GET request with wrong nonce in header
    THEN check that a '401' status code is returned
    """
    API_NAME = constants["API_NAME"]
    response = test_client.get(f"/{API_NAME}")
    endpoints = json.loads(response.data.decode('utf-8'))
    for endpoint in endpoints:
        if endpoint in collection_names:
            headers_with_correct_pass_and_id['X-authentication'] = "random-string"
            response_get = test_client.get(
                endpoints[endpoint], headers=headers_with_correct_pass_and_id)
            assert response_get.status_code == 401


def test_wrong_nonce_post(test_client, constants, collection_names,
                          headers_with_correct_pass_and_id):
    """
    GIVEN a Flask application
    WHEN a collection endpoint has a POST request with wrong nonce in header
    THEN check that a '401' status code is returned
    """
    API_NAME = constants["API_NAME"]
    response = test_client.get(f"/{API_NAME}")
    endpoints = json.loads(response.data.decode('utf-8'))
    for endpoint in endpoints:
        if endpoint in collection_names:
            headers_with_correct_pass_and_id['X-authentication'] = "random-string"
            response_post = test_client.post(endpoints[endpoint],
                                             headers=headers_with_correct_pass_and_id,
                                             data=json.dumps(dict(foo="bar")))
            assert response_post.status_code == 401


# get and delete can be parametrize together as for both of them no data object in request
@pytest.mark.parametrize("operation", [
    ("get"),
    ("delete"),
])
def test_correct_auth_get(operation, test_client, constants, collection_names,
                          headers_with_correct_pass_and_id):
    """
    GIVEN a Flask application
    WHEN a collection endpoint has a GET or a DELETE request with correct user credentials
    THEN check that a '401' status code is not returned
    """
    API_NAME = constants["API_NAME"]
    response = test_client.get(f"/{API_NAME}")
    endpoints = json.loads(response.data.decode('utf-8'))
    for endpoint in endpoints:
        if endpoint in collection_names:
            response = test_client.get(endpoints[endpoint])
            x_auth = 'X-Authentication'
            headers_with_correct_pass_and_id[x_auth] = response.headers[x_auth]
            # get the response for the required operation
            response_op = getattr(test_client, operation)(endpoints[endpoint],
                                                          headers=headers_with_correct_pass_and_id)
            assert response_op.status_code != 401


# post and put can be parametrized together as for them data object in request can be same
@pytest.mark.parametrize("operation", [
    ("post"),
    ("put"),
])
def test_correct_auth_post(operation, test_client, constants, collection_names,
                           headers_with_correct_pass_and_id):
    """
    GIVEN a Flask application
    WHEN a collection endpoint has a POST or a PUT request with correct user credentials
    THEN check that a '401' status code is not returned
    """
    API_NAME = constants["API_NAME"]
    response = test_client.get(f"/{API_NAME}")
    endpoints = json.loads(response.data.decode('utf-8'))
    for endpoint in endpoints:
        if endpoint in collection_names:
            response = test_client.get(endpoints[endpoint])
            x_auth = 'X-Authentication'
            headers_with_correct_pass_and_id[x_auth] = response.headers[x_auth]
            response_op = getattr(test_client, operation)(endpoints[endpoint],
                                                          headers=headers_with_correct_pass_and_id,
                                                          data=json.dumps(dict(foo="bar")))
            assert response_op.status_code != 401
