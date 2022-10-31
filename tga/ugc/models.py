from django.db import models


class Profile(models.Model):
    external_id = models.PositiveIntegerField(
        verbose_name='External user ID',
        unique=True,
    )
    name = models.TextField(
        verbose_name='Username',
    )

    def __str__(self):
        return f'#{self.external_id} {self.name}'


class Message(models.Model):
    profile = models.ForeignKey(
        to='ugc.Profile',
        verbose_name='Profile',
        on_delete=models.PROTECT,
    )
    text = models.TextField(
        verbose_name='Text',
    )
    created_at = models.DateTimeField(
        verbose_name='Pick up time',
        auto_now_add=True,
    )

    def __str__(self):
        return f'Message {self.pk} from {self.profile}'
