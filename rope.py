class rope:
    def __init__(self, id, pulley, end_point1, end_point2):
        self.id = id
        self.pulley = [pulley]
        self.ep1 = end_point1
        self.ep2 = end_point2
        self.a = None
        self.T = None
