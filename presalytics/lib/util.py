import datetime
import re
import importlib
import base64
import typing
import presalytics.lib.constants


class classproperty(property):
    def __get__(self, obj, objtype=None):
        return super(classproperty, self).__get__(objtype)

    def __set__(self, obj, value):
        super(classproperty, self).__set__(type(obj), value)

    def __delete__(self, obj):
        super(classproperty, self).__delete__(type(obj))


def roundup_date_modified(current_datetime: datetime.datetime):
    one_second = datetime.timedelta(seconds=1)
    rounddown = current_datetime.replace(microsecond=0)
    return rounddown + one_second


def get_site_host():
    site_host = presalytics.lib.constants.SITE_HOST
    try:
        site_host = presalytics.settings.HOST_SITE
    except (KeyError, AttributeError):
        pass
    return site_host


def import_string(dotted_path) -> type:
    """
    Import a dotted module path and return the attribute/class designated by the
    last name in the path. Raise ImportError if the import failed.
    """
    try:
        module_path, class_name = dotted_path.rsplit('.', 1)
    except ValueError as err:
        raise ImportError("%s doesn't look like a module path" % dotted_path) from err

    module = importlib.import_module(module_path)

    try:
        return getattr(module, class_name)
    except AttributeError as err:
        raise ImportError('Module "%s" does not define a "%s" attribute/class' % (
            module_path, class_name)
        ) from err


def to_snake_case(camel_case_str):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', camel_case_str)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def to_camel_case(snake_str):
    components = snake_str.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])


def to_title_case(name_string):
    try:
        components = re.split('_| ', name_string)
        return ''.join(x[0].upper() + x[1:] for x in components)
    except Exception:
        return name_string.replace(" ", "")


def camel_case_split(str):
    words = [[str[0]]]
    for c in str[1:]:
        if words[-1][-1].islower() and c.isupper():
            words.append(list(c))
        else:
            words[-1].append(c)
    return [''.join(word) for word in words]


def list_to_base64(string_list: typing.List[str]) -> typing.List[str]:
    return_list = []
    for item in string_list:
        bts = base64.b64encode(item.encode('ascii'))
        return_list.append(bts.decode('ascii'))
    return return_list
