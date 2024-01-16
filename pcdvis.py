import open3d as o3d
import json
import copy

# pcdpath = "/tmp/point_cloud.ply"
pcdpath = "/Volumes/WORKING/recon/115886CF-AF45-4AEB-B1F4-DDF5CF588EF4/input.ply"
camerapath = "/Volumes/WORKING/recon/115886CF-AF45-4AEB-B1F4-DDF5CF588EF4/out.myxed"
cameraquatpath = "/Volumes/WORKING/recon/115886CF-AF45-4AEB-B1F4-DDF5CF588EF4/input_cameras.quat"
ply_point_cloud = o3d.data.PLYPointCloud()
pcd = o3d.io.read_point_cloud(pcdpath)
objects = []
# objects.append(pcd)
INVR = 1.0/(180.0/3.14159)

if True:
    with open(camerapath, "r") as cf:
        data = cf.read()
        cameras = json.loads(data)["cameras"]
        f = o3d.geometry.TriangleMesh.create_coordinate_frame(size=1, origin=[0, 0, 0])
        idx = 0
        for cam in cameras:
            if idx < 3000 and idx % 5 == 0:
                f = o3d.geometry.TriangleMesh.create_coordinate_frame(size=1, origin=[0, 0, 0])
                R = f.get_rotation_matrix_from_xyz((cam[4]*INVR, cam[5]*INVR, cam[6]*INVR))
                f.rotate(R, center=(0,0,0))
                f.translate((cam[1], cam[2], cam[3]))
                objects.append(f)
            idx += 1

if False:
    with open(cameraquatpath, "r") as cf:
        # f = o3d.geometry.TriangleMesh.create_coordinate_frame(size=1, origin=[0, 0, 0])
        idx = 0
        for line in cf.readlines():
            cam = line.split(" ")
            if idx < 3000 and idx % 1 == 0:
                print(cam[0], cam[1], cam[2], cam[3])
                f = o3d.geometry.TriangleMesh.create_coordinate_frame(size=1, origin=[0, 0, 0])
                # R = f.get_rotation_matrix_from_quaternion((cam[4], cam[5], cam[6], cam[7]))
                # f.rotate(R, center=(0,0,0))
                f.translate((cam[1], cam[2], cam[3]))
                objects.append(f)
            idx += 1

o3d.visualization.draw_geometries(objects)