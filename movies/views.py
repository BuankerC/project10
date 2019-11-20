from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from .models import Movie, Genre, Review
from .forms import ReviewForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST


# Create your views here.

def index(request):
    movies = Movie.objects.all()
    context = {
        'movies': movies
    }
    return render(request, 'movies/index.html', context)


def detail(request, id):
    movie = get_object_or_404(Movie, id=id)
    review_form = ReviewForm
    context = {
        'movie': movie,
        'review_form': review_form
    }
    return render(request, 'movies/detail.html', context)


@login_required
@require_POST
def review(request, id):
    movie = get_object_or_404(Movie, id=id)
    if request.method == "POST":
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.movie = movie
            review.user = request.user
            review.save()
            return redirect('movies:detail', id)


@require_POST
def review_delete(request, id, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.user == review.user:
        review.delete()
    return redirect('movies:detail', id)


@login_required
def like(request, id):
    movie = get_object_or_404(Movie, id=id)
    user = request.user
    if user in movie.like_users.all():
        movie.like_users.remove(user)
    else:
        movie.like_users.add(user)
    return redirect('movies:detail', id)
