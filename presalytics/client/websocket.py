import presalytics
import logging
import sys
import json
import requests
import signalrcore.hub_connection_builder


class EventsWebsocket(object):
    api_client: presalytics.Client

    def __init__(self, *args, **kwargs):
        self.server_url = presalytics.settings.HOST_EVENTS + "/hub"
        self.api_client = presalytics.client.api.Client()
        self.handler = logging.StreamHandler()
        self.handler.setLevel(presalytics.settings.DEBUG)
        self.forward_address = kwargs.get("forward_address", None)
        self.hub_connection = signalrcore.hub_connection_builder.HubConnectionBuilder()\
            .with_url(
                self.server_url,
                options={
                    "verify_ssl": False,
                    "access_token_factory": self.api_client.get_access_token
                }
            ).configure_logging(
                logging.DEBUG,
                socket_trace=True,
                handler=self.handler
            ).with_automatic_reconnect({
                "type": "interval",
                "keep_alive_interval": 10,
                "intervals": [1, 3, 5, 6, 7, 87, 3]
            }).build()

        self.hub_connection.on_open(self.on_connection_open)
        self.hub_connection.on("HandleEvent", self.handle_event)
        self.hub_connection.on_close(lambda: print("Connection closed."))
        self.hub_connection.on_error(lambda data: print(f"An exception was thrown closed {data.error}"))

    def listen(self):
        self.hub_connection.start()
        input("Ready to send and receive Presaltyics events.")

    def on_connection_open(self):
        print("Websocket to Events API opened.")

    def handle_event(self, data):
        for entry in data:
            event_dict = json.loads(entry)
            event_dict.pop("$id")  # this id is assigned by signalR -- not useful downstream.
            print(event_dict)
            if self.forward_address:
                requests.post(self.forward_address, data=event_dict)

    def close(self):
        self.hub_connection.stop()
        sys.exit(0)
