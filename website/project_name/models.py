from django.conf import settings
from django.db import models

class UserProfile(models.Model):
    email_confirmed = models.BooleanField(default=False)

    def email_user(self, subject, message, from_email=None, ignore_confirmed=False):
        if not (ignore_confirmed or self.email_confirmed):
            return False

        self.user.email_user(subject, message, from_email)
        return True

