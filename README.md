# Project 10

Project 07에 이어서.....



## 느낀점

- 잊었던 기억이 새록새록 떠올랐다. 공부를 안하면 금방 잊는다는 것을 깨달았다. 분명 얼마전만 해도 다 알았던 것같은데 오랜만에 하니까 기억이 하나도 안나서 당황스러웠다. 그래도 이렇게 같이 프로젝트를 하면서 서로 모르는것을 알려주고 복습을 해서 유익한 시간이였다.



## Modeling

`movies` App

```python
# models.py

from django.db import models
from django.conf import settings
# Create your models here.


class Genre(models.Model):
    name = models.CharField(max_length=50)


class Movie(models.Model):
    title = models.CharField(max_length=100)
    audience = models.IntegerField()
    poster_url = models.TextField()
    description = models.TextField()
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    # genres = models.ManyToManyField(Genre, related_name="movies")
    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='like_movies')


class Review(models.Model):
    content = models.CharField(max_length=100)
    score = models.IntegerField()
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)

```

> genre와 movie를 N:M으로 연결하기 위해서 ManyToManyField로 연결해주었지만, 가져오는 영화 정보에서 장르가 하나씩만 할당이 되어서 정보를 읽어오는데 문제가 있어서 그냥 기존에 했던 방법( ForeingKey)대로 가져왔다.



`accounts` App

```python
# models.py

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
# Create your models here.


class User(AbstractUser):
    followers = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="followings")

```

> follw 기능은 user 모델과 ManyTOMany로 연결해준다.



## Follow

`account` App

```python
# views.py

def follow(request, id):
    you = get_object_or_404(User, id=id)
    me = request.user

    if me.is_authenticated and you != me:
        if you.followers.filter(id=me.id):
            you.followers.remove(me)
        else:
            you.followers.add(me)
    return redirect('accounts:userpage', id)
```

> 팔로우 기능은 팔로잉을 했는지, 팔로우를 했는지 구별하여서 팔로워 추가/삭제 한다.



userpage.html

```html
{% if user not in user_info.followers.all %}
  <a href="{% url 'accounts:follow' user_info.id %}">팔로우</a>
  {% else %}
  <a href="{% url 'accounts:follow' user_info.id %}">팔로우 취소</a>
{% endif %}
```

> 팔로우 여부에 따라서 화면에 나타나는 글이 다르게 표시하였다.

