import time
import requests as rq

# change the host:port value for the server you are testing accordingly
host_port = 'http://192.168.1.100:8444'

asteroid_id = list()


def test_create_asteroid_and_send_alert():
    """
    Tests the Creation of Asteroid with alert: /asteroid/create
    """
    body = {
            "type": "M",
            "sizeMeters": 1000,     # will send a notification alert
            "distanceFromEarthAU": 124000001,
            "location": "35x35x35",
            "probabilityOfCollisionWithEarth": 0.9,
            "timeOfObservation": time.time()
    }
    resp = rq.post(
        url=f"{host_port}/asteroid/create", headers={'content-type': 'application/json'}, json=body, timeout=12
    )
    global asteroid_id
    asteroid_id.append(resp.json().get('asteroidId'))
    print(test_create_asteroid_and_send_alert.__name__, f'response: {resp.json()}')
    assert resp.json()


def test_update_asteroid_and_send_alert():
    """
    Tests the Update of Asteroid: /asteroid/update/<asteroidId>
    """
    body = {
            "type": "M",
            "sizeMeters": 90,
            "distanceFromEarthAU": 124000001,
            "location": "35x35x35",
            "probabilityOfCollisionWithEarth": 0.9,     # will send a notification alert
            "timeOfObservation": time.time()
    }
    resp = rq.put(
        url=f"{host_port}/asteroid/update/{asteroid_id[0]}", headers={'content-type': 'application/json'}, json=body,
        timeout=12
    )
    print(test_update_asteroid_and_send_alert.__name__, f'response: {resp.json()}', sep='=>')
    assert resp.json()


def test_create_asteroid_without_sending_alert():
    """
    Tests the Creation of Asteroid without alert: /asteroid/create
    """
    body = {
            "name": "small_asteroid_001",
            "type": "M",
            "sizeMeters": 100,
            "distanceFromEarthAU": 124000001,
            "location": "35x35x35",
            "probabilityOfCollisionWithEarth": 0.4,
            "timeOfObservation": time.time()
    }
    resp = rq.post(
        url=f"{host_port}/asteroid/create", headers={'content-type': 'application/json'}, json=body, timeout=12
    )
    global asteroid_id
    asteroid_id.append(resp.json().get('asteroidId'))
    print(test_create_asteroid_without_sending_alert.__name__, f'response: {resp.json()}', sep='=>')
    assert resp.json()


def test_update_asteroid_without_sending_alert():
    """
    Tests the Update of Asteroid without sending any alerts: /asteroid/update/<asteroidId>
    """
    body = {
            "type": "M",
            "sizeMeters": 90,
            "distanceFromEarthAU": 124000001,
            "location": "35x35x35",
            "probabilityOfCollisionWithEarth": 0.6,
            "timeOfObservation": time.time()
    }
    resp = rq.put(
        url=f"{host_port}/asteroid/update/{asteroid_id[1]}", headers={'content-type': 'application/json'}, json=body,
        timeout=12
    )
    print(test_update_asteroid_without_sending_alert.__name__, f'response: {resp.json()}', sep='=>')
    assert resp.json()


def test_update_asteroid_which_is_not_present():
    """
    Tests the Update of Asteroid which is not present in the system: /asteroid/update/<asteroidId>
    """
    body = {
            "type": "M",
            "sizeMeters": 90,
            "distanceFromEarthAU": 124000001,
            "location": "35x35x35",
            "probabilityOfCollisionWithEarth": 0.6,
            "timeOfObservation": time.time()
    }
    random_id = '1234567890987432'
    resp = rq.put(
        url=f"{host_port}/asteroid/update/{random_id}", headers={'content-type': 'application/json'}, json=body,
        timeout=12
    )
    print(test_update_asteroid_which_is_not_present.__name__, f'response: {resp.json()}', sep='=>')
    assert resp.json()


def test_get_asteroid():
    """
    Tests the Fetching of Asteroid-Info: /asteroid/fetch/<asteroidId>
    """
    for every_id in asteroid_id:
        resp = rq.get(
            url=f"{host_port}/asteroid/fetch/{every_id}", headers={'content-type': 'application/json'}, timeout=12
        )
        print(test_get_asteroid.__name__, f'response: {resp.json()}', sep='=>')
        assert resp.json()


def test_delete_asteroid():
    """
    Tests the removal of Asteroid-Info: /asteroid/delete/<asteroidId>
    """
    global asteroid_id
    for every_id in asteroid_id:
        resp = rq.delete(
            url=f"{host_port}/asteroid/delete/{every_id}", headers={'content-type': 'application/json'}, timeout=12
        )
        print(test_delete_asteroid.__name__, f'response: {resp.json()}', sep='=>')
        assert resp.json()


def test_delete_asteroid_which_is_not_present():
    """
    Tests the Delete of Asteroid which is not present in the system: /asteroid/delete/<asteroidId>
    """
    random_id = '0876543456789876543'
    resp = rq.delete(
        url=f"{host_port}/asteroid/delete/{random_id}", headers={'content-type': 'application/json'}, timeout=12
    )
    print(test_delete_asteroid_which_is_not_present.__name__, f'response: {resp.json()}', sep='=>')
    assert resp.json()


def test_create_asteroid_with_invalid_fields():
    """
    Tests the Creation of Asteroid with invalid fields: /asteroid/create
    """
    body = {
            "type-1": "M",
            "sizeMeters-2": 90,
            "distanceFromEarthAU": 124000001,
            "location": "35x35x35",
            "probabilityOfCollisionWithEarth": 0.6,
            "timeOfObservation-2": time.time()
    }

    resp = rq.post(
        url=f"{host_port}/asteroid/create", headers={'content-type': 'application/json'}, json=body,
        timeout=12
    )
    print(test_create_asteroid_with_invalid_fields.__name__, f'response: {resp.json()}', sep='=>')
    assert resp.json()


if __name__ == '__main__':
    test_create_asteroid_and_send_alert()
    test_update_asteroid_and_send_alert()
    test_create_asteroid_without_sending_alert()
    test_update_asteroid_without_sending_alert()
    test_update_asteroid_which_is_not_present()
    test_get_asteroid()
    test_delete_asteroid()
    test_delete_asteroid_which_is_not_present()
    test_create_asteroid_with_invalid_fields()
