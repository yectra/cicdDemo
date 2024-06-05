from fastapi.testclient import TestClient
import zipfile
from io import BytesIO
#from ..api.main import app

# D:\QR\tests\test_api.py
from api.main import app  # Assuming your main application file is named main.py

client = TestClient(app)


def test_generate_qr_multiple_urls():
    urls = ["https://www.example.com/", "https://www.wikipedia.org/"]
    response = client.post("/generate_qr_codes/", params={"urls": urls})
    assert response.status_code == 200

def test_generate_qr_phone_numbers():
    phone_numbers = ["1234567890", "+447912345678"]
    response = client.post("/generate_qr_codes_phone/", params={"phone_numbers": phone_numbers})
    assert response.status_code == 200

def test_generate_qr_emails():
    emails = ["test@example.com", "another@domain.com"]
    response = client.post("/generate_qr_codes_email/", params={"emails": emails})
    assert response.status_code == 200