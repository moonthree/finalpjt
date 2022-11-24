from django.db import models
from django.conf import settings
# Create your models here.


class Genre(models.Model):
    genre_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)


class Actor(models.Model):
    person_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    gender = models.IntegerField()
    popularity = models.IntegerField()
    profile_path = models.TextField(null=True)
    biography = models.TextField(null=True)
    birthday = models.CharField(max_length=255)


class Movie(models.Model):
    # auto_increment_id = models.AutoField(primary_key = True)
    # movie_id = models.ForeignKey(Credit, on_delete=models.CASCADE)
    movie_id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=100)
    popularity = models.IntegerField()
    vote_avg = models.IntegerField()
    overview = models.TextField()
    released_date = models.DateField()
    poster_path = models.TextField(null=True)
    backdrop_path = models.TextField(null=True)
    genres = models.ManyToManyField(
        Genre, related_name='genre_contained_movies')
    # movie_credits = models.ManyToManyField(Credit, related_name='genre_contained_movies')


class Video(models.Model):
    video_id = models.CharField(max_length=255, primary_key=True)
    movie_id = models.ForeignKey(Movie, on_delete=models.CASCADE)
    key = models.TextField(null=True)
    name = models.CharField(max_length=255)
    iso_639_1 = models.CharField(max_length=255)
    published_at = models.CharField(max_length=255)
    iso_3166_1 = models.CharField(max_length=255)
    site = models.CharField(max_length=255)


class Credit(models.Model):
    # movie_id = models.IntegerField(primary_key = True)
    auto_increment_id = models.AutoField(primary_key=True)
    person_id = models.IntegerField()
    # person_id = models.ForeignKey(Actor, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    popularity = models.IntegerField()
    character = models.CharField(max_length=100)
    profile_path = models.TextField(null=True)
    credit_movies = models.ManyToManyField(
        Movie, related_name='movie_contained_credits')


class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    content = models.TextField()
    likes = models.IntegerField(default=0)
    rate = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='like_comments', blank=True)


# class CommentLike(models.Model):
#     like_id = models.AutoField(primary_key=True)
#     comment_id = models.ForeignKey(Comment, on_delete=models.CASCADE)
#     user_id = models.ForeignKey(settings.AUTH_USER_MODEL,
#                                 on_delete=models.CASCADE)


class ClickedMovies(models.Model):
    clicked_movie_id = models.AutoField(primary_key=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)


class UnseenMovies(models.Model):
    unseen_movie_id = models.AutoField(primary_key=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
