import configparser


class ConfigManager:
    CONFIG_FILE_NAME = 'config.ini'
    def __init__(self):
        self.config_path = None
        self.weights_path = None
        self.devices = None
        self.converter_version = None
        self.labelme_version = None

    def load_config(self):
        config = configparser.ConfigParser()
        config.read('./dcvt/config.ini', encoding='utf-8')

        self.converter_version = config['converter']['version']
        self.labelme_version = config['labelme']['version']

    def save_config(self, section, option, value):
        config = configparser.ConfigParser()
        config.read(self.CONFIG_FILE_NAME, encoding='utf-8')
        config.set(section, option, value)
        with open(self.CONFIG_FILE_NAME, 'w') as f:
            config.write(f)
