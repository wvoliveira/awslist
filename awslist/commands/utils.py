import configparser

def config_parser(file, section):
    config = configparser.ConfigParser()
    config.read(file)
    if config.has_section(section):
        items_dict = dict(config.items(section))
        return items_dict
    else:
        print("File {0} or section {1} doesnt't exists".format(file, section))
        exit(1)
