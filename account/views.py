from django.contrib.auth import login, authenticate
from django.views.generic import CreateView, UpdateView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from taggit.views import *

from .models import User
from .forms import SignUpForm, UpdateProfileForm
from mentorship.models import Connection


@login_required
def index(request):
    my_connections = Connection.objects.connections_for_user(request.user)
    pending_requests = request.user.requests_received.all()
    return render(request, "account/index.html",
                  {'pending_requests': pending_requests,
                   'my_connections': my_connections,
                  })


class UpdateProfileView(UpdateView):
    form_class = UpdateProfileForm
    template_name = 'account/user_update_form.html'
   # fields = ['username', 'first_name', 'last_name', 'email', 'city', 'zipcode',
    #             'state', 'country', 'bio', 'birth_date', 'organization', 'image']
    #TagField = {'tags'}

    slug_field = 'username'
    slug_url_kwarg = 'slug'

    def get(self, request, **kwargs):
        user = request.user

        form = self.form_class(instance=request.user,
                               initial={'username': user.username,
                                        'first_name': user.first_name,
                                        'last_name': user.last_name,
                                        'email': user.email,
                                        'city': user.city,
                                        'zipcode': user.zipcode,
                                        'state': user.state,
                                        'country': user.country,
                                        'bio': user.bio,
                                        'birth_date': user.birth_date,
                                        'organization': user.organization,
                                        'image': user.image,
                                        'tags': user.tag_string(),
                                        })

        return render(request, self.template_name, {"form": form})

    def post(self, request, **kwargs):
        form = self.form_class(request.POST, instance=request.user)
        if form.is_valid():
            tags = form.cleaned_data['tags']
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            form.save_m2m()
            profile.tags.set(*tags)
            return redirect('account:index')

        return render(request, self.template_name, {'form': form})



def user_detail(request, username):
    user = get_object_or_404(User, username=username)
    # parsing the list of tags and putting it into a string
    tag_string = user.tag_string()
    # User object below needs to be capitalized for access to the 'Manager'
    context = {'user': user,
               #'tags': tags,
               'tag_string': tag_string,
               }
    return render(request, 'account/user_detail.html', context)


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = "account/signup_form.html"

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            raw_password = form.cleaned_data["password1"]
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('account:index')

        return render(request, self.template_name, {'form': form})
