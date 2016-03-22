from configobj import ConfigObj
import os


def get_config(path=None):
    if path is None:
        path = os.path.expanduser('~/.benzo')

    config = ConfigObj(path)

    if 'benzo' not in config:
        config['benzo'] = {}
        config.write()

    return config
