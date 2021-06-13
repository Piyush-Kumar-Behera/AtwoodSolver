import numpy as np
import math

def solve_rope(sx, objects):
    st = objects[sx]
    e1 = objects[st.ep1]
    e2 = objects[st.ep2]
    a1 = [1, -e1.m]
    a2 = [1, e2.m]
    b = np.array([e1.m*9.81*math.sin(e1.theta), e2.m*9.81*math.sin(e2.theta)])
    a = np.array([a1,a2])

    x = np.linalg.solve(a,b)

    st.a = x[1]
    st.T = x[0]

    return objects

