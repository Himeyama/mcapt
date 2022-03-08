import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import collections
from mpl_toolkits.mplot3d.art3d import Line3DCollection
from matplotlib.animation import FuncAnimation
import numpy as np
from IPython.display import HTML

def line(frame: int, a: int, b: int):
    return [
        (float(df.loc[frame, :, :, a].X), float(df.loc[frame, :, :, a].Y), float(df.loc[frame, :, :, a].Z)),
        (float(df.loc[frame, :, :, b].X), float(df.loc[frame, :, :, b].Y), float(df.loc[frame, :, :, b].Z))]

def update(frame):
    joint_comb_lines = [line(frame, _[0], _[1]) for _ in joint_comb]
    col = Line3DCollection(joint_comb_lines)
    ax.cla()
    ax.add_collection(col)
    ax.scatter(df.loc[frame, :, :, :].X, df.loc[frame, :, :, :].Y, df.loc[frame, :, :, :].Z)


df = pd.read_csv('test.csv').set_index(['Frame', 'Time', 'Hand', 'Part'])

joint_comb = pd.read_csv('mcapt/hand_joint_conb.csv', header=None).values.tolist()

fig = plt.figure()
ax = fig.add_subplot(projection="3d")
ani = FuncAnimation(fig, update, frames=np.arange(78), interval=50)
plt.show()