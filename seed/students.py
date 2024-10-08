import sys
import os
import random

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from faker import Faker
from sqlalchemy import select
from database.db import session
from database.models import Student, Group
from decorators import decorator_seed

fake = Faker("en_US")


@decorator_seed
def seed_students(count: int):
    group_id = session.scalars(select(Group.id)).all()
    for _ in range(count):
        student = Student(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=fake.ascii_free_email(),
            address=fake.address(),
            group_id=random.choice(group_id),
        )
        session.add(student)
    session.commit()


if __name__ == "__main__":
    seed_students(1)
