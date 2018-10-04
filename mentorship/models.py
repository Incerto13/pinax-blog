from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.conf import settings
from django.urls import reverse
from django.db.models import Q



class ConnectionsQuerySet(models.QuerySet):
    def connections_for_user(self, user):
        return self.filter(
            Q(mentor=user) | Q(mentee=user)
        )


@python_2_unicode_compatible # on python2 this will automatically add a unicode method to model
class Connection(models.Model):
    mentor = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="mentor_connections", on_delete=models.CASCADE)
    mentee = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="mentee_connections", on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    last_active = models.DateTimeField(auto_now=True)

    objects = ConnectionsQuerySet.as_manager()

    def get_absolute_url(self):
        return reverse('connection_detail', args=[self.id])

    def __str__(self):
        return "{0} {1} --- {2} {3}".format(
            self.mentor.first_name, self.mentor.last_name,
            self.mentee.first_name, self.mentee.last_name)


class ConnectionRequest(models.Model):
    from_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="requests_sent",
        on_delete=models.CASCADE,
    )

    to_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="requests_received",
        verbose_name="Mentor to request",
        help_text="Please select the mentor you want to connect with",
        on_delete=models.CASCADE,
    )

    message = models.CharField(
        max_length=300, blank=True,
        verbose_name="Optional Message",
        help_text="It's always nice to add a friendly message!",
    )

    timestamp = models.DateTimeField(auto_now_add=True)


