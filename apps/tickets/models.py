import uuid
from django.core.validators import MinValueValidator
from django.db import models, transaction
from cloudinary.models import CloudinaryField
from .constants import Status
from .utils import get_file_extension


class StatusModel(models.Model):
    uuid = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False
    )
    status = models.CharField(
        max_length=15,
        choices=Status,
        default=Status.PENDING
    )

    class Meta:
        abstract = True


class Ticket(StatusModel):
    user = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE
    )
    total_images = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1)
        ]
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        verbose_name = "Ticket"
        verbose_name_plural = "Tickets"

    def __str__(self):
        return str(self.uuid)
    
    def can_add_images(self):
        return self.images.count() < self.total_images and self.status is not Status.FINISHED
    
    def add_image(self, file):
        from .tasks import upload_image

        file_format = get_file_extension(file)
        file = file.read()

        image = self.images.create()
        
        upload_image.delay(
            photo_uuid=str(image.uuid), 
            file_format=file_format,
            file_data=file
        )

    def set_error(self):
        self.status = Status.ERROR
        self.save(update_fields=['status'])

    def finish(self):
        self.status = Status.FINISHED
        self.save(update_fields=['status'])
    
    def check_status(self):
        images = self.images.all()
        total_images = self.total_images
        
        if len(images) == total_images and all(image.status == Status.FINISHED for image in images):
            self.finish()


class TicketImage(StatusModel):
    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = CloudinaryField(
        'image',
        editable=False,
        blank=True,
        null=True
    )

    def set_in_progress(self):
        self.status = Status.IN_PROGRESS
        self.save(update_fields=['status'])

    @transaction.atomic
    def finish_upload(self, cloudinary_result):
        self.image = cloudinary_result['url']
        self.status = Status.FINISHED
        self.save(update_fields=[
            'image',
            'status'
        ])
        self.ticket.check_status()

    @transaction.atomic
    def set_error(self):
        self.status = Status.ERROR
        self.save(update_fields=['status'])
        self.ticket.set_error()

