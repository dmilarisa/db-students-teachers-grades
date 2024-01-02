import random

from faker import Faker
from sqlalchemy.exc import SQLAlchemyError

from conf.db import session
from conf.models import Student, Teacher, Subject, Grade, Group


fake = Faker("uk-UA")


def insert_teachers():
    for _ in range(5):
        teacher = Teacher(fullname=fake.name())
        session.add(teacher)


def insert_groups():
    groups = ['A01', 'B01', 'C01']
    for g in groups:
        group = Group(name=g)
        session.add(group)


def insert_students():
    groups = session.query(Group).all()
    for _ in range(40):
        student = Student(
            fullname=fake.name(),
            group_id=random.choice(groups).id
        )
        session.add(student)


def insert_subjects():
    teachers = session.query(Teacher).all()
    subjects = ['Math', 'Economics', 'Probability Theory', 'Literature', 'Physical Ed.']
    for subject in subjects:
        subject = Subject(
            name=subject,
            teacher_id=random.choice(teachers).id
        )
        session.add(subject)


def insert_grades():
    students = session.query(Student).all()
    subjects = session.query(Subject).all()
    for st in students:
        for subj in subjects:
            for _ in range(21):
                grade = Grade(
                    grade=random.randint(0,100),
                    grade_date=fake.date_between(start_date='-1y'),
                    student_id=st.id,
                    subject_id=subj.id
                )
                session.add(grade)


if __name__ == '__main__':
    try:
        insert_teachers()
        insert_groups()
        session.commit()
        insert_students()
        insert_subjects()
        session.commit()
        insert_grades()
        session.commit()
    except SQLAlchemyError as e:
        print(e)
        session.rollback()
    finally:
        session.close()

