import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from faker import Faker
from database.db import session
from database.models import Teacher
from decorators import decorator_seed

fake = Faker("en_US")


@decorator_seed
def seed_teachers(count: int):
    for _ in range(count):
        teacher = Teacher(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=fake.ascii_free_email(),
            address=fake.address(),
            start_work=fake.date_between(start_date="-1y", end_date="today"),
        )
        session.add(teacher)
    session.commit()


if __name__ == "__main__":
    seed_teachers()
