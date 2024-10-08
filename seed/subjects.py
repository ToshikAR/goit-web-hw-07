import sys
import os
import random

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))


from database.db import session
from sqlalchemy import select
from database.models import Subject, Teacher
from decorators import decorator_seed

SUBJECTE = [
    "Mathematics",
    "Physics",
    "Geometry",
    "Programming",
    "Chemistry",
    "Biology",
    "History",
    "Biology",
]


@decorator_seed
def seed_subjects():
    teachers_id = session.scalars(select(Teacher.id)).all()
    for sub in SUBJECTE:
        subject = Subject(
            name=sub,
            teacher_id=random.choice(teachers_id),
        )
        session.add(subject)
    session.commit()


if __name__ == "__main__":
    seed_subjects()
