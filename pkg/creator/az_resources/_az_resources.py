import logging
import time

from pkg.creator._creator import Creator
from pkg.creator.type._creator_type import CreatorType
from pkg.global_data import _global_data


class AzureResourceCreator(Creator):

    def create(self, *args):
        self.lang = args[0]
        self.platform = args[1]
        self.factory = args[2]
        self._create_azure_resources()

    def _create_azure_resources(self):
        logging.info("started creating the azure resources for lang :: {} and platform :: {}".
                     format(self.lang, self.platform))
        self._create_storage_account()
        self._create_function_app_plan()
        time.sleep(12)
        res = self._create_function_app()
        logging.info("azure resources created successfully for lang :: {} and platform :: {}".
                     format(self.lang, self.platform))
        self._update_function_app_url(res)

    def _create_function_app(self):
        creator: Creator = self.factory.retrieve_instance(CreatorType.FUNCTION_APP)
        return creator.create(self.lang, self.platform)

    def _create_function_app_plan(self):
        creator: Creator = self.factory.retrieve_instance(CreatorType.FUNCTION_APP_PLAN)
        creator.create(self.lang, self.platform)

    def _create_storage_account(self):
        creator: Creator = self.factory.retrieve_instance(CreatorType.STORAGE_ACCOUNT)
        creator.create(self.lang)

    def _update_function_app_url(self, res):
        logging.info("adding into global data")
        _global_data.put('url', res['defaultHostName'])
        logging.info("url added into global data")
