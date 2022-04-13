from django.db import models


class Category(models.Model):

    name = models.CharField(max_length=200),
    slug = models.SlugField(max_length=200, unique=True)


class Review(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE, related_name='reviews')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    score = models.IntegerChoices('Оценка', '1 2 3 4 5 6 7 8 9 10')
    
    def __str__(self):
        return self.text


class Comment(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text