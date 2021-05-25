from flask import Flask, jsonify, request, json

from frontend_handlers.port import FrontendPort
from frontend_handlers.settings import SERVER_PORT


class ApiFrontendAdapter(FrontendPort):
    NAME = "Launcher API"

    def __init__(self):
        self.api = Flask(self.NAME)
        self.launch_app_cb = None
        self.get_status_cb = None
        self._add_endpoint(endpoint='new-launch', endpoint_name='new-launch', handler=self.launch_app)
        self._add_endpoint(endpoint='launch-state/<launch_id>', endpoint_name='launch-state',
                           handler=self.get_launch_status)

    def add_launch_app_callback(self, callback):
        self.launch_app_cb = callback

    def call_launch_app_callback(self, app_name, app_properties):
        return self.launch_app_cb(app_name, app_properties)

    def add_get_launch_status_callback(self, callback):
        self.get_status_cb = callback

    def call_get_launch_status_callback(self, launch_id):
        return self.get_status_cb(launch_id)

    def run(self):
        self.api.run(port=SERVER_PORT, host="0.0.0.0")

    def _add_endpoint(self, endpoint=None, endpoint_name=None, handler=None):
        self.api.add_url_rule("/api/v1/" + endpoint, endpoint_name, handler)

    def launch_app(self):
        app_name = request.args.get("name", None)
        app_properties = json.loads(request.data)
        response = self.launch_app_cb(app_name, app_properties)
        return jsonify(response)

    def get_launch_status(self, launch_id):
        response = self.get_status_cb(launch_id)
        return jsonify(response)
