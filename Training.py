from utility import load_training_data


class GeneticAlgorythm:

    def __init__(self):
        # load and split the data
        data = load_training_data()
        self.train = data.head(int(len(data) * 0.8))
        self.validation = data.iloc[max(self.train.index):]
        

    def save(self):
        pass

    def tournament_selection(self):
        pass

    def mutation(self):
        pass

    def crossover(self):
        pass

    def fitness(self):
        pass
