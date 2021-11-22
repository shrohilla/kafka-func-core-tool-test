from pkg.command.azcli_cmd import AzCliCommand
from pkg.executor._executor import Executor


class AzCliCommandExecutor(Executor):

    def __init__(self, cmd: AzCliCommand):
        self.az_cli_command = cmd

    def execute(self):
        return self.az_cli_command.execute_command()