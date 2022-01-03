from re import match
from typing import Any, Dict
from spring_config.client import SpringConfigClient
from spring_config import ClientConfigurationBuilder, ClientConfiguration
from .__interface import ISettings


class SpringConfig(ISettings):
    # pylint: disable=too-many-arguments
    def __init__(self,
                 endpoint: str,
                 app_name: str,
                 profile: str = 'default',
                 user: str = '',
                 pwd: str = '') -> None:
        super().__init__()

        if match(r"^[a-zA-Z]+://[0-9\.a-zA-Z_-]+:\d+$", endpoint) is not None:
            pass  # Address is ok
        elif match(r"^[a-zA-Z]+://[0-9\.a-zA-Z_-]+$", endpoint) is not None:
            endpoint += ":8888"
        elif match(r"^[0-9\.a-zA-Z_-]+:\d+$", endpoint) is not None:
            endpoint = "http://" + endpoint
        else:
            endpoint = f"http://{endpoint}:8888"

        _conf: ClientConfigurationBuilder = ClientConfigurationBuilder()
        _conf.app_name(app_name)
        if len(user) > 0 and len(pwd) > 0:
            _conf.authentication((user, pwd))   # pragma: no cover
        _conf.address(endpoint)
        _conf.profile(profile)
        _cconf: ClientConfiguration = _conf.build()

        _spring_client: SpringConfigClient = SpringConfigClient(_cconf)
        _d: Dict[str, Any] = _spring_client.get_config()
        self._config(_d, raise_on_missing=True, read_only=True)
    # pylint: enable=too-many-arguments

    def _update(self, key: str, val: str) -> None:
        pass  # pragma: no cover
