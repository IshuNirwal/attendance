from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import qrcode 


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

    def __str__(self) :
        return f"{self.name}"

    def generate_qr_code(self):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(self.employee_id)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        qr_filename = f"{self.employee_id}.png" 
        qr_path = f'barcode/{qr_filename}'  
        full_path = f'media/{qr_path}'  
        img.save(full_path)

        return qr_path

    def save(self, *args, **kwargs):
        if not self.employee_id:
            last_employee = Employee.objects.order_by('-id').first()
            if last_employee:
                last_id = int(last_employee.employee_id[2:])
                new_id = f"AP{str(last_id + 1).zfill(3)}"
            else:
                new_id = "AP001"
            self.employee_id = new_id

        qr_path = self.generate_qr_code()  
        self.barcode = qr_path 

        super().save(*args, **kwargs)

    def has_module_perms(self, app_label):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return self.is_admin


class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    arrivaltime = models.DateTimeField(auto_now_add=True)
    departuretime = models.DateTimeField(auto_now_add=True)
    is_present=models.BooleanField(default=False)

    def __str__(self) :
        return f"{self.employee}"