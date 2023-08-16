from json import dumps

from aiohttp.web import RouteTableDef, Request, Response
from aiohttp.web_exceptions import HTTPBadRequest
from pydantic import ValidationError

from src.schemas.image import ImageSchema
from src.schemas.toast import ToastSchema
from src.utils.web.image import apply_image
from src.utils.web.require_login import require_login

router = RouteTableDef()


@router.post("/images")
@require_login
async def images_post(request: Request) -> Response:
    form = await request.post()

    image = form.get("file")

    if image is None:
        raise HTTPBadRequest(
            headers={
                "HX-Trigger": dumps(
                    {
                        "toast": ToastSchema(
                            message="Неверные параметры запроса"
                        ).model_dump()
                    }
                )
            },
        )

    uploaded_file = apply_image(image.file.read())

    return Response(
        status=200,
        text="Файл загружен",
        headers={
            "Uploaded-Name": uploaded_file,
        },
    )


@router.delete("/images")
@require_login
async def images_delete(request: Request) -> Response:
    form = await request.post()

    try:
        data = ImageSchema.model_validate(form)

    except ValidationError:
        raise HTTPBadRequest(
            headers={
                "HX-Trigger": dumps(
                    {
                        "toast": ToastSchema(
                            message="Неверные параметры запроса"
                        ).model_dump()
                    }
                )
            },
        )
