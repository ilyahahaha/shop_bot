from functools import wraps


def singleton(cls):
    """
    Реализация декоратора класса для создания синглетона.
    Взято из https://github.com/siddheshsathe/handy-decorators/blob/master/src/decorators.py
    """
    previous_instances = {}

    @wraps(cls)
    def wrapper(*args, **kwargs):
        if cls in previous_instances and previous_instances.get(cls, None).get(
            "args"
        ) == (args, kwargs):
            return previous_instances[cls].get("instance")
        else:
            previous_instances[cls] = {
                "args": (args, kwargs),
                "instance": cls(*args, **kwargs),
            }
            return previous_instances[cls].get("instance")

    return wrapper
