from fastapi import FastAPI, Query, Form
from fastapi.responses import StreamingResponse
from typing import List
import qrcode
from io import BytesIO
import zipfile
app = FastAPI()
def generate_qr_code(data: str) -> bytes:
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img_bytes = BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    return img_bytes.getvalue()
@app.post("/generate_qr_codes/")
async def generate_qr_codes(urls: List[str] = Query(...)):
    buffer = BytesIO()
    with zipfile.ZipFile(buffer, 'w') as zip_file:
        for i, url in enumerate(urls):
            qr_code = generate_qr_code(url)
            zip_file.writestr(f'qr_code_url_{i+1}.png', qr_code)
    buffer.seek(0)
    return StreamingResponse(buffer, media_type="application/zip", headers={
        'Content-Disposition': 'attachment; filename="qr_codes.zip"'
    })
@app.post("/generate_qr_codes_phone/")
async def generate_qr_codes_phone(phone_numbers: List[str] = Query(...)):
    buffer = BytesIO()
    with zipfile.ZipFile(buffer, 'w') as zip_file:
        for i, phone_number in enumerate(phone_numbers):
            qr_code = generate_qr_code(f"tel:{phone_number}")
            zip_file.writestr(f'qr_code_phone_{i+1}.png', qr_code)
    buffer.seek(0)
    return StreamingResponse(buffer, media_type="application/zip", headers={
        'Content-Disposition': 'attachment; filename="qr_codes_phone.zip"'
    })
@app.post("/generate_qr_codes_email/")
async def generate_qr_codes_email(emails: List[str] = Query(...)):
    buffer = BytesIO()
    with zipfile.ZipFile(buffer, 'w') as zip_file:
        for i, email in enumerate(emails):
            qr_code = generate_qr_code(f"mailto:{email}")
            zip_file.writestr(f'qr_code_email_{i+1}.png', qr_code)
    buffer.seek(0)
    return StreamingResponse(buffer, media_type="application/zip", headers={
        'Content-Disposition': 'attachment; filename="qr_codes_email.zip"'
    })
