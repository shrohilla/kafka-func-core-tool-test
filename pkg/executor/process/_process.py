import logging
import subprocess

from pkg.executor._executor import Executor


class ProcessExecutor(Executor):

    def __init__(self, object: str):
        self._process_cmd = object

    def execute(self):
        process_cmd = self._process_cmd
        logging.info("command -> {}".format(process_cmd))
        output = subprocess.check_output(process_cmd, timeout=100000, shell=True)
        result = output.decode('UTF-8', errors='strict')
        return result