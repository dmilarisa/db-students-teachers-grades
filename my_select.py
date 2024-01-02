from sqlalchemy import func, desc, select, and_

from conf.models import Grade, Teacher, Student, Subject, Group
from conf.db import session


def select_01():
    """
    SELECT s.name, s.id, AVG(g.grade) AS avg_grade
    FROM students s
    LEFT JOIN grades as g ON s.id = g.student_id
    GROUP BY s.id
    ORDER BY avg_grade DESC
    LIMIT 5
    """
    result = session.query(Student.id, Student.fullname, func.round(func.avg(Grade.grade), 2).label('average_grade')) \
        .select_from(Student).join(Grade).group_by(Student.id).order_by(desc('average_grade')).limit(5).all()
    return result


def select_02():
    """
    SELECT
        s.id,
        s.fullname,
        ROUND(AVG(g.grade), 2) AS avg_grade
    FROM grades g
    JOIN students s ON s.id = g.student_id
    WHERE g.subject_id = 1
    GROUP BY s.id
    ORDER BY avg_grade DESC
    LIMIT 1;
    """
    result = session.query(Student.id, Student.fullname, func.round(func.avg(Grade.grade), 2).label('average_grade')) \
        .select_from(Grade).join(Student).filter(Grade.subject_id == 1).group_by(Student.id)\
        .order_by(desc('average_grade')).limit(1).all()
    return result


def select_03():
    """
    SELECT groups.id, groups.name, AVG(g.grade)
    FROM groups
    JOIN students s ON s.group_id = groups.id
    JOIN grades g on g.student_id = s.id
    WHERE g.subject_id = 3
    GROUP BY groups.id
    """
    result = session.query(Group.id, Group.name, func.round(func.avg(Grade.grade), 2).label('average_grade')) \
        .select_from(Group).join(Student).join(Grade).filter(Grade.subject_id == 3).group_by(Group.id).all()
    return result


def select_04():
    """
    SELECT ROUND(AVG(grade), 0)
    FROM grades g;
    """
    result = session.query(func.round(func.avg(Grade.grade), 0).label('average_grade')).select_from(Grade).all()
    return result


def select_05():
    """
    SELECT s.id, s.name
    FROM subjects s
    JOIN teachers t ON s.teacher_id = t.id
    WHERE t.id = 1;
    """
    result = session.query(Subject.id, Subject.name)\
        .select_from(Subject).join(Teacher).filter(Teacher.id == 1).all()
    return result


def select_06():
    """
    SELECT s.id, s.fullname, s.group_id as group_id
    FROM students s
    WHERE s.group_id = 1
    ORDER BY s.fullname ASC
    """
    result = session.query(Student.id, Student.fullname)\
        .select_from(Student).filter(Student.group_id == 1).order_by(Student.fullname).all()
    return result


def select_07():
    """
    SELECT s.group_id, s.fullname, g.subject_id, g.grade
    FROM students s
    JOIN grades g on g.student_id = s.id
    WHERE s.group_id = 2 AND g.subject_id = 1
    ORDER BY s.fullname;
    """
    result = session.query(Student.group_id, Student.fullname, Grade.subject_id, Grade.grade)\
        .select_from(Student).join(Grade).filter(Student.group_id == 2).filter(Grade.subject_id == 1)\
        .order_by(Student.fullname).all()
    return result


def select_08():
    """
    SELECT AVG(g.grade) as avg_grade
    FROM teachers t
    JOIN subjects s ON s.teacher_id = t.id
    JOIN grades g ON g.subject_id = s.id
    WHERE t.id = 1 and s.id = 3;
    """
    result = session.query(func.round(func.avg(Grade.grade), 0).label('average_grade')) \
        .select_from(Teacher).join(Subject).join(Grade).filter(Teacher.id == 1, Subject.id == 3).all()
    return result


def select_09():
    """
    SELECT sub.id, sub.name
    FROM students s
    JOIN grades g ON g.student_id = s.id
    JOIN subjects sub ON sub.id = g.subject_id
    WHERE s.id = 4
    group by sub.id;
    """
    result = session.query(Subject.id, Subject.name)\
        .select_from(Student).join(Grade).join(Subject).filter(Student.id == 1).group_by(Subject.id).all()
    return result


def select_10():
    """
    SELECT s.fullname, t.fullname, sub.name
    FROM students s
    JOIN grades g ON g.student_id = s.id
    JOIN subjects sub ON sub.id = g.subject_id
    JOIN teachers t ON t.id =sub.teacher_id
    WHERE s.id = 4 AND t.id = 4
    group by s.id, t.id, sub.id
    """
    result = session.query(Student.fullname, Teacher.fullname, Subject.name) \
        .select_from(Student).join(Grade).join(Subject).join(Teacher)\
        .filter(Student.id == 1, Teacher.id == 4).\
        group_by(Student.id, Teacher.id, Subject.id).all()
    return result


def select_11():
    """
    SELECT s.fullname as student_name, t.fullname as teacher_name, AVG(g.grade) as avg_grade
    FROM students s
    JOIN grades g ON g.student_id = s.id
    JOIN subjects sub ON sub.id = g.subject_id
    JOIN teachers t ON t.id =sub.teacher_id
    WHERE t.id = 4 AND s.id = 5
    GROUP BY s.id, t.id
    """
    result = session.query(
        Student.fullname.label('student_name'),\
        Teacher.fullname.label('teacher_name'),\
        func.round(func.avg(Grade.grade).label('avg_grade')))\
        .select_from(Student).join(Grade).join(Subject).join(Teacher)\
        .filter(Teacher.id == 4, Student.id == 5)\
        .group_by(Student.id, Teacher.id).all()
    return result


def select_12():
    """
    select s.id, s.fullname, g.grade, g.grade_date
    from grades g
    join students s on g.student_id = s.id
    where g.subject_id = 1 and s.group_id = 1 and g.grade_date = (
        select max(grade_date)
        from grades g
        join students s on s.id = g.id
        where g.subject_id = 1 and s.group_id = 1
    );
    """

    subquery = (select(func.max(Grade.grade_date)).join(Student).filter(and_(
        Grade.subject_id == 1, Student.group_id == 1
    ))).scalar_subquery()

    result = session.query(Student.id, Student.fullname, Grade.grade, Grade.grade_date)\
        .select_from(Grade)\
        .join(Student)\
        .filter(and_(Grade.subject_id == 1, Student.group_id == 1, Grade.grade_date == subquery)).all()
    return result


if __name__ == '__main__':
    print(select_01())
    print(select_02())
    print(select_03())
    print(select_04())
    print(select_05())
    print(select_06())
    print(select_07())
    print(select_08())
    print(select_09())
    print(select_10())
    print(select_11())
    print(select_12())




