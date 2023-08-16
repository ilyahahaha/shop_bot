from hashlib import md5
from io import BytesIO
from pathlib import Path

from PIL import Image
from aiofiles.os import remove

from src.common.exceptions import FileNotExistsError
from src.common.settings import Settings

settings = Settings()


def apply_image(image: bytes) -> str:
    buffer = BytesIO(image)

    file_name = f"{md5(image).hexdigest()}.jpeg"

    image = Image.open(buffer)

    if image.mode in ("RGBA", "P"):
        image = image.convert("RGB")

    image.save(Path(settings.base_dir).parent / "images" / file_name, format="JPEG")

    return file_name


async def remove_image(file_name: str) -> None:
    try:
        await remove(Path(settings.base_dir).parent / "images" / file_name)
    except OSError:
        raise FileNotExistsError(f"Файл с названием {file_name} не найден")
