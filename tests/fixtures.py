from unittest.mock import MagicMock

import pytest

from launcher import Launcher


@pytest.fixture
def launcher():
    return Launcher(MagicMock())
