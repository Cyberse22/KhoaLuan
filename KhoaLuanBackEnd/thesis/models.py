from django.contrib.auth.models import AbstractUser
from django.db import models
from cloudinary.models import CloudinaryField
from django.dispatch import receiver
from django.db.models.signals import post_save


# reviewer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='reviewer_thesis')
# defense_council = models.ForeignKey(DefenseCouncil, on_delete=models.CASCADE, related_name='defense_council_thesis')
# Base Model
class BaseModel(models.Model):
    created_date = models.DateField(auto_now_add=True, null=True)
    updated_date = models.DateField(auto_now=True, null=True)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True


# Models User
class Role(models.TextChoices):
    SINHVIEN = 'sinhvien', 'Sinh Viên'
    GIANGVIEN = 'giangvien', 'Giảng Viên'
    GIAOVUKHOA = 'giaovukhoa', 'Giáo Vụ Khoa'


class Majors(models.TextChoices):
    IT = 'cntt', 'Công Nghệ Thông Tin',
    BT = 'cnsh', 'Công Nghệ Sinh Học',
    BA = 'kdqt', 'Kinh Doanh Quốc Tế'


class CustomUser(AbstractUser):
    id = models.CharField(max_length=10, unique=True, null=False, primary_key=True)
    username = models.CharField(max_length=10, null=False, unique=True)
    first_name = models.CharField(max_length=10, null=False)
    last_name = models.CharField(max_length=50, null=False)
    email = models.EmailField()
    password = models.CharField(max_length=255, null=False)
    avatar = CloudinaryField('avatar', null=True)
    role = models.CharField(max_length=255, choices=Role.choices, default=Role.SINHVIEN)
    major = models.CharField(max_length=255, choices=Majors.choices, default=Majors.IT)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['id']


@receiver(post_save, sender=CustomUser)
def assign_default_avatar(sender, instance, created, **kwargs):
    if created and not instance.avatar:
        instance.avatar = 'https://res.cloudinary.com/dnjupjumj/image/upload/v1707143617/fbcenucmko5hqwerew9w.jpg'
        instance.save()


# Models DefenseCouncil
class DefenseCouncil(BaseModel):
    id = models.CharField(null=False, primary_key=True, unique=True, max_length=10)
    president = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='president')
    secretary = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='secretary')
    reviewer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='reviewer')
    members = models.ManyToManyField(CustomUser, related_name='members')
    thesis = models.ManyToManyField('Thesis', related_name='thesis_check')


# Models Thesis
def thesis_file_default():
    return 'thesis.pdf'


class Thesis(BaseModel):
    id = models.CharField(null=False, primary_key=True, unique=True, max_length=10)
    name = models.CharField(null=False, max_length=255)
    students = models.ManyToManyField(CustomUser, related_name='student_thesis')
    advisors = models.ManyToManyField(CustomUser, related_name='advisor_thesis')
    file_thesis = models.FileField(upload_to='file_thesis', default=thesis_file_default())
    date_defend = models.DateField()
    is_defend = models.BooleanField(default=False)


# Models Score
class ThesisScore(BaseModel):
    thesis = models.ForeignKey(Thesis, on_delete=models.CASCADE, related_name='thesis_score')
    council = models.ForeignKey(DefenseCouncil, on_delete=models.CASCADE, related_name='council_score')
    score = models.DecimalField(max_digits=5, decimal_places=2)
    criteria = models.JSONField()
