from matplotlib import pyplot as plt
import presalytics
import presalytics.lib
import presalytics.lib.widgets
import presalytics.lib.widgets.matplotlib

plt.plot([1, 2, 3, 4])
plt.ylabel('Y-axis')
plt.xlabel('X-Axis')

test_plot_1 = presalytics.lib.widgets.matplotlib.MatplotlibPyplot(plt, 'test_plot_1', module=__name__)
