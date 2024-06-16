import base64
import io
import uuid

from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image


def convert_to_base64(image: InMemoryUploadedFile) -> str:
    """Convert image from htmx file input to base64."""
    image = Image.open(image)

    image = image.resize((320, 320))

    img_io = io.BytesIO()
    image.save(img_io, format='PNG')
    img_io.seek(0)

    return base64.b64encode(img_io.read()).decode()


def convert_from_base64(image: str) -> InMemoryUploadedFile:
    """Convert base64 image to django image format."""
    data = base64.b64decode(image.encode('UTF-8'))

    buf = io.BytesIO(data)
    img = Image.open(buf)
    img_io = io.BytesIO()
    img.save(img_io, format='PNG')
    img_io.seek(0)
    return InMemoryUploadedFile(
        img_io, field_name=None,
        name=str(uuid.uuid1()) + ".jpg",
        content_type='image/png',
        size=img_io.tell(),
        charset=None
    )
