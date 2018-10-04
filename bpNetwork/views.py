from django.shortcuts import render, redirect


def welcome(request):
    if request.user.is_authenticated:
        return redirect('account:index')
    else:
        return render(request, 'bpNetwork/welcome.html')