import os

# Automatically configure default logger
try:
    use_logger = os.environ['USE_LOGGER']
except KeyError:
    use_logger = True

if use_logger:
    try:
        import presalytics.lib.logger
    except:
        pass 

