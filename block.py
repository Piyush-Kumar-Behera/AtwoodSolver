import math

def dist(p1, p2):
    return math.sqrt(((p1[0]-p2[0])**2) + ((p1[1]-p2[1])**2))

def compute_theta(pulley_centre, bl_cd):
    dist_list = []
    for i in range(4):
        dist_list.append(dist((bl_cd[i][0],bl_cd[i][1]),pulley_centre))

    s_dist_list = sorted(dist_list)

    point_n = None
    point_f = None
    for i in range(4):
        if dist_list[i] == s_dist_list[0] or dist_list[i] == s_dist_list[1]:
            point_n = (bl_cd[i][0],bl_cd[i][1])
            if i > 0:
                point_f = (bl_cd[i-1][0],bl_cd[i-1][1])
            else:
                if dist_list[i+1] == s_dist_list[0] or dist_list[i+1] == s_dist_list[1]:
                    point_f = (bl_cd[3][0],bl_cd[3][1])
                else:
                    point_f = (bl_cd[i+1][0],bl_cd[i+1][1])
    
    ret = math.atan(abs(point_n[0]-point_f[0])/(abs(point_n[1]-point_f[1])+0.01))
    return point_f, point_n, ret

class block:
    def __init__(self, id, string, pulley_centre,block_coordinates, m = 5):
        self.id = id
        self.string = string
        self.block_cord = block_coordinates
        self.p1, self.p2, self.theta = compute_theta(pulley_centre = pulley_centre, bl_cd = block_coordinates)
        self.m = m

if __name__ == '__main__':
    pass