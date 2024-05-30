import os

import factory
from factory import LazyAttribute, Faker
from PIL import Image

from src.config import settings
from src.database import SessionLocal
from src.tdd.models import Member


class MemberFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Member
        sqlalchemy_session = SessionLocal()
        sqlalchemy_get_or_create = ("username",)
        sqlalchemy_session_persistence = "commit"

    username = Faker("user_name")
    email = LazyAttribute(lambda o: "%s@example.com" % o.username)

    @factory.lazy_attribute
    def avatar(self):

        width = 300
        height = 300
        color = "blue"
        image_format = "JPEG"
        image_palette = "RGB"

        with Image.new(image_palette, (width, height), color) as thumb:
            filename = f"{self.username}.jpg"
            full_path = os.path.join(
                settings.UPLOADS_DEFAULT_DEST,
                filename
            )
            thumb.save(full_path, format=image_format)

        return filename
