import logging
import time

from pkg.command._command import Command
from pkg.command.shell_cmd import ShellCommand
from pkg.enums.Platform._platform import OSPlatform
from pkg.enums.language._language import Language
from pkg.utils import _name_creator


class FunctionPublisher:
    _function_publish_cmd = "func azure functionapp publish {} --publish-local-settings -y"

    def publish(self, lang: Language, platform: OSPlatform):
        #if Language.TYPESCRIPT == lang:
        #    self._prepare_build(lang, platform)
        func_app_publish_cmd = self._function_publish_cmd
        if not Language.PYTHON == lang:
            func_app_publish_cmd = func_app_publish_cmd+" --force"
        func_app_publish_cmd = func_app_publish_cmd.format(_name_creator.create_function_app(lang, platform))
        logging.debug("func publish command -- {}".format(func_app_publish_cmd))
        shell_cmd: Command = ShellCommand(func_app_publish_cmd)
        time.sleep(12)
        shell_cmd.execute_command()
        logging.info("function app published successfully")
        pass

    def _prepare_build(self, lang, platform):
        cmd = 'func extensions install'
        shell_cmd: Command = ShellCommand(cmd)
        shell_cmd.execute_command()
        cmd = 'npm run build:production'
        shell_cmd: Command = ShellCommand(cmd)
        shell_cmd.execute_command()
        logging.info("npm run for typescript app")
