import yaml
import sys
from project_store_exception_layer.exception import CustomException as LoadYamlException

class CommonUtils:
    
    def read_yaml(self,path_to_yaml: str) -> dict:
        """This method is used to read yaml file.
        Args: path_to_yaml: path to yaml file.
        Returns: content: type(__dict__) content of yaml file.
        """
        try:
            with open(path_to_yaml) as yaml_file:
                content = yaml.safe_load(yaml_file)
            # print(f"YAML file: {path_to_yaml} loaded successfully")
            return content
        
        except Exception as e:
            load_yaml_exception = LoadYamlException(
                "Failed during loading yaml file in module [{0}] class [{1}] method [{2}]"
                    .format(self.__module__, CommonUtils.__name__,
                            self.read_yaml.__name__))
            raise Exception(load_yaml_exception.error_message_detail(str(e), sys)) from e