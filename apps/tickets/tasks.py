from celery import shared_task
import cloudinary.uploader
from io import BytesIO
from .models import TicketImage


@shared_task(name='tickets.upload_image')
def upload_image(photo_id, file_data, file_format='jpg'):
    image = TicketImage.objects.get(uuid=photo_id)
    image.set_in_progress()
    
    try:
        result = cloudinary.uploader.upload(
            BytesIO(file_data), 
            resource_type="image", 
            format=file_format
        )
        image.finish_upload(cloudinary_result=result)
    except Exception as e:
        image.set_error()
        raise e
        
    return result

