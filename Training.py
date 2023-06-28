from Agent import Agent
from utility import load_training_data


def initAgents(amounts, actions_amount):
    agents = []
    for i in range(amounts):
        agents.append(Agent(actions_amount))
    return agents


class GeneticAlgorythm:

    def __init__(self):
        # load and split the data
        data = load_training_data()
        self.train = data.head(int(len(data) * 0.8))
        self.validation = data.iloc[max(self.train.index):]
        self.actions_amount = 2
        self.epoch = 100
        self.num_weight = 10
        self.mutation_prob = 0.05
        self.allele_prob = 0.1
        self.cross_prob = 0.4
        self.starting_amt = 10_000
        self.agents: list[Agent] = initAgents(100, self.actions_amount)

    def save(self):
        pass

    def tournament_selection(self):
        pass

    def mutation(self):
        self.mutationMethode()
        self.mutationWeigth()
        pass

    def crossover(self):
        pass

    def fitness(self):
        pass

    def mutationMethode(self):
        pass

    def mutationWeigth(self):
        pass

    def logic(self):
        self.fitness()
        for i in range(self.epoch):
            self.printbest()
            self.tournament_selection()
            self.crossover()
            self.mutation()
        self.printbest()

    def printbest(self):
        best_agent = self.agents[0]
        for agent in self.agents:
            if agent.get_score() > best_agent.get_score():
                best_agent = agent
        print("Best agent has {}$ profit".format(best_agent.get_score()))
