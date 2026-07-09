import os
import time
from dotenv import load_dotenv

from ctrader_open_api import Client, TcpProtocol, EndPoints
from ctrader_open_api.messages.OpenApiMessages_pb2 import ProtoOAApplicationAuthReq
from ctrader_open_api.messages.OpenApiMessages_pb2 import ProtoOAAccountAuthReq

load_dotenv()


CLIENT_ID = os.getenv("CTRADER_CLIENT_ID")
CLIENT_SECRET = os.getenv("CTRADER_SECRET")
ACCESS_TOKEN = os.getenv("CTRADER_ACCESS_TOKEN")
ACCOUNT_ID = int(os.getenv("CTRADER_ACCOUNT_ID"))


def on_connected(client):
    print("✅ Connected to cTrader Open API")

    request = ProtoOAApplicationAuthReq()
    request.clientId = CLIENT_ID
    request.clientSecret = CLIENT_SECRET

    client.send(request)


def on_message(client, message):
    print("MESSAGE:")
    print(message)


def on_error(client, error):
    print("ERROR:")
    print(error)


client = Client(
    EndPoints.PROTOBUF_DEMO_HOST,
    EndPoints.PROTOBUF_PORT,
    TcpProtocol
)


client.setConnectedCallback(on_connected)
client.setMessageReceivedCallback(on_message)
client.setErrorCallback(on_error)


print("Connecting...")

client.startService()

while True:
    time.sleep(1)
