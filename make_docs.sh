if [ -d tmp ]; then rm -Rf tmp; fi
mkdir tmp
pdoc presalytics --template-dir docs/pdoc/templates --html -o tmp
cp -r tmp/presalytics/* docs/
rm -r tmp
