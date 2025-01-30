from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"<Author {self.name}> pk={self.pk}"


class Category(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return f"<Category {self.name}> pk={self.pk}"


# class Tag(models.Model):
#     name = models.CharField(max_length=20)
#
#     def __str__(self):
#         return f"<Tag {self.name}> pk={self.pk}"
