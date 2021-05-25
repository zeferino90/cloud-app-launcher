from unittest.mock import patch, MagicMock

from frontend_handlers.adapters import ApiFrontendAdapter
from fixtures import apifrontend
from frontend_handlers.settings import SERVER_PORT


def test_api_frontend_adapter_constructor():
    with patch("frontend_handlers.adapters.Flask") as mock_flask:
        with patch("frontend_handlers.adapters.ApiFrontendAdapter._add_endpoint") as mock_add_endpoint:
            apifrontend = ApiFrontendAdapter()
            api = mock_flask(ApiFrontendAdapter.NAME)
            assert api == apifrontend.api
            assert apifrontend._add_endpoint.call_count == 2


def test_add_launch_app_callback(apifrontend):
    callback = MagicMock()
    apifrontend.add_launch_app_callback(callback)
    assert callback == apifrontend.launch_app_cb


def test_call_launch_app(apifrontend):
    callback = MagicMock()
    app_name = MagicMock()
    app_properties = MagicMock()
    apifrontend.launch_app_cb = callback
    apifrontend.call_launch_app_callback(app_name, app_properties)
    apifrontend.launch_app_cb.assert_called_with(app_name, app_properties)


def test_add_get_launch_status_callback(apifrontend):
    apifrontend = ApiFrontendAdapter()
    callback = MagicMock()
    apifrontend.add_get_launch_status_callback(callback)
    assert callback == apifrontend.get_status_cb


def test_call_get_launch_status(apifrontend):
    callback = MagicMock()
    launch_id = MagicMock()
    apifrontend.get_status_cb = callback
    apifrontend.call_get_launch_status_callback(launch_id)
    apifrontend.get_status_cb.assert_called_with(launch_id)


def test_run(apifrontend):
    apifrontend.api = MagicMock()
    apifrontend.run()
    apifrontend.api.run.assert_called_with(port=SERVER_PORT, host="0.0.0.0")


def test_add_endpoint(apifrontend):
    apifrontend.api = MagicMock()
    endpoint = MagicMock()
    endpoint_name = MagicMock()
    handler = MagicMock()
    apifrontend._add_endpoint(endpoint, endpoint_name, handler)
    apifrontend.api.add_url_rule.assert_called_with("api/v1" + endpoint, endpoint_name, handler)


def test_launch_app(apifrontend):
    launch_app_cb = MagicMock()
    apifrontend.launch_app_cb = launch_app_cb
    with patch("frontend_handlers.adapters.request") as mock_request:
        with patch("frontend_handlers.adapters.json") as mock_json:
            with patch("frontend_handlers.adapters.jsonify") as mock_jsonify:
                apifrontend.launch_app()
                mock_request.args.get.assert_called_with("name", None)
                mock_json.loads.assert_called_with(mock_request.data)
                app_name = mock_request.args.get("name", None)
                app_properties = mock_json.loads(mock_request.data)
                apifrontend.launch_app_cb.assert_called_with(app_name, app_properties)
                response = apifrontend.launch_app_cb(app_name, app_properties)
                mock_jsonify.assert_called_with(response)


def test_get_launch_id(apifrontend):
    get_status_cb = MagicMock()
    apifrontend.get_status_cb = get_status_cb
    launch_id = MagicMock()
    with patch("frontend_handlers.adapters.jsonify") as mock_jsonify:
        apifrontend.get_launch_status(launch_id)
        get_status_cb.assert_called_with(launch_id)
        response = apifrontend.get_status_cb(launch_id)
        mock_jsonify.assert_called_with(response)
