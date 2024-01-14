import os
import sys
import csv
from PIL import Image
from typing import NamedTuple
import json

CAMERA_CONFIGURATIONS = {}
with open("./camera_configurations.json") as cfile:
    print("reading camera configuraitons")
    d = cfile.read()
    CAMERA_CONFIGURATIONS = json.loads(d)
    print(CAMERA_CONFIGURATIONS)



def generateDiagCSV():
    HEADER = """ply
    format ascii 1.0 
    element vertex NPOINTS
    property float x
    property float y
    property float z
    property uchar red
    property uchar green
    property uchar blue
    end_header
    """

    with open('cameras.csv', newline='') as csvfile:
        lines = []
        camreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for r in camreader:
            if r[0][0] != "#":
                line = "{} {} {} {} {} {}\n".format(r[1], r[2], r[3], 255, 255, 0)
                lines.append(line)
        nverts = len(lines)
        output = HEADER.replace("NPOINTS", str(nverts))
        for line in lines:
            output += line
        with open("cameras.ply", "w") as outfile:
            outfile.write(output)

class CameraInfo(NamedTuple):
    uid: str
    px: float
    py: float
    pz: float
    rx: float
    ry: float
    rz: float
    config: dict
    width: float
    height: float

def getRename(uid, offset):
    if offset < 0:
        name = uid.replace("frame0","")
        name = name.replace(".png","")
        fid = int(name) + offset
        uid = "%05d.png" % fid
    return uid

def readRCCamerasFile(filepath, configname, imagepath):
    configinfo = CAMERA_CONFIGURATIONS[configname]
    width = 0
    height = 0
    offset = -1
    uid = "frame000001.png"
    uid = getRename(uid, -1)
    image_path = os.path.join(imagepath, uid)
    print("image path: ", image_path)
    image = Image.open(image_path)
    print(image.width, image.height)
    width = image.width
    height = image.height


    lines = []
    with open(filepath, newline='') as csvfile:
        camreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for r in camreader:
            if r[0][0] != "#":
                print(r)
                uid = getRename(r[0], -1)
                ci = CameraInfo(uid, float(r[1]), float(r[2]), float(r[2]), float(r[4]), float(r[5]), float(r[6]), configinfo, width, height)
                lines.append(ci)


    return lines

def createMyxedConfig(camerapath, configname, imagepath):
    cameras = readRCCamerasFile(camerapath, configname, imagepath)
    print(cameras)
    return cameras

if __name__ == "__main__":
    camerapath = sys.argv[1]
    configname = sys.argv[2]
    imagepath = sys.argv[3]
    outpath = sys.argv[4]
    skip = int(sys.argv[5])
    scale = int(sys.argv[6])
    print(camerapath, configname, imagepath, outpath)
    camconfig = createMyxedConfig(camerapath, configname, imagepath)
    configdata = {
        "cameras": camconfig,
        "processing": {
            "skip": skip
        }
    }
    with open(outpath, "w") as outf:
        outf.write(json.dumps(configdata, indent=2))
