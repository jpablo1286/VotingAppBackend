# VotingAppBackend
## Introduction
In order to keep this demo project as real as posible i built an Application in a non-monolitic approach, for this we have an **UI** (user interface) and a **Backend**, this application is deplyed using **Docker containers** with docker-compose all of this over **AWS infrastrcutre** deployed using **Ansible** so a the end of the day we have four repositories.
1. **UI:** https://github.com/jpablo1286/VotingAppUI
2. **Backend:** https://github.com/jpablo1286/VotingAppBackend
3. **Docker containers :** https://github.com/jpablo1286/VotingAppDocker
4. **Ansible Playbooks:** https://github.com/jpablo1286/VotingAppAnsible

## Check the working app visiting this link http://votingapp.juanrivera.org/ ##


# Backend

For develop this Backend i used Python with Django Rest Framework.
Basically we only have a single Model (Vote) and a few Views for CRUD methods, additional we have a couple Views for getting statisitcs for Cats, Dogs and Colors, as described by **urls.py** file.
> urlpatterns = [
    path('api-token-auth', obtain_auth_token, name='api_token_auth'),
    path('vote/list', views.VoteList.as_view(), name='VoteList'),
    path('vote/pets', views.PetsList.as_view(), name='PetsList'),
    path('vote/colors', views.ColorsList.as_view(), name='ColorsList'),
    path('vote/create', views.VoteCreate.as_view(), name='VoteCreate'),
    path('vote/update/<str:id>', views.VoteUpdate.as_view(), name='VoteUpdate'),
    path('vote/delete/<str:id>', views.VoteDelete.as_view(), name='VoteDelete'),
]

this backend persist data using a MySQL Database.
