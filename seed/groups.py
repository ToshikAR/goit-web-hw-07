import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from faker import Faker
from database.db import session
from database.models import Group
from decorators import decorator_seed

fake = Faker("en_US")
GROUPS = ["GroupA", "GroupB", "GroupC", "GroupD", "GroupE"]


@decorator_seed
def seed_groups():
    for gr in GROUPS:
        group = Group(
            name=gr,
        )
        session.add(group)
    session.commit()


if __name__ == "__main__":
    seed_groups()
