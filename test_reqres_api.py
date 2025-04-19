from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import requests
import uuid
import pytest

ENDPOINT = "https://reqres.in/"

def test_call_endpoint():
    response = requests.get(ENDPOINT)
    assert response.status_code == 200
    print (response)

    # data = response.json()
    # print(data)

    status_code = response.status_code
    print(status_code)

    get_users_response = get_users(2)
    assert get_users_response.status_code == 200

    data = get_users_response.json()
    print(data)

def test_get_user():
    get_user_response = get_users(2)
    assert get_user_response.status_code == 200
    data = get_user_response.json()
    print(data)
    assert data['data']['id'] == 2
    assert data['data']['email'] == "janet.weaver@reqres.in"
    user_data = get_user_response.json().get('data')
    print(user_data)
    expected_keys = ['id', 'email', 'first_name', 'last_name', 'avatar']
    for key in expected_keys:
        assert key in user_data, f"Key '{key}' not found in user data"
    assert set(user_data.keys()) == set(expected_keys), "User data keys do not match expected keys"

def test_get_non_existent_user():
    get_user_response = get_users(123)
    assert get_user_response.status_code == 404
    data = get_user_response.json()
    print(data)

def test_get_all_users():
    get_users_response = get_all_users(1)
    assert get_users_response.status_code == 200
    data = get_users_response.json()
    # print(data)
    assert data['data'][3]['email'] == "eve.holt@reqres.in"

    for users in data['data']:
        #print (users)
        #print (users.get('email'))
        emails = users.get('email')
        assert "eve.holt@reqres.in"
        print(emails)
    

def test_create_task():
    payload = {
        "name" : "robert",
        "job" : "qa tester"
    }
    create_user_response = create_user(payload)
    print(create_user_response)
    assert create_user_response.status_code == 201
    create_user_data = create_user_response.json()
    print(create_user_data)
    assert create_user_data['name'] == payload['name']
    assert create_user_data['job'] == payload['job']
    assert 'id' in create_user_data  # ID is randomly generated
    assert 'createdAt' in create_user_data  # Also generated
    user_id = create_user_data.get('id')
    if user_id is None:
        print("User ID not found in the response.")
        return
    print(user_id)
    get_task_response = get_users(user_id)
    print(get_task_response)
    get_user_data = get_task_response.json()
    print(get_user_data)
    # assert get_task_response.status_code == 200
    get_task_data = get_task_response.json()
    # assert get_task_data['data']['id'] == data['id']
    # assert get_task_data['data']['name'] == payload['name']
    # assert get_task_data['data']['job'] == payload['job']
    print(get_task_data)

def test_create_user_with_large_payload():
    payload = {
        "name" : "robert" * 1000,
        "job" : "qa tester" * 1000
    }
    create_user_response = create_user(payload)
    print(create_user_response)
    assert create_user_response.status_code == 201
    create_user_data = create_user_response.json()
    print(create_user_data)
    assert create_user_data['name'] == payload['name']
    assert create_user_data['job'] == payload['job']
    assert 'id' in create_user_data  # ID is randomly generated
    assert 'createdAt' in create_user_data  # Also generated
    user_id = create_user_data.get('id')
    if user_id is None:
        print("User ID not found in the response.")
        return
    
def test_create_multiple_users():
    users = create_multiple_users(10)
    assert len(users) == 10
    ids = [user['id'] for user in users]
    print(f"Created user IDs: {ids}")
    assert len(set(ids)) == len(ids), "Duplicate IDs detected!"

def test_update_user():
    #create a user
    payload = new_user_payload()
    create_user_response = create_user(payload)
    assert create_user_response.status_code == 201
    user_id = create_user_response.json()
    print(user_id)

    #update the user
    new_payload = {
        "name" : payload['name'],
        "job" : "New job title"
    }

    update_user_response = update_user(new_payload)
    assert update_user_response.status_code == 200
    #print(update_user_response)
    update_user_data = update_user_response.json()
    print(update_user_data)
    assert update_user_data['name'] == new_payload['name']
    assert update_user_data['job'] == new_payload['job']
    assert 'updatedAt' in update_user_data  # Also generated
    user_id = update_user_data.get('id')

def test_patch_user():
    #create a user
    payload = new_user_payload()
    create_user_response = create_user(payload)
    assert create_user_response.status_code == 201
    user_id = create_user_response.json()
    print(user_id)

    #patch the user
    new_payload = {
        "name" : payload['name'],
        "job" : "Patched job title"
    }

    patch_user_response = patch_user(new_payload)
    assert patch_user_response.status_code == 200
    print(patch_user_response)
    patch_user_data = patch_user_response.json()
    print(patch_user_data)
    assert patch_user_data['name'] == new_payload['name']
    assert patch_user_data['job'] == new_payload['job']
    assert 'updatedAt' in patch_user_data  # Also generated
    user_id = patch_user_data.get('id')

def test_delete_user():
    #create a user
    payload = new_user_payload()
    create_user_response = create_user(payload)
    assert create_user_response.status_code == 201
    user_id = create_user_response.json()
    print(user_id)

    #delete the user
    delete_user_response = delete_user(user_id)
    assert delete_user_response.status_code == 204
    print(delete_user_response)
    #check that the user is deleted
    get_user_response = get_users(user_id)
    assert get_user_response.status_code == 404
    print(get_user_response)

def test_register_user():
    payload = {
        "email": "eve.holt@reqres.in",
        "password": "pistol"
    }

    register_user_response = register_user(payload)
    assert register_user_response.status_code == 200
    print(register_user_response)
    register_user_data = register_user_response.json()
    print(register_user_data)
    assert register_user_data['id'] == 4
    assert register_user_data['token'] == 'QpwL5tke4Pnpja7X4'

