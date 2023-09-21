import numpy as np
def in_rect(rect,target):
    a = (rect[0][0], rect[0][1])
    b = (rect[1][0], rect[1][1])
    c = (rect[2][0], rect[2][1])
    d = (rect[3][0], rect[3][1])
    e = (target[0], target[1])

    # 原点から点へのベクトルを求める
    vector_a = np.array(a)
    vector_b = np.array(b)
    vector_c = np.array(c)
    vector_d = np.array(d)
    vector_e = np.array(e)

    # 点から点へのベクトルを求める
    vector_ab = vector_b - vector_a
    vector_ae = vector_e - vector_a
    vector_bc = vector_c - vector_b
    vector_be = vector_e - vector_b
    vector_cd = vector_d - vector_c
    vector_ce = vector_e - vector_c
    vector_da = vector_a - vector_d
    vector_de = vector_e - vector_d

    # 外積を求める
    vector_cross_ab_ae = np.cross(vector_ab, vector_ae)
    vector_cross_bc_be = np.cross(vector_bc, vector_be)
    vector_cross_cd_ce = np.cross(vector_cd, vector_ce)
    vector_cross_da_de = np.cross(vector_da, vector_de)
    #print(vector_cross_ab_ae,vector_cross_bc_be,vector_cross_cd_ce,vector_cross_da_de)
    return vector_cross_ab_ae > 0 and vector_cross_bc_be > 0 and vector_cross_cd_ce > 0 and vector_cross_da_de > 0