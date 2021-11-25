import json
import logging
import time

from pkg.command._command import Command
from pkg.executor._executor import Executor
from pkg.executor.process._process import ProcessExecutor


class ShellCommand(Command):
    _retry_count = 3

    def __init__(self, cmd: str):
        self.cmd = cmd

    def execute_command(self, *args):
        return self._command_execute()

    def _command_execute(self):
        is_executed_success = False
        count = 0
        while not is_executed_success:
            try:
                result = self._execute_process()
                logging.info(result)
                is_executed_success = True
            except Exception as e:
                logging.error(e)
                time.sleep(5)
                if count + 1 == self._retry_count:
                    raise e
            count += 1
        return result

    def _execute_process(self):
        process_executor: Executor = ProcessExecutor(self.cmd)
        return process_executor.execute()
