from unittest.mock import MagicMock

import pytest

from frontend_handlers.adapters import ApiFrontendAdapter
from launcher import Launcher


@pytest.fixture
def launcher():
    return Launcher(MagicMock())

@pytest.fixture
def apifrontend():
    return ApiFrontendAdapter()
