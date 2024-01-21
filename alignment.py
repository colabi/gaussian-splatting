# from scene.colmap_loader import read_extrinsics_text, read_intrinsics_text, qvec2rotmat
# import quaternion


# rotation_matrix = [
#     [0.9907987706943584, -0.1005435301870792, -9.06023980260358e-002],
# [-6.380014327147308e-002, -0.937349190545091, 0.3424996886173798],
# [-0.1193622122327156, -0.3335678244705003, -0.9351391173343835]
# ]
# quaternion_wxyz = quaternion.from_rotation_matrix(rotation_matrix)
# qvec = [0.171981, -0.982762, -0.0418066, -0.0534118]
# print(quaternion_wxyz)
# print(qvec)
# #y and z in bundler are negated

# testvecs = [
#     [1,0,0,0],
#     [0,1,0,0],
#     [0,0,1,0],
#     [0,0,0,1]
# ]


# for qvec in testvecs:
#     q = qvec2rotmat(qvec)
#     print(q)

import numpy as np

p_orig = [33.519539, 12.567035, 11.564203, 1.0]
mvp = [[-0.406135, -0.263145, 0.822257, 0.822175], 
    [-0.074304, -0.992629, -0.340647, -0.340613], 
    [0.676642, -0.266949, 0.456128, 0.456083], 
    [34.193218, 12.112477, 6.646991, 6.656327]]
p_proj = [0.780222, -0.348476, 0.999816]
tp = np.matmul(p_orig, mvp)
print(tp)
print(tp/tp[3])