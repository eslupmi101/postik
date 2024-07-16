from django.conf import settings
import qrcode
from qrcode.image.svg import SvgPathImage
from io import BytesIO


def generate_qr_code_svg(data: str) -> str:
    # Создаем QR-код
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=5,  # Размер квадрата в QR-коде
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    # Генерируем SVG
    img = qr.make_image(image_factory=SvgPathImage)

    # Получаем SVG-строку
    buffer = BytesIO()
    img.save(buffer)
    svg_data = buffer.getvalue().decode()

    # Изменяем размер SVG на 180x180 пикселей
    svg_data = svg_data.replace('width="', 'width="200"').replace('height="', 'height="200"')

    return svg_data


def get_telegram_auth_link(request) -> str:
    # if session don't created
    # TODO fix, sessions don't created automatically
    if not request.session.session_key:
        request.session.save()

    session_id = request.session.session_key

    return f'tg://resolve?domain={settings.BOT_MANAGER_NAME}&start={session_id}'
