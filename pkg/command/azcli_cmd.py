import json
import logging

from pkg.command._command import Command
from pkg.entity._az_cli import AzCli
from pkg.executor._executor import Executor
from pkg.executor.process._process import ProcessExecutor


class AzCliCommand(Command):
    def __init__(self, object: AzCli):
        if type(object) != AzCli:
            raise TypeError("not azcli object type")
        self._az_cli = object

    def execute_command(self, *args):
        return self._az_cli_command_execute()

    def _az_cli_command_execute(self):
        try:
            result = self._execute_process(self._az_cli)
            logging.info(result)
            if result is not None and result != '':
                result = json.loads(result.strip())
        except Exception as e:
            logging.error(e)
            raise e
        return result

    def _execute_process(self, az_cli):
        process_executor: Executor = ProcessExecutor(self._az_cli.build_az_cli())
        return process_executor.execute()
