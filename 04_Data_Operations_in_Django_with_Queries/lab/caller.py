import os
import django
from datetime import date

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import Student


def add_students() -> None:
    Student.objects.create(
        student_id='FC5204',
        first_name='John',
        last_name='Doe',
        birth_date='1995-05-15',
        email='john.doe@university.com',
    )

    Student.objects.create(
        student_id='FE0054',
        first_name='Jane',
        last_name='Smith',
        birth_date=None,
        email='jane.smith@university.com',
    )

    Student.objects.create(
        student_id='FH2014',
        first_name='Alice',
        last_name='Johnson',
        birth_date='1998-02-10',
        email='alice.johnson@university.com',
    )

    student = Student(
        student_id='FH2015',
        first_name='Bob',
        last_name='Wilson',
        birth_date='1996-11-25',
        email='bob.wilson@university.com',
    )
    student.save()


def get_students_info() -> str:
    students_records = []
    all_students = Student.objects.all()

    for student in all_students:
        students_records.append(f'Student №{student.student_id}: '
                                f'{student.first_name} {student.last_name}; '
                                f'Email: {student.email}')

    return '\n'.join(students_records)

    # all_students = Student.objects.all()
    #
    # return '\n'.join(str(s) for s in all_students)


def update_students_emails() -> None:
    all_students = Student.objects.all()

    for student in all_students:
        student.email = student.email.replace(student.email.split('@')[1], 'uni-students.com')

    Student.objects.bulk_update(all_students, ['email'])


def truncate_students() -> None:
    Student.objects.all().delete()


# test code

# add_students()
# print(Student.objects.all())

# print(get_students_info())

# update_students_emails()
# for student in Student.objects.all():
#     print(student.email)

# truncate_students()
# print(Student.objects.all())
# print(f"Number of students: {Student.objects.count()}")