def test_register_user_without_password():
    payload = {
        "email": "sydney@fife"
    }

    register_user_response = register_user(payload)
    assert register_user_response.status_code == 400
    print(register_user_response)
    register_user_data = register_user_response.json()
    print(register_user_data)
    assert register_user_data['error'] == 'Missing password'
    assert "Missing password" in register_user_data['error']

def test_login_user_without_password():
    payload = {
        "email": "peter@klaven"
    }

    login_user_response = login_user(payload)
    assert login_user_response.status_code == 400
    print(login_user_response)
    login_user_data = login_user_response.json()
    print(login_user_data)
    assert login_user_data['error'] == 'Missing password'
    assert "Missing password" in login_user_data['error']


def test_login_user():
    payload = {
        "email": "eve.holt@reqres.in",
        "password": "cityslicka"
    }

    login_user_response = login_user(payload)
    assert login_user_response.status_code == 200
    print(login_user_response)
    login_user_data = login_user_response.json()
    print(login_user_data)
    assert login_user_data['token'] == 'QpwL5tke4Pnpja7X4'

def test_get_users_delayed():
    delay_nb = 3
    start = time.time()
    get_users_delayed_response = get_users_delayed(delay_nb)
    end = time.time()
    assert get_users_delayed_response.status_code == 200
    print(get_users_delayed_response)
    get_users_delayed_data = get_users_delayed_response.json()
    print(get_users_delayed_data)
    assert len(get_users_delayed_data['data']) == 6
    assert get_users_delayed_data['page'] == 1
    assert get_users_delayed_data['per_page'] == 6
    assert get_users_delayed_data['total'] == 12
    assert get_users_delayed_data['total_pages'] == 2
    assert get_users_delayed_data['data'][0]['id'] == 1
    assert get_users_delayed_data['data'][0]['first_name'] == 'George'
    assert get_users_delayed_data['data'][0]['last_name'] == 'Bluth'
    assert end - start >= delay_nb, f"Response time was {end - start} seconds, expected at least {delay_nb} seconds"
    

def create_user_concurrent(index):
    payload = {
        "name": f"user_{index}",
        "job": f"tester_{index}"
    }
    response = create_user(payload)
    assert response.status_code == 201
    data = response.json()
    print(f"[{index}] Created user: {data}")
    return data

def test_create_multiple_users_concurrently(count=10, max_workers=5):
    created_users = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(create_user_concurrent, i) for i in range(count)]

        for future in as_completed(futures):
            try:
                result = future.result()
                created_users.append(result)
            except Exception as e:
                print(f"Error during concurrent user creation: {e}")

    # Check if all users were created
    assert len(created_users) == count, f"Expected {count} users, got {len(created_users)}"
    print("All users created successfully!")


def create_user_concurrent_timed(index):
    payload = {
        "name": f"user_{index}",
        "job": f"tester_{index}"
    }

    start_time = time.time()
    response = create_user(payload)
    end_time = time.time()
    duration = round(end_time - start_time, 3)

    assert response.status_code == 201
    data = response.json()
    print(f"[{index}] Created user in {duration}s: {data}")

    return {
        "index": index,
        "data": data,
        "duration": duration
    }

MAX_AVG_RESPONSE_TIME = 2.0  # seconds
USER_COUNT = 10
MAX_WORKERS = 5

@pytest.mark.load
def test_create_users_concurrent_with_threshold():
    def create_user_timed(index):
        payload = {
            "name": f"user_{index}",
            "job": f"tester_{index}"
        }
        start = time.time()
        response = create_user(payload)
        duration = time.time() - start
        assert response.status_code == 201
        return duration

    durations = []

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(create_user_timed, i) for i in range(USER_COUNT)]
        for future in as_completed(futures):
            try:
                durations.append(future.result())
            except Exception as e:
                pytest.fail(f"User creation failed: {e}")

    avg_time = sum(durations) / len(durations)
    print(f"\nAverage response time: {avg_time:.2f}s")

    assert avg_time <= MAX_AVG_RESPONSE_TIME, (
        f"Average response time {avg_time:.2f}s exceeds threshold of {MAX_AVG_RESPONSE_TIME}s"
    )


def get_users(id):
    return requests.get(ENDPOINT + f"/api/users/{id}")

def get_all_users(page_nb):
    return requests.get(ENDPOINT + f"/api/users?page={page_nb}")

def create_user(payload):
    return requests.post(ENDPOINT + "/api/users", json=payload)

def update_user(user_id, payload):
    return requests.put(ENDPOINT + f"/api/users/{user_id}", json=payload)

def patch_user(user_id, payload):
    return requests.patch(ENDPOINT + f"/api/users/{user_id}", json=payload)

def delete_user(id):
    return requests.delete(ENDPOINT + f"/api/users/{id}")

def register_user(payload):
    return requests.post(ENDPOINT + "/api/register", json=payload)

def login_user(payload):
    return requests.post(ENDPOINT + "/api/login", json=payload)

def get_users_delayed(delay_nb):
    return requests.get(ENDPOINT + f"/api/users?delay={delay_nb}")

def new_user_payload():
    name = f"test_user_{uuid.uuid4()}"
    job = f"test_job_{uuid.uuid4()}"

    return {
        "name": name,
        "job": job
    }

def create_multiple_users(count=5):
    created_users = []

    for i in range(count):
        payload = {
            "name": f"user_{i}",
            "job": f"tester_{i}"
        }

        response = create_user(payload)
        print(f"Creating user {i + 1}: Status {response.status_code}")
        assert response.status_code == 201

        data = response.json()
        print(data)
        assert data['name'] == payload['name']
        assert data['job'] == payload['job']
        assert 'id' in data
        assert 'createdAt' in data

        created_users.append(data)

    return created_users
