from dotenv import load_dotenv
load_dotenv()

import os

import urllib.request

import urllib.parse as urlparse
import hashlib
import hmac
import base64

import json

KEY: str = os.environ.get("KEY") # type: ignore
SECRET: str = os.environ.get("SECRET") # type: ignore

def main():
    lat = 47.655878
    long = -122.3100851

    url = f"https://maps.googleapis.com/maps/api/streetview/metadata?location={lat},{long}&key={KEY}"
    signed_url = sign_url(url, SECRET)

    # https://developers.google.com/maps/documentation/streetview/metadata#examples
    json_res = urllib.request.urlopen(signed_url)
    meta_data = json.loads(json_res.read())

    if meta_data["status"] == "OK":
        # https://developers.google.com/maps/documentation/streetview/request-streetview
        url = f"https://maps.googleapis.com/maps/api/streetview?size=600x300&location={lat},{long}&key={KEY}"
        signed_url = sign_url(url, SECRET)
        urllib.request.urlretrieve(signed_url, "./images/test.jpg")


def sign_url(input_url: str, secret: str) -> str:
    # https://developers.google.com/maps/documentation/maps-static/digital-signature
    url = urlparse.urlparse(input_url)
    url_to_sign = url.path + "?" + url.query

    decoded_key = base64.urlsafe_b64decode(secret)

    signature = hmac.new(decoded_key, str.encode(url_to_sign), hashlib.sha1)

    encoded_signature = base64.urlsafe_b64encode(signature.digest())

    original_url = url.scheme + "://" + url.netloc + url.path + "?" + url.query

    return original_url + "&signature=" + encoded_signature.decode()


if __name__ == '__main__':
    main()