import numpy as np

class Pulley:
    def __init__(self, id, idx_pos, movable=False, **kwargs):
        '''
        Parameters:
            id: unique id of the Pulley
            idx_pos: the index of the variable associated to this pulley in the lhs of equation
            movable: True if pulley is movable 
        '''
        self.id = id
        self.acc = None
        self.index_pos = idx_pos
        self.movable = movable

class Block:
    def __init__(self, id, idx_pos, wt_component, mass, **kwargs):
        '''
        Parameters:
            id: unique id of the Block
            idx_pos: the index of the variable associated to this block in the lhs of equation
            wt_component: the weight component opposite to the direction of Tension on the block
            mass: mass of the block
        '''
        self.id = id
        self.acc = None
        self.index_pos = idx_pos
        self.m = mass
        self.mg = wt_component

        
class String:
    def __init__(self, id, idx_pos, **kwargs):
        '''
        Parameters:
            id: unique id of the String
            idx_pos: the index of the variable associated to this string in the lhs of equation
        '''
        self.id = id
        self.T = None
        self.index_pos = idx_pos


if __name__ == '__main__':
    pass