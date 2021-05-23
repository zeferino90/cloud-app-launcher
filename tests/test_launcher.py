from unittest.mock import MagicMock, patch, ANY

import pytest

from launcher import Launcher
from fixtures import launcher


def test_launcher_constructor_succeed():
    cloud_adapter = MagicMock()
    launcher = Launcher(cloud_adapter)
    assert isinstance(launcher, Launcher)
    assert launcher.cloud_adapter == cloud_adapter


def test_launch_app__run_ok(launcher):
    app_name = MagicMock()
    launch_id = MagicMock()
    launcher.cloud_adapter.launch_app.return_value = launch_id
    with patch("launcher.App") as mock_app:
        assert {"launch_id": launch_id} == launcher.launch_app(app_name, {"app_property": ANY})
        mock_app.assert_called_with(app_name, {"app_property": ANY})
        mock_app_instance = mock_app(app_name, {"app_property": ANY})
        launcher.cloud_adapter.launch_app.assert_called_with(mock_app_instance)


def test_launch_app__launch_exception(launcher):
    app_name = MagicMock()
    launcher.cloud_adapter.launch_app.side_effect = Exception
    with patch("launcher.App") as mock_app:
        mock_app_instance = mock_app(app_name, {"app_property": ANY})
        response = {'error_msg': f"Exception while launching the app {mock_app_instance.name}"}
        assert response == launcher.launch_app(app_name, {"app_property": ANY})
        mock_app.assert_called_with(app_name, {"app_property": ANY})
        launcher.cloud_adapter.launch_app.assert_called_with(mock_app_instance)


def test_check_app_launch__return_status(launcher):
    launch_id = MagicMock()
    launcher.cloud_adapter.get_launch_status.return_value = {}
    assert isinstance(launcher.check_app_launch(launch_id), dict)


def test_check_app_launch__exception(launcher):
    launch_id = MagicMock()
    launcher.cloud_adapter.get_launch_status.side_effect = Exception
    response = {'error_msg': f"Exception getting launch status for {launch_id}"}
    assert response == launcher.check_app_launch(launch_id)
