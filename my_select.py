from sqlalchemy import and_, func, desc

from database.db import session
from database.models import Group, Student, Teacher, Subject, Grade
from seed.decorators import error_select


@error_select
def select_1():
    """
    Знайти 5 студентів із найбільшим середнім балом з усіх предметів.
    """
    result = (
        session.query(
            Student.fullname,
            func.round(func.avg(Grade.grade), 2).label("avg_grade"),
        )
        .select_from(Grade)
        .join(Student)
        .group_by(Student.id)
        .order_by(desc("avg_grade"))
        .limit(5)
        .all()
    )
    return result


@error_select
def select_2(subject_id=1):
    """
    Знайти студента із найвищим середнім балом з певного предмета.
    """
    result = (
        session.query(
            Student.fullname,
            func.round(func.avg(Grade.grade), 2).label("avg_grade"),
        )
        .join(Grade)
        .filter(Grade.subject_id == subject_id)
        .group_by(Student.id)
        .order_by(func.avg(Grade.grade).desc())
        .first()
    )
    return result


@error_select
def select_3(subject_id=1):
    """
    Знайти середній бал у групах з певного предмета.
    """
    result = (
        session.query(
            Group.name.label("group_name"),
            Subject.name.label("subject_name"),
            func.round(func.avg(Grade.grade), 2).label("avg_grade"),
        )
        .select_from(Group)
        .join(Student, Student.group_id == Group.id)
        .join(Grade, Grade.student_id == Student.id)
        .join(Subject, Grade.subject_id == Subject.id)
        .filter(Grade.subject_id == subject_id)
        .group_by(Group.id, Subject.name)
        .order_by(func.avg(Grade.grade).desc())
        .all()
    )
    return result


@error_select
def select_4():
    """
    Знайти середній бал на потоці (по всій таблиці оцінок).
    """
    result = session.query(
        func.round(func.avg(Grade.grade), 2).label("avg_grade"),
    ).first()
    return result


@error_select
def select_5(teacher_id=1):
    """
    Знайти які курси читає певний викладач.
    """
    result = (
        session.query(
            Teacher.fullname,
            Subject.name.label("subject_name"),
        )
        .join(Teacher, Teacher.id == Subject.teacher_id)
        .filter(Teacher.id == teacher_id)
        .all()
    )
    return result


@error_select
def select_6(student_id=1):
    """
    Знайти список студентів у певній групі.
    """
    result = (
        session.query(
            Student.fullname,
            Group.name.label("group_name"),
        )
        .join(Group, Group.id == Student.group_id)
        .filter(Student.id == student_id)
        .all()
    )
    return result


@error_select
def select_7(group_id=1, subject_id=1):
    """
    Знайти оцінки студентів у окремій групі з певного предмета.
    """
    result = (
        session.query(
            Student.fullname,
            Grade.grade.label("grade"),
            Group.name.label("group_name"),
            Subject.name.label("subject_insme"),
        )
        .join(Group, Group.id == Student.group_id)
        .join(Grade, Student.id == Grade.student_id)
        .filter(Group.id == group_id)
        .filter(Subject.id == subject_id)
        .all()
    )
    return result


@error_select
def select_8(teacher_id=1):
    """
    Знайти середній бал, який ставить певний викладач зі своїх предметів.
    """
    result = (
        session.query(
            Teacher.fullname,
            Subject.name.label("subject_name"),
            func.round(func.avg(Grade.grade), 2).label("avg_grade"),
        )
        .join(Subject, Subject.teacher_id == Teacher.id)
        .join(Grade, Grade.subject_id == Subject.id)
        .filter(Teacher.id == teacher_id)
        .group_by(Teacher.id, Teacher.fullname, Subject.name)
        .first()
    )
    return result


@error_select
def select_9(student_id=1):
    """
    Знайти список курсів, які відвідує певний студент.
    """
    result = (
        session.query(
            Student.fullname,
            Subject.name.label("subject_name"),
        )
        .join(Grade, Grade.subject_id == Subject.id)
        .join(Student, Student.id == Grade.student_id)
        .filter(Student.id == student_id)
        .distinct()
        .all()
    )
    return result


@error_select
def select_9(student_id=1):
    """
    Знайти список курсів, які відвідує певний студент.
    """
    result = (
        session.query(
            Student.fullname,
            Subject.name.label("subject_name"),
        )
        .join(Grade, Grade.subject_id == Subject.id)
        .join(Student, Student.id == Grade.student_id)
        .filter(Student.id == student_id)
        .distinct()
        .all()
    )
    return result


@error_select
def select_10(student_id=1, teacher_id=1):
    """
    Список курсів, які певному студенту читає певний викладач.
    """
    result = (
        session.query(
            Student.fullname,
            Teacher.fullname,
            Subject.name.label("subject_name"),
        )
        .join(Grade, Grade.subject_id == Subject.id)
        .join(Student, Student.id == Grade.student_id)
        .filter(Student.id == student_id)
        .filter(Teacher.id == teacher_id)
        .group_by(Student.id, Teacher.id, Subject.name)
        .distinct()
        .all()
    )
    return result


@error_select
def select_11(teacher_id=1, student_id=1):
    """
    Додаткове завдання
    Середній бал, який певний викладач ставить певному студентові.
    """
    result = (
        session.query(
            Teacher.fullname,
            Student.fullname,
            func.round(func.avg(Grade.grade), 2).label("avg_grade"),
        )
        .join(Subject, Subject.teacher_id == Grade.subject_id)
        .join(Teacher, Teacher.id == Subject.teacher_id)
        .join(Student, Student.id == Grade.student_id)
        .filter(Teacher.id == teacher_id)
        .filter(Student.id == student_id)
        .group_by(Teacher.id, Student.id)
        .all()
    )
    return result


@error_select
def select_12(group_id=1, subject_id=1):
    """
    Додаткове завдання
    Оцінки студентів у певній групі з певного предмета на останньому занятті.
    """
    lastGradeDate = (
        session.query(
            func.max(Grade.date_of).label("max_date"),
        )
        .select_from(Grade)
        .join(Subject, Subject.id == Grade.subject_id)
        .join(Student, Student.id == Grade.student_id)
        .join(Group, Group.id == Student.group_id)
        .filter(Grade.subject_id == subject_id)
        .filter(Group.id == group_id)
        .scalar()
    )
    if not lastGradeDate:
        return None

    result = (
        session.query(
            Student.fullname,
            Subject.name.label("subject_name"),
            Grade.grade,
            Grade.date_of,
        )
        .select_from(Grade)
        .join(Student, Student.id == Grade.student_id)
        .join(Group, Group.id == Student.group_id)
        .join(Subject, Subject.id == Grade.subject_id)
        .filter(Grade.date_of == lastGradeDate)
        .filter(Group.id == group_id)
        .filter(Grade.subject_id == subject_id)
        .all()
    )
    return result


if __name__ == "__main__":
    select_list = [
        select_1(),
        select_2(),
        select_3(),
        select_4(),
        select_5(),
        select_6(20),
        select_7(2, 4),
        select_8(2),
        select_9(30),
        select_10(35, 2),
        select_11(2, 1),
        select_12(1, 5),
    ]

    print(select_list[11])
