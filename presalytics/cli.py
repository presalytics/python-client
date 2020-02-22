import argparse
import presalytics

parser = argparse.ArgumentParser(
    description="Automatically generate API docs for Python modules.",
    epilog="Further documentation is available at <https://pdoc3.github.io/pdoc/doc>.",
)
add = parser.add_argument
group_add = parser.add_mutually_exclusive_group().add_argument

add('--version', action='version', version='%(prog)s ' + presalytics.__version__)


def main(_args=None):
    """ Command-line entry point """
    global args
    args = _args or parser.parse_args()

if __name__ == "__main__":
    main(parser.parse_args())