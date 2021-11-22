# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import sys

from pkg._exception import FilePathNotFoundInArgs
from pkg.entity.InputData import InputData
from pkg.initiator._initiator import IntiateApp
from pkg.orchestrator._orchestrator import TestOrchestrator


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    file_path = None
    try:
        file_path = sys.argv[1]
    except IndexError:
        raise FilePathNotFoundInArgs('Config file path is not given in command line arguments.')
    initiator: IntiateApp = IntiateApp
    input_data: InputData = initiator.initiate(file_path)
    testOrchestrator: TestOrchestrator = TestOrchestrator()
    testOrchestrator.orchestrate(input_data.function_path)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
