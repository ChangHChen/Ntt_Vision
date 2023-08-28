import os
import argparse
import numpy as np
import matplotlib.pyplot as plt
import string

parser = argparse.ArgumentParser(
    prog="depth maps to images",
    description="as title",
)

parser.add_argument("--path", help="path to the depth map folder", type=str)

args = parser.parse_args()
args.path = os.path.abspath(args.path)
os.chdir(args.path)

if not os.path.exists(f"{args.path}/images/"):
    os.makedirs(f"{args.path}/images/")
cmap = plt.cm.viridis


def colored_depthmap(depth, d_min=None, d_max=None):
    if d_min is None:
        d_min = np.min(depth)
    if d_max is None:
        d_max = np.max(depth)

    depth_relative = (d_max - depth) / (d_max - d_min)
    return 225 * cmap(depth_relative)[:, :, :3]


def make_depthmap(depth_map, path, filename):
    if not isinstance(depth_map, np.ndarray):
        depth_map = np.array(depth_map)
    if depth_map.ndim == 3:
        depth_map = depth_map.squeeze()

    depth_map = colored_depthmap(depth_map)

    plt.imshow(depth_map.astype("uint8"))
    plt.axis("off")
    plt.savefig(f"{path}\images\{filename}.png")
    print(f"{filename}.png generated.")


for file in os.listdir():
    if file.endswith(".npy"):
        depth_map = np.load(file)
        filename = file.split("/")[-1].replace(".npy", "")
        make_depthmap(depth_map, args.path, filename)
