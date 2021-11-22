from pkg.creator._creator import Creator
from pkg.creator.app_plan._app_plan import FunctionPlanCreator
from pkg.creator.az_resources._az_resources import AzureResourceCreator
from pkg.creator.function_app._function_app import FunctionAppCreator
from pkg.creator.local_function._local_function import LocalFunctionAppCreator
from pkg.creator.storageacnt._storage_account import StorageAccountCreator
from pkg.creator.type._creator_type import CreatorType
from pkg.factory._absfactory import KafkaExtTestAbsFactory
from pkg.enums.language._language import Language


class CreatorFactory(KafkaExtTestAbsFactory):
    instance_map = {}

    def retrieve_instance(self, *args):
        creator_type, lang_creator_type = self.validate_extract_val(args)

        if self.instance_map[lang_creator_type] is not None:
            return self.instance_map[lang_creator_type]
        if self.instance_map[creator_type] is not None:
            return self.instance_map[creator_type]
        raise ("creator type is not found")

    def validate_extract_val(self, args):
        lang_creator_type: Language = None
        creator_type: CreatorType = None
        try:
            lang_creator_type = args[0]
        except IndexError:
            pass
        try:
            creator_type = args[1]
        except IndexError:
            pass
        return creator_type, lang_creator_type

    def build_factory(self, path: str):
        self.build_factory_creator_type()
        self.create_factory_language(path)

    def create_factory_language(self, path):
        pass
        # for creator_type in Language:
        #     creator: Creator = None
        #     if creator_type == Language.PYTHON:
        #         creator = PythonFunctionCreator(path, creator_type)
        #     else:
        #         break
        #     self.instance_map[creator_type] = creator

    def build_factory_creator_type(self):
        for creator_type in CreatorType:
            creator: Creator = None
            if creator_type == CreatorType.STORAGE_ACCOUNT:
                creator = StorageAccountCreator()
            elif creator_type == CreatorType.FUNCTION_APP_PLAN:
                creator = FunctionPlanCreator()
            elif creator_type == CreatorType.AZURE_RESOURCE:
                creator = AzureResourceCreator()
            elif creator_type == CreatorType.LOCAL_FUNCTION:
                creator = LocalFunctionAppCreator()
            else:
                creator = FunctionAppCreator()

            self.instance_map[creator_type] = creator

factory_instance = CreatorFactory()

def get_instance():
    return factory_instance