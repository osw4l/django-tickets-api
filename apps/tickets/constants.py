from django.db import models


class Status(models.TextChoices):
    PENDING = "PENDING", "PENDING"
    IN_PROGRESS = "IN_PROGRESS", "IN_PROGRESS"
    FINISHED = "FINISHED", "FINISHED"
    ERROR = "ERROR", "ERROR"

