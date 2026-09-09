import matplotlib.pyplot as plt
from matplotlib.widgets import SpanSelector
import numpy as np

fig, (ax1, ax2) = plt.subplots(2, figsize=(8, 6))

x = np.linspace(0, 2*np.pi, 100)
y_sin = np.sin(x) + 0.5 * np.random.randn(len(x))
y_cos = np.cos(x) + 0.5 * np.random.randn(len(x))

ax1.plot(x, y_sin, label='Sine', color='blue')
ax1.plot(x, y_cos, label='Cosine', color='red')
ax1.set_title('Press left mouse button and drag '
              'to select a region in the top graph')

line2_1, line2_2 = ax2.plot([], [], [])


def onselect(xmin, xmax):
    indmin, indmax = np.searchsorted(x, (xmin, xmax))
    indmax = min(len(x) - 1, indmax)

    region_x = x[indmin:indmax]
    region_y_sin = y_sin[indmin:indmax]
    region_y_cos = y_cos[indmin:indmax]

    if len(region_x) >= 2:
        line2_1.set_data(region_x, region_y_sin)
        line2_2.set_data(region_x, region_y_cos)
        ax2.set_xlim(region_x[0], region_x[-1])

        newmin = min(region_y_sin.min(), region_y_cos.min())
        newmax = max(region_y_sin.max(), region_y_cos.max())

        ax2.set_ylim(newmin, newmax)
        fig.canvas.draw_idle()


span = SpanSelector(
    ax1,
    onselect,
    "horizontal",
    useblit=True,
    props=dict(alpha=0.5, facecolor="tab:blue"),
    interactive=True,
    drag_from_anywhere=True
)
# Set useblit=True on most backends for enhanced performance.

# Display the plot
plt.show()
