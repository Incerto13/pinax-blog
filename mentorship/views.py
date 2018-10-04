
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from .models import Connection, ConnectionRequest
from .forms import ConnectionRequestForm
from django.views.generic import ListView


@login_required
def new_connection_request(request):
    if request.method == "POST":
        connection_request = ConnectionRequest(from_user=request.user)
        form = ConnectionRequestForm(instance=connection_request, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('account:index')
    else:
        form = ConnectionRequestForm()
    return render(request, "mentorship/new_connection_request_form.html", {'form': form})


@login_required
def accept_connection(request, id):
    connection_request = get_object_or_404(ConnectionRequest, pk=id)
    if not request.user == connection_request.to_user:
        raise PermissionDenied
    if request.method == 'POST':
        if "accept" in request.POST:
            connection = Connection.objects.create(
                mentor=connection_request.to_user,
                mentee=connection_request.from_user,
            )
        connection_request.delete()
        return render(request, "mentorship/connection_detail.html",
                      {'connection': connection}
                      )
    else:
        return render(request,
                      "mentorship/accept_connection_form.html",
                      {'connection_request': connection_request}
                      )


@login_required()
def connection_detail(request, id):
    connection = get_object_or_404(Connection, pk=id)
    return render(request,
                  "mentorship/connection_detail.html",
                  {'connection': connection}
                  )


class AllConnectionsList(ListView):
    model = Connection
