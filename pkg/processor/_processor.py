from abc import abstractmethod

from pkg._exception import ValidationFailedException


class Processor:

        @abstractmethod
        def validate(self):
            self.cleanup()
            pass

        @abstractmethod
        def pre_process(self):
            if not self.validate():
                raise ValidationFailedException("validation failed")
            pass

        def process(self):
            self.pre_process()
            self.execute_process()
            self.post_process()

        def post_process(self):
            pass

        @abstractmethod
        def execute_process(self, *args):
            pass

        def cleanup(self):
            pass