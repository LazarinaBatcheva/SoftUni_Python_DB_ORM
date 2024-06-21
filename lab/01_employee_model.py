class Employee(models.Model):
    name = models.CharField(
        max_length=30,
    )
    email_address = models.EmailField()
    photo = models.URLField()
    birth_date = models.DateField()
    works_full_time = models.BooleanField()
    created_on = models.DateTimeField(
        auto_now_add=True,
    )
