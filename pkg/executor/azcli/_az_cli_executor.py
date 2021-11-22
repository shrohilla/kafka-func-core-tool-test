from pkg.command.azcli_cmd import AzCliCommand
from pkg.entity._az_cli import AzCli
from pkg.executor._executor import Executor
from pkg.executor.azcli.command._azcli_cmd_executor import AzCliCommandExecutor


class AzCliExecutor(Executor):

    def __init__(self):
        pass

    def run_az_cli(self, cmd: AzCli):
        az_cli_command = AzCliCommand(cmd)
        az_cli_cmd_executor = AzCliCommandExecutor(az_cli_command)
        return az_cli_cmd_executor.execute()
