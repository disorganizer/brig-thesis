import math
import pygal
import humanize

size = lambda s: 36 + s + math.ceil(s/(64 * 1024)) * (8 + 16)

r = [x + 0.01 for x in range(0, 2 * 1024 * 1024, 1024 * 128)]
v = [size(x) for x in r]

p = pygal.Line(logarithmic=False)
p.add('encrypted', v)
p.add('original', r)
# p.x_labels = [humanize.naturalsize(x) for x in r]
p.y_labels = [humanize.naturalsize(x) for x in v]
p.render_in_browser()
