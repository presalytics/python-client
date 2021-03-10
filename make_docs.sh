if [ -d tmp ]; then rm -Rf tmp; fi
mkdir ./tmp
pdoc presalytics --template-dir ./docs/pdoc/templates --html -o tmp
cp -rf ./tmp/* ./docs/
rm -r ./tmp
