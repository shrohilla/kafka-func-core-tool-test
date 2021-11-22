from pkg.command._http_cmd import HttpCommand
from pkg.executor._executor import Executor
from pkg.executor.http.command._http_cmd_executor import HttpCommandExecutor


class HttpExecutor(Executor):

    def execute(self, cmd: HttpCommand):
        http_command = HttpCommand(cmd)
        http_cmd_executor = HttpCommandExecutor(http_command)
        return http_cmd_executor.execute()
