from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Park, Like
from .forms import CommentCreateForm


def like(request, pk):
    park = Park.objects.get(pk=pk)

    if request.user.is_authenticated:  
        likes = Like.objects.filter(author = request.user, park = park)  

        if len(likes) == 0:
            like = Like.objects.create(
                author = request.user,
                park = park,
            )
            like.save()

            park.num_likes += 1
            park.save()

        return redirect("main:home")
    
    return redirect("custom_auth:login")


def delete_like(request, pk):
    park = Park.objects.get(pk=pk)

    if request.user.is_authenticated:  
        likes = Like.objects.filter(author = request.user, park = park)  

        if len(likes) == 0:
            return redirect("main:home")
        else:
            like = Like.objects.get(
                author = request.user,
                park = park,
            )
            like.delete()

            park.num_likes -= 1
            if park.num_likes < 0:
                park.num_likes = 0
            park.save()

        return redirect("main:home")    
            
    return redirect("custom_auth:login")

def favorites(request):
    user = request.user
    likes = Like.objects.filter(author=user)
    parks = []
    for like in likes:
        parks.append(like.park)

    context = {
        "parks" : parks, 
    }        

    return render(request, "main/favorites.html", context)    


@login_required(login_url="/auth/login/")
def create_post_comment(request, pk):
    park = Park.objects.get(pk=pk)

    if request.method == "POST":
        form = CommentCreateForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.park = Park.objects.get(pk=pk)
            comment.save()
            messages.success(request, "The post has been created successfully.")
            
            park.num_comments += 1
            park.save()

            return redirect("main:home")
        else:
            messages.error(request, "Please correct the following errors:")
    else:
        form = CommentCreateForm()

    context = {
        "form": form,
        "park": park
    } 

    return render(request, "parks/create_park_comment.html", context)
