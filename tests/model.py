
from sqlalchemy import Column, Integer, String, Table, ForeignKey
from tests.conftest import Base, engine
from sqlalchemy import MetaData


class TestUser(Base):
    # call fisrt then create_all
    # __table_args__ = {'schema': schema}
    __tablename__ = "test_users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    nickname = Column(String)

    def __repr__(self):
        return "<User(name='%s', fullname='%s', nickname='%s')>" % (
            self.name,
            self.fullname,
            self.nickname,
        )


metadata_obj = MetaData()

User = Table(
    "user",
    metadata_obj,
    Column("user_id", Integer, primary_key=True),
    Column("user_name", String(16), nullable=False),
    Column("email_address", String(60)),
    Column("nickname", String(50), nullable=False),
)


Address = Table(
    "engine_email_addresses",
    metadata_obj,
    Column("address_id", Integer, primary_key=True),
    Column("remote_user_id", Integer, ForeignKey(User.c.user_id)),
    Column("email_address", String(20)),
    mysql_engine="InnoDB",
)

Base.metadata.create_all(engine)
