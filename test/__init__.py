from functools import lru_cache
import presalytics

@lru_cache(maxsize=None)
def get_test_client():
    client = presalytics.Client()
    return client