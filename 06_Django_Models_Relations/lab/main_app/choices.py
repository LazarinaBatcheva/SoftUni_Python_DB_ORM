from django.db import models


class StudentEnrollmentGradeChoice(models.TextChoices):
    A = 'A', 'A'
    B = 'B', 'B'
    C = 'C', 'C'
    D = 'D', 'D'
    F = 'F', 'F'
