from ..src.api._api import Api
from .entities import President

api = Api()
api.add_entity(President)

if __name__ == '__main__':
    api.start()
    while True:
        try:
            continue
        except Exception:
            api.stop()
