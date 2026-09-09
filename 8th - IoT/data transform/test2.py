import matplotlib.pyplot as plt
from matplotlib.widgets import SpanSelector
import pandas as pd

fig, axes = plt.subplots(2,1)

df = pd.read_csv('raw_data/subject_0/Left Swipe_MetaWear_2024-05-04T14.33.38.146_C10F6B5AC415_Accelerometer_100.000Hz_1.7.3.csv')

# print(df[["x-axis (g)", "y-axis (g)", "z-axis (g)"]].head())
df = df[['x-axis (g)', 'y-axis (g)', 'z-axis (g)']]
df.plot(ax=axes[0]).legend()
df.plot(ax=axes[1])

def onselect(xmin, xmax):
    axes[1].set_xlim(left=xmin, right=xmax)
    fig.canvas.draw_idle()
    
span_0 = SpanSelector(
    axes[0],
    onselect,
    "horizontal",
    button=1,
    useblit=True,
    props=dict(alpha=0.5, facecolor="tab:blue"),
    interactive=True,
    drag_from_anywhere=True
)

#TODO: add modifier to save instead of zoom
span_1 = SpanSelector(
    axes[1],
    onselect,
    "horizontal",
    button=1,
    useblit=True,
    props=dict(alpha=0.5, facecolor="tab:blue"),
    drag_from_anywhere=True
)

span_1_save = SpanSelector(
    axes[1],
    print("ok"), #TODO: save function
    "horizontal",
    button=3,
    useblit=True,
    props=dict(alpha=0.5, facecolor="tab:red"),
    interactive=True,
    drag_from_anywhere=True,
)

def on_key_press(event):
    if event.key == 'right':
        (xmin, xmax) = axes[1].get_xlim()
        range = xmax - xmin
        xmin = int(xmin + range / 3)
        xmax = int(xmax + range / 3)

        axes[1].set_xlim(left=xmin+250, right=xmax+250)
        fig.canvas.draw_idle()

fig.canvas.mpl_connect('key_press_event', on_key_press)
        

# plt.xlabel('Sample', fontsize=20)
# plt.ylabel('Axes', fontsize=20)
plt.show()