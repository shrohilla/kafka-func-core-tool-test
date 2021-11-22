from pkg.creator._creator import Creator
from pkg.enums.Platform._platform import OSPlatform
from pkg.factory.creator import _creator
from pkg.factory.creator._creator import CreatorFactory
from pkg.enums.language._language import Language
from pkg.processor.FunctionProcessor._function import FunctionProcessor
from pkg.processor._processor import Processor


class TestOrchestrator:
    def __init__(self):
        pass

    def orchestrate(self, path: str):
        creatorFac: CreatorFactory = _creator.get_instance()
        creatorFac.build_factory(path)

        for os_platform in OSPlatform:
            lang_processor: Processor = FunctionProcessor(path, os_platform)
            lang_processor.process()
