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


class Tag(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return f"<Tag {self.name}> pk={self.pk}"


class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, related_name="articles")

    def __str__(self):
        return f"<Article> pk={self.pk}"
