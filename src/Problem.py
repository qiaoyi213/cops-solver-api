from pyqubo import Binary, Constraint, OneHotEncInteger
from dwave.samplers import SimulatedAnnealingSampler
from dwave_networkx.algorithms.independent_set import maximum_weighted_independent_set_qubo,is_independent_set
from dwave_networkx.algorithms.tsp import traveling_salesperson_qubo, is_hamiltonian_path
from dwave_networkx.algorithms.coloring import vertex_color_qubo, is_vertex_coloring
from dwave_networkx.algorithms.max_cut import weighted_maximum_cut
import numpy as np
import dimod
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
        
        h = {v: 0. for v in self.G}
        J = {(u, v): self.G[u][v]['weight'] for u, v in self.G.edges}

        qubo = dimod.ising_to_qubo(h,J)[0]

        return qubo

    def solve_SA(self):
        Q = self.get_qubo()
        sampler = SimulatedAnnealingSampler()
        sampleset = sampler.sample_qubo(Q, num_reads=1000)

        best_sample = sampleset.first.sample

        return {k: int(v) for k,v in best_sample.items()}


class VertexCoverProblem:
    def __init__(self, graph):
        self.G = nx.Graph()
        self.G.add_edges_from(graph)
    
    def get_qubo(self):
        
        return maximum_weighted_independent_set_qubo(self.G)
    
    def solve_SA(self):
        Q = self.get_qubo()
        sampler = SimulatedAnnealingSampler()

        sampleset = sampler.sample_qubo(Q, num_reads=1000)

        best_sample = sampleset.first.sample

        return {k: int(v) for k,v in best_sample.items()}



class KnapsackProblem: #01 Knapsack
    def __init__(self, weights, values, capacity):
        self.weights = weights
        self.values = values
        self.capacity = capacity
    
    def get_qubo(self):
        n = len(self.weights)
        x = [Binary(f"x_{i}") for i in range(n)]
        # define the sum of weights and values using variables
        knapsack_weight = sum(self.weights[i] * x[i] for i in range(n))
        knapsack_value = sum(self.values[i] * x[i] for i in range(n))
        
        weight_one_hot = OneHotEncInteger("weight_one_hot",value_range=(1, self.capacity), strength=100) # sigma(n*yn) #strength  of constraints
        Ha = Constraint((weight_one_hot - knapsack_weight)**2,"weight_constraint")
        Hb = knapsack_value
        H = Ha - Hb
        model = H.compile()
        qubo, offset = model.to_qubo()

        return qubo
    
    def solve_SA(self):
        Q = self.get_qubo()
        sampler = SimulatedAnnealingSampler()
        sampleset = sampler.sample_qubo(Q, num_reads=1000)

        best_sample = sampleset.first.sample

        return {k: int(v) for k,v in best_sample.items()}
    

class GraphColoringProblem:
    def __init__(self, graph, colors):
        self.colors = colors
        self.G = nx.Graph()
        self.G.add_edges_from(graph)
        

    def get_qubo(self):
        qubo = vertex_color_qubo(self.G, colors=self.colors)
        
        return qubo
    def parse_answer(self, sample):
        coloring = {}
        for key, value in sample.items():
            if value == 1:
                (node, color) = key
                coloring[int(node)] = int(color)

        return coloring

    def solve_SA(self):
        Q = self.get_qubo()
        sampler = SimulatedAnnealingSampler()
        sampleset = sampler.sample_qubo(Q, num_reads=1000)

        best_sample = sampleset.first.sample
        return self.parse_answer(best_sample)
    
        
class HamiltonianCycleProblem:
    def __init__(self, graph):
        self.G = nx.Graph()
        self.G.add_edges_from(graph)
    def not_in_edge(self, n, Edge): #用來幫忙編輯 H3
        set_edge = set()
        #count=0
        count_else=0
        for i in range( n ):
            for k in range( n ):
                if ( i, k ) in Edge or ( k, i ) in Edge:
                    #count+=1
                    #print("edge:",k,(i,k))
                    continue
                else:
                    count_else+=1
                    set_edge.add( ( i, k ) )
                    #print("edge_else:",k,(i,k))
        #print("count=",count)
        print("不在圖中的邊數=",count_else)
        return set_edge
    
    def get_qubo(self):
        n = len(self.G.nodes)
        print(n)
        variable_list=[]
        tmp_list=[]
        H1 = 0
        for i in range(n):
            tmp = 0
            for j in range(n):
                x = Binary("x_{}_{}".format(i,j))
                tmp_list.append(x)
                #print(x)
                tmp += x
            variable_list.append(tmp_list)
            tmp_list=[]
            #print("ouo")
            H1 += (1-tmp)**2
        H2 = 0
        for j in range(n):
            tmp = 0
            for i in range(n):
                tmp += variable_list[i][j]
            H2 += (1-tmp)**2

        H3 = 0
        for ( u, v ) in self.not_in_edge(n, self.G.edges() ):
            #print("NOT an edge in graph:",(u,v))
            for j in range(n): #0~j-1    range(n)會從0~n-1
                if (j < n-1):
                    H3 += variable_list[u][j]*variable_list[v][j+1]
                else: # j = n  j~0(最後一個到第一個)
                    H3 += variable_list[u][-1]*variable_list[v][0]

        a=1
        b=1
        c=1
        H = a*H1 + b*H2 + c*H3
        model = H.compile()
        qubo, offset = model.to_qubo()
        QVar = model.variables
        return qubo
    def parse_answer(self, sample):
        cycle = []
        for key, value in sample.items():
            if value == 1:
                (node, pos) = key.split("_")[1], key.split("_")[2]
                cycle.append(int(node))

        return cycle
        
    def solve_SA(self):
        
        Q = self.get_qubo()
        sampler = SimulatedAnnealingSampler()
        sampleset = sampler.sample_qubo(Q, num_reads=1000)

        best_sample = sampleset.first.sample
        
        return {"cycle": self.parse_answer(best_sample)}


class TravellingSalespersonProblem:
    def __init__(self, graph):
        self.G = nx.Graph()
        self.G.add_weighted_edges_from(graph)

    def get_qubo(self):
        return traveling_salesperson_qubo(self.G)
    def fitness_function(self, x, matrix):
        f_x = 0
        for i in range(len(x)-1):
            f_x += matrix[x[i],x[i+1]]
        return f_x+matrix[x[-1],x[0]]

    def parse_answer(self, sample):
        route = [None]*len(self.G)
        for (city, times), val in sample.items():
            if val:
                route[times] = city
        print(route)
        
        print(self.fitness_function(route, nx.to_numpy_array(self.G)))
        return route
    
    def solve_SA(self):
        Q = self.get_qubo()
        sampler = SimulatedAnnealingSampler()
        sampleset = sampler.sample_qubo(Q, num_reads=1000)

        best_sample = sampleset.first.sample
        return {"route": self.parse_answer(best_sample)}
        

class JobShopSchedulingProblem:

    pass
    