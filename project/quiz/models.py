from django.db import models
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=255)
    normal_threshold = models.FloatField(default=47)
    monitoring_threshold = models.FloatField(default=38.4)

    def __str__(self):
        return self.name

class Test(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(null=True)

    def __str__(self):
        return self.title

class Question(models.Model):
    content = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to='quiz/', blank=True, null=True)
    audio_file = models.FileField(upload_to='audio/', blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    test = models.ForeignKey(Test, related_name='questions', on_delete=models.CASCADE)

    class Meta:
        ordering = ['category']

    def __str__(self):
        return self.content

class Choice(models.Model):
    question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    weight = models.FloatField(default=1.0)

    def __str__(self):
        return self.text

class UserTestResult(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    completed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.test.title}"

class UserAnswer(models.Model):
    user_test_result = models.ForeignKey(UserTestResult, related_name='answers', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)  # Example default value

    def __str__(self):
        return f"{self.question.content} - {self.choice.text}"
