#
# Copyright (C) 2023, Inria
# GRAPHDECO research group, https://team.inria.fr/graphdeco
# All rights reserved.
#
# This software is free for non-commercial, research and evaluation use 
# under the terms of the LICENSE.md file.
#
# For inquiries contact  george.drettakis@inria.fr
#

import torch
from torch import nn
import numpy as np
from utils.graphics_utils import getWorld2View2, getProjectionMatrix
from PIL import Image


def myxed_getWorld2View2(R, t, translate=np.array([.0, .0, .0]), scale=1.0):
    # RT = [[-0.51236784, -0.24800345, 0.8221761, 0.0], [0.85363424, -0.25159222, 0.45608112, 0.0], [0.09374341, 0.9355189, 0.340612, 0.0], [0.0, 0.0, 0.0, 1.0]]
    Rt = np.zeros((4, 4))
    Rt[:3, :3] = R
    Rt[3, 3] = 1.0
    Rt = torch.tensor(Rt).type(torch.FloatTensor)

    T = np.zeros((4,4))
    T[0,0] = 1.0
    T[1,1] = 1.0
    T[2,2] = 1.0
    T[3,3] = 1.0
    # T[3, :3] = [-43.137, -11.416, -6.656]
    T[3, :3] = -t
    T = torch.tensor(T).type(torch.FloatTensor)

    MV = (T.unsqueeze(0).bmm(Rt.unsqueeze(0))).squeeze(0)
    # print(Rt, T, MV)
 
    return MV.type(torch.FloatTensor)

class Camera(nn.Module):
    def __init__(self, colmap_id, R, T, FoVx, FoVy, image, gt_alpha_mask,
                 image_name, uid,
                 trans=np.array([0.0, 0.0, 0.0]), scale=1.0, data_device = "cuda",
                 image_path="",image_height=0,image_width=0
                 ):
        super(Camera, self).__init__()

        self.uid = uid
        self.colmap_id = colmap_id
        self.R = R
        self.T = T
        self.FoVx = FoVx
        self.FoVy = FoVy
        self.image_name = image_name
        self.image_path = image_path

        try:
            self.data_device = torch.device(data_device)
        except Exception as e:
            print(e)
            print(f"[Warning] Custom device {data_device} failed, fallback to default cuda device" )
            self.data_device = torch.device("cuda")

        if False:
            self.original_image = image.clamp(0.0, 1.0).to(self.data_device)
            self.image_width = self.original_image.shape[2]
            self.image_height = self.original_image.shape[1]

            if gt_alpha_mask is not None:
                self.original_image *= gt_alpha_mask.to(self.data_device)
            else:
                self.original_image *= torch.ones((1, self.image_height, self.image_width), device=self.data_device)
        else:
            self.image_width = image_width
            self.image_height = image_height

        self.zfar = 100.0
        self.znear = 0.01

        self.trans = trans
        self.scale = scale

        MV = [[-0.51236784, -0.24800345, 0.8221761, 0.0], [0.85363424, -0.25159222, 0.45608112, 0.0], [0.09374341, 0.9355189, 0.340612, 0.0], [11.732968, 7.3434877, -42.939945, 1.0]]
        MVP = [[-0.3842759, -0.24800348, -0.8224502, -0.8221761], [0.6402257, -0.25159225, -0.4562332, -0.45608112], [0.07030757, 0.93551904, -0.34072557, -0.340612], [8.7997265, 7.3434887, 42.85423, 42.939945]]
        # self.world_view_transform = torch.tensor(MV).cuda()
        self.world_view_transform = myxed_getWorld2View2(R, T, trans, scale).cuda()
        self.projection_matrix = getProjectionMatrix(znear=self.znear, zfar=self.zfar, fovX=self.FoVx, fovY=self.FoVy).transpose(0,1).cuda()
        self.projection_matrix[0][0] *= -1.0
        self.projection_matrix[0][2] *= -1.0
        self.full_proj_transform = (self.world_view_transform.unsqueeze(0).bmm(self.projection_matrix.unsqueeze(0))).squeeze(0)
        # self.full_proj_transform = torch.tensor(MVP).cuda()

        self.camera_center = self.world_view_transform.inverse()[3, :3]
        # print("MV: ", self.world_view_transform, " MVP: ", self.full_proj_transform)

    def load_image(self):
        image = Image.open(self.image_path)
        original_image = image.clamp(0.0, 1.0).to('cuda')
        return original_image

class MiniCam:
    def __init__(self, width, height, fovy, fovx, znear, zfar, world_view_transform, full_proj_transform):
        self.image_width = width
        self.image_height = height    
        self.FoVy = fovy
        self.FoVx = fovx
        self.znear = znear
        self.zfar = zfar
        self.world_view_transform = world_view_transform
        self.full_proj_transform = full_proj_transform
        view_inv = torch.inverse(self.world_view_transform)
        self.camera_center = view_inv[3][:3]

