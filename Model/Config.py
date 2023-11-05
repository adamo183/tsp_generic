from configparser import ConfigParser


class Config:
    def __init__(self):
        self.data_path = ''
        self.population_size = 0
        self.selection_number_k = 0
        self.crossing_rate = 0.0
        self.mutation_rate = 0.0
        self.inversion_rate = 0.0
        self.iteration = 1


def read_config_file():
    config = ConfigParser()
    config.read('config.ini')
    conf = Config()
    conf.data_path = config.get('main', 'DATA_PATH')
    conf.population_size = config.getint('main', 'POPULATION_SIZE')
    conf.selection_number_k = config.getint('main', 'SELECTION_NUMBER_K')
    conf.crossing_rate = config.getfloat('main', 'CROSSING_RATE')
    conf.mutation_rate = config.getfloat('main', 'MUTATION_RATE')
    conf.inversion_rate = config.getfloat('main', 'INVERSION_RATE')
    conf.iteration = config.getint('main', 'ITERATION')
    return conf