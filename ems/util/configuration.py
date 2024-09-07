import os
import yaml


class Configuration:
    _instance = None

    def __new__(cls, ):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.configuration = {}
            cls._instance.read_config()
        return cls._instance


    def replace_env_variables(self, config_str):
        return os.path.expandvars(config_str)


    def read_config(self):
        file_name = os.environ.get('CONFIG_FILE', "/resources/application.yaml")
        with open(file_name, 'r', encoding="utf-8") as file_obj:
            data = file_obj.read()
        try:
            updated_config_str = self.replace_env_variables(data)
            self.configuration = yaml.safe_load(updated_config_str)
            return self.configuration
        except KeyError as error:
            raise ConfigurationError() from error
        except TypeError as error:
            raise ConfigurationError() from error


class ConfigurationError(Exception):
    pass
