import numpy as np
from objects import Pulley, Block, String
class Solver:
    def __init__(self, **kwargs):
        self.graph = dict()
        self.reverse_graph = dict()
        self.id_object = dict()
        self.pulley_list = []
        self.block_list = []
        self.string_list = []
        self.idx_alloc = 0
        print('Graph Initialized...')

    def add_object(self, otype=None, **kwargs):
        '''
            Parameters:
            otype: Valid values : 'P', 'B', 'S' for pulley, block or string respectively
            movable: If otype = 'P', movable should be True if the Pulley isn't fixed, by default the value is False
            wt_component: If otype = 'B', the weight component opposite to the direction of string Tension
            mass: If otype = 'B', mass of the block 
            return_obj: True, to return the string unique id & object. By default the value is False, i.e. only string unique id is returned

            Returns:
            Object Id: string unique id given to each object
                       object is returned depending on the value of return_obj
        '''
        if otype not in ['P','B','S']:
            raise Exception("otype must be 'P', 'B' or 'S' in add_object method call")

        ret_obj = None
        ret_id  = None
        if otype == 'P':
            p_id = otype + str(len(self.pulley_list)+1)
            movable = False
            if 'movable' in kwargs.keys():
                movable = kwargs['movable']
            ret_id = p_id
            P_temp = Pulley(id=p_id, idx_pos=self.idx_alloc, movable=movable)
            ret_obj = P_temp
            self.id_object[p_id] = P_temp
            self.idx_alloc += 1
            self.pulley_list.append(p_id)

        elif otype == 'B':
            b_id = otype + str(len(self.block_list)+1)
            wt_component = 0
            mass = 0
            if 'wt_component' in kwargs.keys():
                wt_component = kwargs['wt_component']
            if 'mass' in kwargs.keys():
                mass = kwargs['mass']

            ret_id = b_id
            B_temp = Block(id=b_id, idx_pos=self.idx_alloc, wt_component=wt_component, mass=mass)
            ret_obj = B_temp
            self.id_object[b_id] = B_temp
            self.idx_alloc += 1
            self.block_list.append(b_id)

        else:
            s_id = otype + str(len(self.string_list)+1)
            ret_id = s_id
            S_temp = String(id=s_id, idx_pos=self.idx_alloc)
            ret_obj = S_temp
            self.id_object[s_id] = S_temp
            self.idx_alloc += 1
            self.string_list.append(s_id)

        return_val = False
        if 'return_obj' in kwargs.keys():
            return_val = kwargs['return_obj']
        
        if return_val:
            return ret_id, ret_obj
        else:
            return ret_id

    def add_node(self, node_1, node_2):
        #forward graph
        '''
        Parameters:
        node_1,node_2 for a edge from node_1 to node_2
        Also updates the reverse graph
        '''
        if node_1 not in self.graph.keys():
            self.graph[node_1] = []
        
        self.graph[node_1].append(node_2)

        #reverse graph
        if node_2 not in self.reverse_graph.keys():
            self.reverse_graph[node_2] = []

        self.reverse_graph[node_2].append(node_1)

    def add_relation(self, string_id, pulley_on = [], endpoints = [], **kwargs):
        '''
            Parameters:
            string_id: Unique Id of a string
            pulley_on: list of pulleys over which the string is passing, else input a empty list
            endpoints: a list of two elements mentioning the endpoints of the string, 
                       it can be pulley_id, block_id, or "fixed" if connected to fixed walls 
        '''

        for pulley_id in pulley_on:
            if pulley_id[0] != 'P':
                raise Exception('String can only pass over pulleys, pulley_on list must cosists of pulley_id only.')
            self.add_node(string_id, pulley_id)
            self.add_node(pulley_id, string_id)

        for ep in endpoints:
            if ep != 'fixed':
                self.add_node(string_id, ep)

    
    def solve(self):
        '''
            Solves the Pulley system using graph if all the specified node relations are established using add_relation method
            Prints the Acceleration of pulleys, blocks and Tension of strings
            Returns:
            solution: The solution of the solved equations in a numpy array
        '''
        self.lhs = []
        self.rhs = []

        #String Constraints and Acceleration Relations
        for s in self.string_list:
            if s in self.graph.keys():
                expression = np.zeros(self.idx_alloc, dtype = np.float32)
                for obj in self.graph[s]:
                    obj_type = 'endPoint'
                    if obj in self.graph.keys():
                        for obj_nod in self.graph[obj]:
                            if obj_nod == s:
                                obj_type = 'passOver'

                    if obj_type == 'passOver':
                        expression[self.id_object[obj].index_pos] = -2.0
                    elif obj_type == 'endPoint':
                        expression[self.id_object[obj].index_pos] = 1.0
                self.lhs.append(expression)
                self.rhs.append(0)
        

        #Tesion Relations
        for s in self.string_list:
            if s in self.graph.keys():
                for obj in self.graph[s]:
                    if obj in self.graph.keys():
                        if s not in self.graph[obj] and obj[0] == 'P':
                            for s1 in self.graph[obj]:
                                if s1 in self.graph.keys():
                                    if obj in self.graph[s1]:
                                        expression = np.zeros(self.idx_alloc, dtype = np.float32)
                                        expression[self.id_object[s1].index_pos] = 2.0
                                        expression[self.id_object[s].index_pos] = -1.0

                                        self.lhs.append(expression)
                                        self.rhs.append(0)
        

        #Force-Mass Equations
        for b in self.block_list:
            expression = np.zeros(self.idx_alloc, dtype = np.float32)
            for s in self.reverse_graph[b]:
                expression[self.id_object[s].index_pos] = 1.0
            expression[self.id_object[b].index_pos] = -self.id_object[b].m
            b = self.id_object[b].mg
            self.lhs.append(expression)
            self.rhs.append(b)

        #Equation for stationary Pulleys
        for p in self.pulley_list:
            expression = np.zeros(self.idx_alloc, dtype = np.float32)
            if self.id_object[p].movable == False:
                expression[self.id_object[p].index_pos] = 1.0
                self.lhs.append(expression)
                self.rhs.append(0)


        self.lhs = np.asarray(self.lhs)
        self.rhs = np.asarray(self.rhs)

        self.solution = np.linalg.solve(self.lhs, self.rhs)
        
        for p in self.pulley_list:
            self.id_object[p].acc = self.solution[self.id_object[p].index_pos]
            print(f"Acceleration of {p}: ", round(self.id_object[p].acc,2))

        for b in self.block_list:
            self.id_object[b].acc = self.solution[self.id_object[b].index_pos]
            print(f"Acceleration of {b}: ", round(self.id_object[b].acc,2))

        for s in self.string_list:
            self.id_object[s].T = self.solution[self.id_object[s].index_pos]
            print(f"Tension of {s}: ", round(self.id_object[s].T,2))

        # print(self.lhs)
        # print(self.rhs)        
        return self.solution



if __name__ == '__main__':
    s = Solver()
    B1 = s.add_object('B', wt_component = 100, mass = 10)
    S1 = s.add_object('S')
    P1 = s.add_object('P', movable=False)
    P2 = s.add_object('P', movable=True)
    B2 = s.add_object('B', wt_component = 200, mass = 20)
    S2 = s.add_object('S')
    B3 = s.add_object('B', wt_component = 100, mass = 10)

    s.add_relation(S1, pulley_on=[P1], endpoints=[B1,P2])
    s.add_relation(S2, pulley_on=[P2], endpoints=[B2,B3])

    solution = s.solve()