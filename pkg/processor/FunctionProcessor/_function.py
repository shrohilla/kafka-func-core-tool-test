from pkg._exception import ValidationFailedException
from pkg.enums.Platform._platform import OSPlatform
from pkg.enums.language._language import Language
from pkg.processor._processor import Processor
from pkg.processor.language._language import LanguageProcessor


class FunctionPlatformProcessor(Processor):

    def __init__(self, path, os_platform: OSPlatform):
        self._path = path
        self._os_platform = os_platform

    def validate(self):
        return True

    def pre_process(self):
        if not self.validate():
            raise ValidationFailedException("validation failed")
        pass

    def execute_process(self):
        for lang in Language:
            if Language.PYTHON == lang and OSPlatform.WINDOW == self._os_platform:
                continue
            processor: Processor = LanguageProcessor(self._path, self._os_platform, lang)
            processor.process()
