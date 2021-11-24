import logging
import os.path

from pkg.command._command import Command
from pkg.command.shell_cmd import ShellCommand
from pkg.creator._creator import Creator
from pkg.enums.Platform._platform import OSPlatform
from pkg.enums.language._language import Language


class LocalFunctionAppCreator(Creator):
    _func_app_name: str = "funcapp"
    _func_app_creation_cmd: str = "func init test"
    _func_app_trigger: str = 'func new --name KafkaExample --template "Kafka trigger"'
    _func_app_out_binding: str = 'func new --name Kafkaoutput --template "Kafka output"'

    def create(self, *args):
        self._folder_path = args[0]
        self._lang = args[1]
        self._platform: OSPlatform = args[2]
        return self._local_func_app()

    def _local_func_app(self):
        os.chdir(self._folder_path)
        os_platform_name = self._platform.name.lower()[0:2]
        self._build_func_app(os_platform_name)
        os.chdir("test-" + self._lang.name+'-'+os_platform_name)
        self._build_io_triggers()

    def _build_func_app(self, os_platform_name: str):
        lang_str: str = self._lang.name.lower()
        logging.info("building function app for lang :: "+lang_str)
        func_app_creation_cmd = self._func_app_creation_cmd + "-" + lang_str +'-' + os_platform_name + " --" + lang_str
        shell_cmd: Command = ShellCommand(func_app_creation_cmd)
        shell_cmd.execute_command()
        logging.info("function app created successfully")

    def _build_io_triggers(self):
        lang_name = self._lang.name.lower()
        logging.info("building the trigger for language :: "+lang_name)
        app_trigger_cmd = self._func_app_trigger
        #TODO
        if Language.POWERSHELL == self._lang:
            app_trigger_cmd = app_trigger_cmd+" --language "+lang_name
        shell_cmd: Command = ShellCommand(app_trigger_cmd)
        shell_cmd.execute_command()
        logging.info("trigger built successfully")
        app_trigger_cmd = self._func_app_out_binding
        #TODO
        if Language.POWERSHELL == self._lang:
            app_trigger_cmd = app_trigger_cmd+" --language "+lang_name
        shell_cmd: Command = ShellCommand(app_trigger_cmd)
        shell_cmd.execute_command()
        logging.info("output binding built successfully")
