from sqlalchemy import select

from fast_zero.models import User


def test_create_user(session):
    user = User(
        username='papiroskopio',
        email='papiroskopio@papirus.com',
        password='123**4',
    )
    session.add(user)
    session.commit()
    result = session.scalar(
        select(User).where(User.email == 'papiroskopio@papirus.com')
    )

    assert result.username == 'papiroskopio'
