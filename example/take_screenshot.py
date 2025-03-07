import base64
from google.cloud import storage # pip install google-cloud-storage
import os
import sys

try:
    from nodriver import cdp, loop, start, Config
except (ModuleNotFoundError, ImportError):
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
    from nodriver import cdp, loop, start, Config


# Google Cloud Storage Upload Function (Direct Upload)
# NOTE: dont forget to set your environment variable GOOGLE_APPLICATION_CREDENTIALS=path/to/credentials.json
def upload_to_gcs(bucket_name, destination_blob_name, image_data):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    # Upload the image bytes directly
    blob.upload_from_string(image_data, content_type="image/jpeg")
    print(f"Screenshot uploaded to gs://{bucket_name}/{destination_blob_name}")


async def main():
    config = Config()
    config.add_argument('--window-size=1920,1080')
    browser = await start(config)

    tab = await browser.get(
        url="https://github.com/ultrafunkamsterdam/undetected-chromedriver",
        new_tab=True
    )

    # Sleep 1 second
    await tab.sleep(1)

    # Take screenshot
    base64_screenshot = await tab.take_screenshot(format="jpeg", full_page=False)

    # Decode image (convert Base64-encoded image to bytes)
    image_bytes = base64.b64decode(base64_screenshot)

    # Upload directly to Google Cloud Storage
    GCS_BUCKET_NAME = "your-bucket-name"
    GCS_DESTINATION = "screenshot/page.jpg"

    upload_to_gcs(GCS_BUCKET_NAME, GCS_DESTINATION, image_bytes)


if __name__ == "__main__":
    loop().run_until_complete(main())
