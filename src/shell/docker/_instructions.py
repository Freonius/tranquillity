from typing import Union


class DockerInstruction:
    @staticmethod
    def FROM(image: str, tag: str = 'latest', as_name: Union[str, None] = None):
        pass
