from importlib.metadata import PackageNotFoundError
from unittest.mock import patch

from darig.common.utils import darig_version


def test_version_installed():
    """Test version retrieval when package is installed."""
    with patch("darig.common.utils.version") as mock_version:
        mock_version.return_value = "1.2.3"
        assert darig_version() == "1.2.3"
        mock_version.assert_called_once_with("darig")


def test_version_not_installed():
    """Test version retrieval when package is not installed."""
    with patch("darig.common.utils.version") as mock_version:
        mock_version.side_effect = PackageNotFoundError
        assert darig_version() == "Unknown (package not installed)"
        mock_version.assert_called_once_with("darig")
