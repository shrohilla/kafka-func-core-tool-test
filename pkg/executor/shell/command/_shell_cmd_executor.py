from pkg.command.shell_cmd import ShellCommand
from pkg.executor._executor import Executor


class ShellCommandExecutor(Executor):

    def __init__(self, cmd: ShellCommand):
        self.shell_cli_command = cmd

    def execute(self):
        return self.shell_cli_command.execute_command()
