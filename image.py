from dotenv import load_dotenv
load_dotenv()

import os

import urllib.request

import urllib.parse as urlparse
import hashlib
import hmac
import base64

from glob import glob
import csv
import json

KEY: str = os.environ.get("KEY") # type: ignore
SECRET: str = os.environ.get("SECRET") # type: ignore
CWD: str = os.getcwd()

def main():
    files = glob(f"{CWD}/coordinates/*.tsv")
    for file in files:
        with open(file, encoding="utf-8") as f:
            rd = csv.reader(f, delimiter="\t", quotechar='"')
            next(rd, None)
            for row in rd:
                short_name, long_name, x, y = row
                y = float(y)
                x = float(x)
                lat, long = convert(y, x)
    # lat = 47.65305984
    # long = -122.3125352
    # save_images(lat, long)


def convert(y: float, x: float):
    y_factor = -0.000005703250456
    y_intercept = 47.66324934

    x_factor = 0.000009927810411
    x_intercept = -122.3277872

    return (y * y_factor + y_intercept, x * x_factor + x_intercept)


def save_images(lat, long):
    fov = 120

    # https://developers.google.com/maps/documentation/streetview/metadata#examples
    url = f"https://maps.googleapis.com/maps/api/streetview/metadata?location={lat},{long}&fov={fov}&source=outdoor&key={KEY}"
    signed_url = sign_url(url, SECRET)

    json_res = urllib.request.urlopen(signed_url)
    meta_data: dict[str, str] = json.loads(json_res.read())
    pano_id: str = meta_data["pano_id"]
    with open(f"{CWD}/images/{pano_id}.json", "w", encoding="utf-8") as f:
        json.dump(meta_data, f, indent=4)

    headings = [0, 120, 240]
    for heading in headings:
        files = glob(f"{CWD}/images/{pano_id}{heading}.*")
        if len(files) > 0:
            continue

        if meta_data["status"] == "OK":
            # https://developers.google.com/maps/documentation/streetview/request-streetview
            url = f"https://maps.googleapis.com/maps/api/streetview?size=600x600&pano={pano_id}&fov={fov}&heading={heading}&source=outdoor&key={KEY}"
            signed_url = sign_url(url, SECRET)
            urllib.request.urlretrieve(signed_url, f"./images/{pano_id}{heading}.jpg")


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