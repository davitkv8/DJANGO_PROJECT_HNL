from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator
from PIL import Image


class TeachersProfile(models.Model):

    birth_date = models.DateField(blank=False, null=False)
    full_name = models.CharField(blank=False, null=False, max_length=55)
    lecture_price = models.PositiveIntegerField(blank=False, null=False, validators=[MaxValueValidator(10000)])
    description = models.TextField(blank=False, null=False, max_length=6000)
    platform_choices = (
        ('', ''),
        ('Google Meet', 'Google Meet'),
        ('Microsoft Teams', 'Microsoft Teams'),
        ('Zoom', 'Zoom'),
        ('Facebook Messenger', 'Facebook Messenger'),
        ('Other', 'Other')
    )
    platform = models.CharField(blank=False, null=False, max_length=55, choices=platform_choices)
    subject_choices = (
        ('', ''),
        ('Mathematics', 'Mathematics'),
        ('Physics', 'Physics'),
        ('Chemistry', 'Chemistry'),
        ('Biology', 'Biology'),
        ('English', 'English'),
        ('Russian', 'Russian')
    )
    subject = models.CharField(blank=False, null=False, max_length=55, default='', choices=subject_choices)
    image = models.ImageField(blank=False, null=False, default='default.jpg', upload_to='teacher_profile_image')
    is_active = models.BooleanField(default=False)
    friends = models.ManyToManyField(User, related_name='friends', blank=True)

    user = models.OneToOneField(User, null=False, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.full_name}'s Profile. (Username : {self.user.username})"

    def get_description(self):
        return self.description[:300]

    def get_friends(self):
        return self.friends.all()

    def get_friends_number(self):
        return self.friends.all().count()

    def get_feedbacks_number(self):
        return self.feedback.all().count()

    def feedback_rating(self):
        sum_rating = 0
        all_feedbacks = self.feedback.all()
        if self.get_feedbacks_number() == 0:
            return 0
        for feedback in all_feedbacks:
            sum_rating += feedback.rating
        return round(sum_rating/self.get_feedbacks_number(), 1)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.height > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


STATUS_CHOICES = (
        ('send', 'send'),
        ('Approve', 'Approve')
    )


class Relationship(models.Model):
    sender = models.ForeignKey(User, null=False, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(TeachersProfile, null=False, on_delete=models.CASCADE, related_name='receiver')
    available_time = ArrayField(models.TextField(max_length=84), blank=True, null=True)
    status = models.CharField(max_length=8, choices=STATUS_CHOICES)

    # def get_friends_number(self):
    #     return Relationship.objects.filter(receiver=self.receiver).all().count()
