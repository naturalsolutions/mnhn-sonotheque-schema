import factory
from factory import LazyAttribute, Faker

from src.database import SessionLocal
from src.users.models import User


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = SessionLocal()
        sqlalchemy_get_or_create = ("username",)
        sqlalchemy_session_persistence = "commit"

    username = Faker("user_name")
    email = LazyAttribute(lambda o: "%s@example.com" % o.username)
