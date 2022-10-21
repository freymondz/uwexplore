# uwexplore

Prototyping repo for UW Explore

## Getting Started

To run `server.py` and `client.py` install the following dependencies:

```shell
pip install -r requirements.txt
```

To run `server.py` use the following command:

```shell
uvicorn server:app --reload
```

To run `client.py` ensure that you have a `.env` file in the root directory with the following variables:

```env
KEY=https://developers.google.com/maps/documentation/streetview/request-streetview
SECRET=https://developers.google.com/maps/documentation/maps-static/digital-signature
```
