from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import UserManager
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db import models
from django.contrib.auth.models import AbstractUser




class CustomUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = CustomUser(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        assert extra_fields["is_staff"]
        assert extra_fields["is_superuser"]
        return self._create_user(email, password, **extra_fields)


class Session(models.Model):
    start_year = models.DateField()
    end_year = models.DateField()

    def __str__(self):
        return "From " + str(self.start_year) + " to " + str(self.end_year)


class CustomUser(AbstractUser):
    USER_TYPE = ((1, "HOD"), (2, "Staff"), (3, "Student"), (4, "Aios"))
    GENDER = [("M", "Male"), ("F", "Female")]
    
    
    username = None  # Removed username, using email instead
    email = models.EmailField(unique=True)
    user_type = models.CharField(default=1, choices=USER_TYPE, max_length=1)
    gender = models.CharField(max_length=1, choices=GENDER)
    profile_pic = models.ImageField()
    address = models.TextField()
    fcm_token = models.TextField(default="")  # For firebase notifications
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return self.last_name + ", " + self.first_name


class Admin(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)



class Course(models.Model):
    name = models.CharField(max_length=120)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Student(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.DO_NOTHING, null=True, blank=False)
    session = models.ForeignKey(Session, on_delete=models.DO_NOTHING, null=True)
    number =  models.CharField(max_length=120)
    def __str__(self):
        return self.admin.last_name + ", " + self.admin.first_name

class Evidence(models.Model):
    student = models.ForeignKey(Student, on_delete=models.DO_NOTHING)
    file_name = models.CharField(max_length=60)
    priority = models.CharField(max_length=60)
    category = models.CharField(max_length=60)
    evidence_file = models.FileField(upload_to="media", null=True, blank=True)



class Staff(models.Model):
    course = models.ForeignKey(Course, on_delete=models.DO_NOTHING, null=True, blank=False)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.admin.last_name + " " + self.admin.first_name

class Aios(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.admin.last_name + " " + self.admin.first_name


class Subject(models.Model):
    name = models.CharField(max_length=120)
    staff = models.ForeignKey(Staff,on_delete=models.CASCADE,)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Attendance(models.Model):
    session = models.ForeignKey(Session, on_delete=models.DO_NOTHING)
    subject = models.ForeignKey(Subject, on_delete=models.DO_NOTHING)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class AttendanceReport(models.Model):
    student = models.ForeignKey(Student, on_delete=models.DO_NOTHING)
    attendance = models.ForeignKey(Attendance, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class LeaveReportStudent(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.CharField(max_length=60)
    message = models.TextField()
    status = models.SmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class LeaveReportStaff(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    date = models.CharField(max_length=60)
    message = models.TextField()
    status = models.SmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class LeaveReportAios(models.Model):
    aios = models.ForeignKey(Aios, on_delete=models.CASCADE)
    date = models.CharField(max_length=60)
    message = models.TextField()
    status = models.SmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class FeedbackStudent(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    feedback = models.TextField()
    reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class FeedbackStaff(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    feedback = models.TextField()
    reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class FeedbackAios(models.Model):
    aios = models.ForeignKey(Aios, on_delete=models.CASCADE)
    feedback = models.TextField()
    reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class NotificationStaff(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class NotificationAios(models.Model):
    aios = models.ForeignKey(Aios, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class NotificationStudent(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class StudentResult(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    test = models.FloatField(default=0)
    exam = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class AssessmentAnalysis(models.Model):
    ANSWERS_A = [("YES", "YES"), ("NO", "NO"), ("NA", "NA")]
    ANSWERS_B = [("HIGH", "HIGH"), ("MEDIUM", "MEDIUM"), ("LOW", "LOW"), ("NA", "NA")]

    student = models.ForeignKey(Student, on_delete=models.DO_NOTHING)
    subject = models.ForeignKey(Subject, on_delete=models.DO_NOTHING)
    DS1 = models.CharField('Similarity score reported on Turnitln',default="NA", choices=ANSWERS_B, max_length=10)
    DS2 = models.CharField('Is the work submitted by the student very similar to that of another student?',default="NA", choices=ANSWERS_A, max_length=5)
    DS3 = models.CharField('Is there a similarity reported on a block of references in thebibliography?', default="NA", choices=ANSWERS_A, max_length=5)
    DR1 = models.CharField('Are there any references mentioned in the documents that have been submitted by the student?', default="NA", choices=ANSWERS_A, max_length=5)
    DR2 = models.CharField('Has the student used sources that are specific to the assessment topic rather than generic or outdated ones in the references?', default="NA", choices=ANSWERS_A, max_length=5)
    DR3 = models.CharField('Do the citations from the references appear in the text as well?', default="NA", choices=ANSWERS_A, max_length=5)
    DR4 = models.CharField('Is there a reasonable range of reference access dates in bibliography?', default="NA", choices=ANSWERS_A, max_length=5)
    DR5 = models.CharField('Has the student used the correct referencing style as mentioned in the assessment brief?', default="NA", choices=ANSWERS_A, max_length=5)
    DC1 = models.CharField('Do you think that the quality of the student assessment submissions is reasonable considering the students participation and module&#39;s level?', default="NA", choices=ANSWERS_A, max_length=5)
    DC2 = models.CharField('Is the writing style used in the supplied documents overly sophisticated, with minimal evidence of the depth of the study?', default="NA", choices=ANSWERS_A, max_length=5)
    DC3 = models.CharField('Is the level of the English writing in the submitted documents significantly better than the quality of the English used by the student in emails, in-class discussions, and other forms of communication?', default="NA", choices=ANSWERS_A, max_length=5)
    DC4 = models.CharField('Is the students submission generic in nature, failing to address the assignments key focus points?', default="NA", choices=ANSWERS_A, max_length=5)
    DC5 = models.CharField('Are there inappropriate replacements of vocabulary in the work that suggests an attempt to make it plagiarism free?', default="NA", choices=ANSWERS_A, max_length=5)
    DC6 = models.CharField('Are there any indications on the students documents that show the involvement of a third?', default="NA", choices=ANSWERS_A, max_length=5)
    MD1 = models.CharField('Is the students name listed as an author on the assessment submission documents metadata?', default="NA", choices=ANSWERS_A, max_length=5)
    MD2 = models.CharField('Does the “Last saved by” value on the metadata show students name?', default="NA", choices=ANSWERS_A, max_length=5)
    MD3 = models.CharField('Does the documents metadata indicate that the total modification time was minimal?', default="NA", choices=ANSWERS_A, max_length=5)
    MD4 = models.CharField('Is there a realistic change trail reported in the mechanism in place to track changes made to student-submitted files since they were created?', default="NA", choices=ANSWERS_A, max_length=5)

class AcademicEngagement(models.Model):
    ANSWERS_A = [("HIGH", "HIGH"), ("MEDIUM", "MEDIUM"), ("LOW", "LOW"), ("NA", "NA")]

    student = models.ForeignKey(Student, on_delete=models.DO_NOTHING)
    subject = models.ForeignKey(Subject, on_delete=models.DO_NOTHING)

    AG1 = models.CharField('What is the level of engagement of the student in the module?', default="NA", choices=ANSWERS_A, max_length=10)
    LA1 = models.CharField('What is the students level of engagement in the virtual learning environment in terms of the overall interaction expected from the student?', default="NA", choices=ANSWERS_A, max_length=10)
    LA2 = models.CharField('Is there any suspicious activity reported in the students device interaction log, such as concurrent logins from multiplelocations, logins from adifferent geographical area, etc?', default="NA", choices=ANSWERS_A, max_length=10)

class AssessmentDetails(models.Model):
    ANSWERS_A = [("YES", "YES"), ("NO", "NO"), ("NA", "NA")]
    ANSWERS_B = [("HIGH", "HIGH"), ("MEDIUM", "MEDIUM"), ("LOW", "LOW"), ("NA", "NA")]

    subject = models.ForeignKey(Subject, on_delete=models.DO_NOTHING)
    AD1 = models.CharField('Has the lecturer participated in any training/learning sessions on contract cheating hosted by the higher education institute?',default="NA", choices=ANSWERS_B, max_length=10)
    AD2 = models.CharField('Does the assessment design ensure relatively higher possibility of detecting contract cheating?',default="NA", choices=ANSWERS_A, max_length=5)
    AD3 = models.CharField('Is there a similarity reported on a block of references in thebibliography?', default="NA", choices=ANSWERS_A, max_length=5)
    AD4 = models.CharField('Are there any references mentioned in the documents that have been submitted by the student?', default="NA", choices=ANSWERS_A, max_length=5)
    AD5 = models.CharField('Has the student used sources that are specific to the assessment topic rather than generic or outdated ones in the references?', default="NA", choices=ANSWERS_A, max_length=5)
    AD6 = models.CharField('Do the citations from the references appear in the text as well?', default="NA", choices=ANSWERS_A, max_length=5)
    AD7 = models.CharField('Is there a reasonable range of reference access dates in bibliography?', default="NA", choices=ANSWERS_B, max_length=10)
    AD8 = models.CharField('Has the student used the correct referencing style as mentioned in the assessment brief?', default="NA", choices=ANSWERS_B, max_length=10)
    OS1 = models.CharField('Is there any information about the assessment available online on any websites that could indicate the likelihood of outsourcing?', default="NA", choices=ANSWERS_A, max_length=5)
    OS2 = models.CharField('Is there any traceable metadata accessible on the contents of the website which can be associated with the student?', default="NA", choices=ANSWERS_A, max_length=5)
    AP1 = models.CharField('In the live/recorded presentation, does the student appear to be comfortable and confident?', default="NA", choices=ANSWERS_A, max_length=5)


class Viva(models.Model):
    ANSWERS_A = [("YES", "YES"), ("NO", "NO"), ("NA", "NA")]

    student = models.ForeignKey(Student, on_delete=models.DO_NOTHING)
    subject = models.ForeignKey(Subject, on_delete=models.DO_NOTHING)

    V = models.CharField('Is a viva needed? (This is a system generated value based on some facts specified above)', default="NA", choices=ANSWERS_A, max_length=10)
    V1 = models.CharField('Was the students performance in the viva satisfactory?', default="NA", choices=ANSWERS_A, max_length=10)



@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 1:
            Admin.objects.create(admin=instance)
        if instance.user_type == 2:
            Staff.objects.create(admin=instance)
        if instance.user_type == 3:
            Student.objects.create(admin=instance)
        if instance.user_type == 4:
            Aios.objects.create(admin=instance)


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.admin.save()
    if instance.user_type == 2:
        instance.staff.save()
    if instance.user_type == 3:
        instance.student.save()
    if instance.user_type == 4:
        instance.aios.save()
