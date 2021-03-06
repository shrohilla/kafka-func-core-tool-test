import abc


class Command:

    @abc.abstractmethod
    def execute_command(self, *args):
        pass