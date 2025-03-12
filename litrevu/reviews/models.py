from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


from django.db import models
from django.conf import settings

class Ticket(models.Model):
    """
    Represents a ticket created by a user.

    :param title: The title of the ticket.
    :type title: str
    :param description: A detailed description of the ticket.
    :type description: str
    :param user: The user who created the ticket.
    :type user: settings.AUTH_USER_MODEL
    :param image: An optional image associated with the ticket.
    :type image: ImageField
    :param time_created: The timestamp when the ticket was created.
    :type time_created: datetime
    :return: A string representation of the ticket.
    :rtype: str
    """
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=2048, blank=True)
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to='ticket_images/', null=True, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} (by {self.user.username})"


class Review(models.Model):
    """
    Represents a review for a ticket.

    :param ticket: The ticket being reviewed.
    :type ticket: Ticket
    :param rating: The rating given in the review, between 0 and 5.
    :type rating: int
    :param headline: The headline of the review.
    :type headline: str
    :param body: The body text of the review.
    :type body: str
    :param user: The user who wrote the review.
    :type user: settings.AUTH_USER_MODEL
    :param time_created: The time when the review was created.
    :type time_created: datetime
    :return: A string representation of the review.
    :rtype: str
    """
    ticket = models.ForeignKey(
        to=Ticket,
        on_delete=models.CASCADE
    )
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    headline = models.CharField(max_length=128)
    body = models.TextField(max_length=8192, blank=True)
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.ticket.title} by {self.user.username}"


class UserFollows(models.Model):
    """
    Represents a following relationship between users.

    :param user: The user who is following another user.
    :type user: ForeignKey to AUTH_USER_MODEL
    :param followed_user: The user who is being followed.
    :type followed_user: ForeignKey to AUTH_USER_MODEL
    :return: A string representation of the following relationship.
    :rtype: str
    """
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='following'
    )
    followed_user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='followed_by'
    )

    class Meta:
        unique_together = ('user', 'followed_user', )

    def __str__(self):
        return f"{self.user.username} follows {self.followed_user.username}"
