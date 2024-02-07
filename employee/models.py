from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from barcode import Code128
from barcode.writer import ImageWriter

class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None, **extra_fields):
        if not email:
            raise ValueError('User must have an email address')
        user = self.model(
            email=self.normalize_email(email),
            name=name,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('name', 'Superuser')
        user = self.create_user(
            email,
            password=password,
            **extra_fields,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Employee(AbstractBaseUser):
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

    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    objects = UserManager()
    USERNAME_FIELD = 'email'

    def generate_barcode(self):
        code = Code128(self.employee_id, writer=ImageWriter())
        barcode_filename = f"{self.employee_id}"
        barcode_path = f'barcode/{barcode_filename}'
        full_path = f'media/{barcode_path}'  
        code.save(full_path)
        return barcode_path

    def save(self, *args, **kwargs):
        if not self.employee_id:
            last_employee = Employee.objects.order_by('-id').first()
            if last_employee:
                last_id = int(last_employee.employee_id[2:])
                new_id = f"AP{str(last_id + 1).zfill(3)}"
            else:
                new_id = "AP001"
            self.employee_id = new_id

        barcode_path = self.generate_barcode()
        self.barcode = barcode_path

        super().save(*args, **kwargs)

    def has_module_perms(self, app_label):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return self.is_admin


class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    arrivaltime = models.DateTimeField(auto_now_add=True)
    departuretime = models.DateTimeField(auto_now_add=True)