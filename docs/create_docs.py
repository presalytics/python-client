import pdoc, os, sys
out_file = os.path.join(os.path.dirname(__file__), "presalytics.html")
top_level = os.path.dirname(os.path.dirname(__file__))
sys.path.append(top_level)
libpaths = [
    top_level,
    os.path.join(top_level, 'lib'),
    os.path.join(top_level, 'client'),
]
pdoc.import_path.extend(libpaths)
mod = pdoc.import_module('presalytics')
doc = pdoc.Module(mod)
string = doc.html()
with open(out_file, 'w+') as f:
    f.write(string)