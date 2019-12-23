import datetime


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
    
