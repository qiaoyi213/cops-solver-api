from pyqubo import Binary
from dwave.samplers import SimulatedAnnealingSampler
import networkx as nx
class SubsetSumProblem:
    def __init__(self, S, target):
        self.S = S
        self.target = target

    
    def get_qubo(self):
        H = 0
        
        x = [Binary(f"x{i}") for i in range(len(self.S))]
        
        for i in range(len(self.S)):
            H += self.S[i] * x[i]
        H = (H-self.target)**2
        model = H.compile()
        qubo, offset = model.to_qubo()
        
        return qubo
    def check_answer(self, answer):
        total = 0
        for k,v in answer.items():
            if v == 1:
                total += self.S[k]
        return total == self.target
    
    def solve_SA(self):
        Q = self.get_qubo()
        sampler = SimulatedAnnealingSampler()
        sampleset = sampler.sample_qubo(Q, num_reads=1000)
        
        best_sample = sampleset.first.sample

        return {k: int(v) for k,v in best_sample.items()}


class MaximumCutProblem:

    def __init__(self, graph):
        self.G = nx.Graph()
        self.G.add_weighted_edges_from(graph)


    def get_qubo(self):
        Q = 0
        x = [Binary(f'x{i}')for i in range(len(self.G.nodes()))]
        for i, j in self.G.edges:
            Q += x[i-1] + x[j-1] - 2 * x[i-1] * x[j-1]
    
        model = Q.compile()
        qubo, offset = model.to_qubo()

        return qubo

    def solve_SA(self):
        Q = self.get_qubo()
        sampler = SimulatedAnnealingSampler()
        sampleset = sampler.sample_qubo(Q, num_reads=1000)

        best_sample = sampleset.first.sample

        return {k: int(v) for k,v in best_sample.items()}


class VertexCoverProblem:
    
    pass


class KnapsackProblem: #01 Knapsack
    pass

class GraphColoringProblem:
    pass

class HamiltonianCycleProblem:
    pass


class TravellingSalespersonProblem:
    pass

class JobShopSchedulingProblem:
    pass
    