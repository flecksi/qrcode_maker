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
async def get_qrcode(text_b64: str = "SGVsbG8gV29ybGQ="):
    IMG_PATH = pathlib.Path(__file__).parent / "pvbatco_1.png"

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
        # fill_color="black",
        # back_color="white",
        image_factory=StyledPilImage,
        module_drawer=GappedSquareModuleDrawer(),
        color_mask=RadialGradiantColorMask(
            center_color=(255, 0, 0), edge_color=(0, 0, 255)
        ),
        embeded_image_path=IMG_PATH,
    )
    # img = qrcode.make(text)
    f = io.BytesIO()
    img.save(f, "PNG")

    # with open("qrcode.png", "wb") as f2:
    #     img.save(f2, "PNG")
    # img.save("qrcode_gapped.png")
    return Response(f.getvalue(), media_type="image/png")
