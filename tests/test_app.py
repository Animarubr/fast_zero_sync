from http import HTTPStatus

from fast_zero.schemas import UserPublic


def test_read_root_deve_retornar_ok_e_ola_mundo(client):
    response = client.get('/')  # Act (Ação)
    assert response.status_code == HTTPStatus.OK  # Assert
    assert response.json() == {'message': 'Olá Mundo!'}  # Assert


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'test',
            'password': '1236',
            'email': 'test@test.com',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'username': 'test',
        'email': 'test@test.com',
    }


def test_create_user_fail_username(client, user):
    response = client.post(
        '/users/',
        json={
            'username': 'test',
            'password': '1236',
            'email': 'test@test.com',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Username already exists.'}


def test_create_user_fail_email(client, user):
    response = client.post(
        '/users/',
        json={
            'username': 'teste',
            'password': '1236',
            'email': 'test@test.com',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Email already exists.'}


def test_read_users(client):
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_read_users_with_user(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_read_user_by_id(client, user):
    response = client.get('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'username': 'test',
        'email': 'test@test.com',
    }


def test_read_user_by_id_fail(client, user):
    response = client.get('/users/10')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not foud!'}


def test_update_user(client, user):
    response = client.put(
        '/users/1',
        json={
            'password': '1236',
            'username': 'amimmeusxman',
            'email': 'papagaiada@mail.com',
            'id': 1,
        },
    )
    assert response.json() == {
        'username': 'amimmeusxman',
        'email': 'papagaiada@mail.com',
        'id': 1,
    }


def test_update_user_fail(client, user):
    response = client.put(
        '/users/2',
        json={
            'password': '1236',
            'username': 'amimmeusxman',
            'email': 'papagaiada@mail.com',
            'id': 2,
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not foud!'}


def test_delete_user(client, user):
    response = client.delete('/users/1')

    assert response.json() == {'message': 'User deleted!'}


def test_delete_user_fail(client, user):
    response = client.delete('/users/2')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not foud!'}
