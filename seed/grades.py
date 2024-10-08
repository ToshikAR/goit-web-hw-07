import sys
import os
import random

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from faker import Faker
from database.db import session
from sqlalchemy import select
from database.models import Grade, Student, Subject
from decorators import decorator_seed

fake = Faker("en_US")


@decorator_seed
def seed_grades():
    students_id = session.scalars(select(Student.id)).all()
    subjects_id = session.scalars(select(Subject.id)).all()
    for st_id in students_id:
        # Генеруємо випадкову кількість оцінок від 5 до 20
        num_grades = random.randint(5, 20)
        for _ in range(num_grades):
            grade = Grade(
                grade=random.randint(1, 12),
                date_of=fake.date_between(start_date="-1y", end_date="today"),
                student_id=st_id,
                subject_id=random.choice(subjects_id),
            )
            session.add(grade)
    session.commit()


if __name__ == "__main__":
    seed_grades()
