import os

from yaml import load, YAMLError
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

from employees_activity.exceptions import ConfigFileNotFound, ConfigFileError, ConfigFileMissingAttribute


class SettingsLoader(object):
    """
    Settings loader from configs/config.yaml file
    """

    def __init__(self):
        file_path = os.path.abspath(os.path.dirname(__file__))
        config_path = os.path.join(file_path, "../configs/config.yaml")

        try:
            with open(config_path, 'r') as stream:
                try:
                    self.settings = load(stream, Loader=Loader)
                except YAMLError as exc:
                    raise ConfigFileError("configs/config.yaml error: {}".format(exc))
        except IOError:
            raise ConfigFileNotFound("configs/config.yaml file not found")

    @property
    def hubstaff_api_url(self):
        return 'https://api.hubstaff.com/v1'

    @property
    def hubstaff_app_token(self):
        app_token = self.settings.get('HUBSTAFF_APP_TOKEN', '')

        if not app_token:
            raise ConfigFileMissingAttribute("'HUBSTAFF_APP_TOKEN' is missing in configs/config.yaml")

        return app_token

    @property
    def file_path(self):
        return self.settings.get('FILE_PATH', '/tmp')

    @property
    def file_name(self):
        return self.settings.get('FILE_NAME', 'employees_activity_{date}')


settings_loader = SettingsLoader()