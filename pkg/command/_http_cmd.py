import json
import logging

import requests
from requests import Response

from pkg.command._command import Command
from pkg.constant import Constant
from pkg.entity._http import HttpRequest
from pkg.global_data import _global_data


class HttpCommand(Command):

    def __init__(self, httpCmd: HttpRequest):
        self.http_req = httpCmd

    def execute_command(self):
        return self._execute_http_cmd()

    def _execute_http_cmd(self):
        try:
            result: Response = self._execute_process()
            logging.info(result)
            #result = json.loads(result.strip())
        except Exception as e:
            print(e)
            _global_data.get('url')
            raise e
        return result

    def _execute_process(self):
        if Constant.HTTPRequest_POST == self.http_req.method:
            logging.info("invoking post request")
            return requests.post(self.http_req.url, self.http_req.body)
        elif Constant.HTTPRequest_GET == self.http_req.method:
            logging.info("invoking get request")
            return requests.get(self.http_req.url, self.http_req.params)
