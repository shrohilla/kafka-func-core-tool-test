import json
import logging

from pkg.command._command import Command
from pkg.executor._executor import Executor
from pkg.executor.process._process import ProcessExecutor


class ShellCommand(Command):

    def __init__(self, cmd: str):
        self.cmd = cmd

    def execute_command(self, *args):
        return self._command_execute()

    def _command_execute(self):
        try:
            result = self._execute_process()
            logging.info(result)
        except Exception as e:
            logging.error(e)
            raise e
        return result

    def _execute_process(self):
        process_executor: Executor = ProcessExecutor(self.cmd)
        return process_executor.execute()
