from matplotlib import pyplot as plt
import presalytics
import presalytics.lib
import presalytics.lib.widgets
import presalytics.lib.widgets.matplotlib

fig, ax = plt.subplots()

ax.plot([3,1,4,1,5], 'ks-', mec='w', mew=5, ms=20)
ax.set_title("test plot")


test_plot_1 = presalytics.lib.widgets.matplotlib.MatplotlibFigure(fig, 'test_plot_1', module=__name__)
