"""
https://climbtheladder.com/10-sqlalchemy-best-practices/

pip install sqlalchemy

"""
from tests.model import TestUser, User, Address
from sqlalchemy import select
from sqlalchemy.orm import aliased


def test_user(db_session):
    our_user = TestUser(name="ed", fullname="Ed Jones", nickname="kname")

    db_session.add(our_user)
    db_session.commit()

    user_1 = (
        db_session.query(TestUser).filter_by(name="ed").first()
    )

    select_q = select(TestUser).where(TestUser.name == 'ed')
    user_2 = db_session.scalar(select_q)

    assert user_1 == user_2
    # Base.metadata.drop_all(engine) # FIXME not working?


def test_user_1(db_session):
    # FIXME
    subq = select(User, Address.email_address).join(User.addresses).subquery()
    ua = aliased(User, subq)
    aa = aliased(Address, subq)
    stmt = select(ua, aa).order_by(aa.email_address)
    result = db_session.execute(stmt)
    result
