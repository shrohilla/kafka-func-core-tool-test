from pkg.command._http_cmd import HttpCommand
from pkg.executor._executor import Executor


class HttpCommandExecutor(Executor):

    def __init__(self, cmd: HttpCommand):
        self.http_command = cmd

    def execute(self):
        return self.http_command.execute_command()
