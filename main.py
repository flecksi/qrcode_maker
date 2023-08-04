from fastapi import FastAPI, Response
from fastapi.responses import FileResponse
import qrcode
import io

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "ok"}


# a GET endpoint to create a qrcode and return it as png-file
# the endpoint should accept a query parameter "text" and return a qrcode with the text
@app.get(
    "/qrcode",
    response_class=FileResponse,
    response_description="Return a qrcode as png-file",
)
async def get_qrcode(text: str):
    img = qrcode.make(text)
    f = io.BytesIO()
    img.save(f, "PNG")

    return Response(f.getvalue(), media_type="image/png")