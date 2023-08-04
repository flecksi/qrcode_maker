from fastapi import FastAPI, Response
from fastapi.responses import FileResponse
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers.pil import (
    GappedSquareModuleDrawer,
    HorizontalBarsDrawer,
    RoundedModuleDrawer,
)
from qrcode.image.styles.colormasks import RadialGradiantColorMask

import io
import base64
import pathlib

IMG_PATH = pathlib.Path(__file__).parent / "pvbatco_1.png"


def get_qrcode_bytes(text_b64, with_image: bool = False, styled: bool = False) -> bytes:
    text = base64.b64decode(text_b64).decode("utf-8")

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(text)
    qr.make(fit=True)

    img = qr.make_image(
        image_factory=StyledPilImage if styled else None,
        module_drawer=GappedSquareModuleDrawer(),
        color_mask=RadialGradiantColorMask(
            center_color=(255, 0, 0), edge_color=(0, 0, 255)
        ),
        embeded_image_path=IMG_PATH if with_image else None,
    )
    f = io.BytesIO()
    img.save(f, "PNG")

    return f.getvalue()


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "ok"}


# a GET endpoint to create a qrcode and return it as png-file
# the endpoint should accept a query parameter "text" and return a qrcode with the text
@app.get(
    "/qrcode",
    response_class=FileResponse,
    response_description="Return a qrcode as png-file from a base64 encoded text",
)
async def get_qrcode(
    text_b64: str = "SGVsbG8gV29ybGQ=", with_image: bool = False, styled: bool = False
) -> Response:
    return Response(
        get_qrcode_bytes(text_b64, with_image=with_image, styled=styled),
        media_type="image/png",
    )
