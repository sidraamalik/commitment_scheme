import os
import configparser
import pkg_resources


class ConfigLoader(object):
    def __init__(self, config_dir=None, filename=None):
        if config_dir is not None:
            self.config_dir = config_dir
        else:
            self.config_dir = "commitmentscheme.api.config"

        self.filename = filename
        self.config = self._load()

    def _load(self):
        path = self._get_path()
        config = configparser.ConfigParser()
        # Preserve case of property names
        config.optionxform = str

        try:
            with open(path, "r") as fp:
                config.readfp(fp)
        except IOError:
            raise Exception(
                "Failed to load config: {0}".format(self.filename))

        return config

    def get(self, section):
        return dict(self.config.items(section))

    def _get_path(self):
        return pkg_resources.resource_filename(
            self.config_dir, self.filename)
