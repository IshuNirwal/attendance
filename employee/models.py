from django.db import models
from django.contrib.auth.models import AbstractUser
from barcode import Code128
from barcode.writer import ImageWriter

class Employee(AbstractUser):
    ROLES = (
        ('admin', 'Admin'),
        ('employee', 'Employee'),
    )

    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    role = models.CharField(max_length=20, choices=ROLES, default='employee')
    employee_id = models.CharField(max_length=10, unique=True, blank=True, null=True)
    barcode = models.ImageField(upload_to='barcode/', blank=True, null=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='employee_groups',
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='employee_user_permissions',
        blank=True,
    )

    def generate_barcode(self):
        code = Code128(self.employee_id, writer=ImageWriter())
        barcode_filename = f"{self.employee_id}"
        barcode_path = f'barcode/{barcode_filename}'
        full_path = f'media/{barcode_path}'  
        code.save(full_path)
        return barcode_path

    def save(self):
        if not self.employee_id:
            last_employee = Employee.objects.order_by('-id').first()
            if last_employee:
                last_id = int(last_employee.employee_id[2:])
                new_id = f"AP{str(last_id + 1).zfill(3)}"
            else:
                new_id = "AP001"
            self.employee_id = new_id

        self.username = self.name 
       
        barcode_path = self.generate_barcode()
        self.barcode = barcode_path

        super().save()
