import logging
import time

from pkg.command._command import Command
from pkg.command.shell_cmd import ShellCommand
from pkg.enums.Platform._platform import OSPlatform
from pkg.enums.language._language import Language
from pkg.executor._executor import Executor
from pkg.executor.shell.command._shell_cmd_executor import ShellCommandExecutor
from pkg.publisher._publisher import Publisher
from pkg.utils import _name_creator


class FunctionAppPublisher(Publisher):
    _function_publish_cmd = "func azure functionapp publish {} "

    def publish(self, lang: Language, platform: OSPlatform):
        if Language.TYPESCRIPT == lang:
            self._prepare_build(lang, platform)
        func_app_publish_cmd = self._function_publish_cmd
        func_app_publish_cmd = func_app_publish_cmd.format(_name_creator.create_function_app(lang, platform))
        logging.info("func publish command -- {}".format(func_app_publish_cmd))
        shell_cmd: Command = ShellCommand(func_app_publish_cmd)
        time.sleep(12)
        shell_cmd.execute_command()
        logging.info("function app published successfully")
        pass

    def _prepare_build(self, lang, platform):
        cmd = 'npm install'
        self._execute_shell_cmd(cmd)
        cmd = 'npm run build:production'
        self._execute_shell_cmd(cmd)
        cmd = 'func extensions install'
        self._execute_shell_cmd(cmd)

    def _execute_shell_cmd(self, cmd):
        shell_cmd: Command = ShellCommand(cmd)
        shell_cmd_exe: Executor = ShellCommandExecutor(shell_cmd)
        shell_cmd_exe.execute()
