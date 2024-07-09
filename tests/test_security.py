from http import HTTPStatus

from jwt import decode

from fast_zero.security import create_access_token, settings


def test_jwt():
    data = {'sub': 'test@test.com'}
    token = create_access_token(data)

    result = decode(
        token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
    )
    assert result['sub'] == data['sub']
    assert result['exp']


def test_jwt_invalid_token(client):
    response = client.delete(
        '/users/2', headers={'Authorization': 'Bearer token-invalido'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validade credentials'}
    assert response.headers['WWW-Authenticate']
    assert response.headers['WWW-Authenticate'] == 'Bearer'


# TODO: fazer o teste para caso o user não esteja registrado
# def test_jwt_token_if_correct_token_and_user_not_exists(client, user, token):
#     response = client.put(
#         '/users/2',
#         headers={'Authorization': f'Bearer {token}'},
#         json={
#             'password': '1236',
#             'username': 'amimmeusxman',
#             'email': 'papagaiada@mail.com',
#             'id': 2,
#         },
#     )

#     assert response.status_code == HTTPStatus.UNAUTHORIZED
#     assert response.json() == {'detail': 'Could not validade credentials'}
