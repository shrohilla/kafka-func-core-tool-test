import json
import logging

from pkg.entity.InputData import InputData

class IntiateApp:

    def initiate(json_file_path):
        logging.basicConfig(
            format='%(asctime)s\t%(levelname)s\t%(message)s',
            level=logging.DEBUG,
            datefmt='%Y-%m-%dT%H:%M:%S')
        config = None
        with open(json_file_path, 'r') as f:
            data = f.read()
            config = json.loads(data)
        return InputData(function_path=config['function_path'])