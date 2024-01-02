import argparse

from sqlalchemy.exc import SQLAlchemyError

from conf.db import session
from conf.models import Teacher


# Функція для обробки опції create
def create_handler(args):
    print(f"Creating {args.model} with name '{args.name}'")
    match args.model:
        case 'Teacher':
            try:
                new_teacher = Teacher(fullname=args.name)
                session.add(new_teacher)
                session.commit()
            except SQLAlchemyError as e:
                print(e)
                session.rollback()
            finally:
                session.close()


# Функція для обробки опції list
def list_handler(args):
    print(f"Listing all {args.model}s")
    match args.model:
        case 'Teacher':
            try:
                teachers_all = session.query(Teacher).all()
                for t in teachers_all:
                    print(t.id, t.fullname)
            except SQLAlchemyError as e:
                print(e)
                session.rollback()
            finally:
                session.close()


# Функція для обробки опції update
def update_handler(args):
    print(f"Updating {args.model} with id={args.id} to name '{args.name}'")
    match args.model:
        case 'Teacher':
            try:
                find_teacher = session.query(Teacher).filter(Teacher.id == args.id).first()
                find_teacher.fullname = args.name
                session.add(find_teacher)
                session.commit()
            except SQLAlchemyError as e:
                print(e)
                session.rollback()
            finally:
                session.close()


# Функція для обробки опції remove
def remove_handler(args):
    print(f"Removing {args.model} with id={args.id}")
    match args.model:
        case 'Teacher':
            try:
                find_teacher = session.query(Teacher).filter(Teacher.id == args.id).first()
                session.delete(find_teacher)
                session.commit()
                session.close()
            except SQLAlchemyError as e:
                print(e)
                session.rollback()
            finally:
                session.close()


def main():
    parser = argparse.ArgumentParser(description="CLI program for CRUD operations with a database")

    # Опції для вказівки дії та моделі
    parser.add_argument('--action', '-a', choices=['create', 'list', 'update', 'remove'], required=True,
                        help="CRUD operation to perform")
    parser.add_argument('--model', '-m', required=True, help="Model on which the operation will be performed")

    # Опції для даних, які необхідно використовувати при виконанні операцій
    parser.add_argument('--id', type=int, help="ID of the record")
    parser.add_argument('--name', help="Fullname of a person or name of the record")

    args = parser.parse_args()

    # Виклик відповідної функції в залежності від обраної опції
    match args.action:
        case 'create':
            create_handler(args)
        case 'list':
            list_handler(args)
        case 'update':
            update_handler(args)
        case 'remove':
            remove_handler(args)


if __name__ == "__main__":
    main()