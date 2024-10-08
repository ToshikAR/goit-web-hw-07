import argparse
import random
from faker import Faker
from sqlalchemy import select

from database.db import session
from database.models import Group, Student, Teacher, Subject, Grade
from seed.decorators import error_select

fake = Faker("en_US")


@error_select
def createStudent(args):
    first_name, last_name = args.name.split(" ")
    group_id = session.scalars(select(Group.id)).all()

    new_student = Student(
        first_name=first_name,
        last_name=last_name,
        email=fake.ascii_free_email(),
        address=fake.address(),
        group_id=random.choice(group_id),
    )
    session.add(new_student)
    session.commit()
    return f"id: {new_student.id} FullName: {new_student.fullname}"


@error_select
def createTeacher(args):
    first_name, last_name = args.name.split(" ")
    new_teacher = Teacher(
        first_name=first_name,
        last_name=last_name,
        email=fake.ascii_free_email(),
        address=fake.address(),
        start_work=fake.date_between(start_date="-1y", end_date="today"),
    )
    session.add(new_teacher)
    session.commit()
    return f"id: {new_teacher.id} FullName: {new_teacher.fullname}"


@error_select
def createGroups(args):
    group_name = args.name
    new_group = Group(
        name=group_name,
    )
    session.add(new_group)
    session.commit()
    return f"id: {new_group.id} name: {new_group.name}"


@error_select
def actionList(args):
    if args.model == "Teacher":
        result = session.query(Teacher).all()
        return [
            f"ID: {s.id}, FullName: {s.fullname}, Emaul: {s.email}, Addres: {s.address} "
            for s in result
        ]
    elif args.model == "Student":
        result = session.query(Student).all()
        return [
            f"ID: {s.id}, FullName: {s.fullname}, Emaul: {s.email}, Addres: {s.address} "
            for s in result
        ]
    elif args.model == "Group":
        result = session.query(Group).all()
        return [f"ID: {s.id}, GroupName: {s.name} " for s in result]
    elif args.model == "Subject":
        result = session.query(Subject).all()
        return [f"ID: {s.id}, SubjectName: {s.name} " for s in result]
    else:
        return None


@error_select
def update_by_id(args):
    if args.id != None and args.name != None and args.model in ["Student", "Teacher"]:
        model = globals()[args.model]
        first_name, last_name = args.name.split(" ")
        obj = session.query(model).filter(model.id == args.id).first()
        if obj:
            obj.first_name = first_name
            obj.last_name = last_name
            session.commit()
        return f"{args.model} => id:{obj.id} update name {obj.first_name} {obj.last_name}"


@error_select
def remove_by_id(args):
    if args.id != None and args.model in ["Student", "Teacher", "Group", "Subject"]:
        model = globals()[args.model]
        obj = session.query(model).filter_by(id=args.id).first()
        session.delete(obj)
        session.commit()
        return f"model: {args.model}, id: {args.id} DELETE!"
    return "None"


# =====================================================================================
def config_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-a",
        "--action",
        type=str,
        help="CRUD operations create|update|list|remove",
    )

    parser.add_argument(
        "-n",
        "--name",
        type=str,
        help="Full name",
    )

    parser.add_argument(
        "-m",
        "--model",
        type=str,
        help="Select model type sqlalchemy Student|Teacher|Subject|Group)",
    )

    parser.add_argument(
        "-i",
        "--id",
        type=int,
        help="Assign id",
    )

    return parser.parse_args()


# =====================================================================================


def main():
    args = config_args()
    if args.action == "create" and args.model in ["Student"]:
        print(createStudent(args))
    elif args.action == "create" and args.model in ["Teacher"]:
        print(createTeacher(args))
    elif args.action == "create" and args.model in ["Group"]:
        print(createGroups(args))
    elif args.action == "list":
        print(actionList(args))
    elif args.action == "update":
        print(update_by_id(args))
    elif args.action == "remove":
        print(remove_by_id(args))
    else:
        print("There is no such action")


if __name__ == "__main__":
    main()
