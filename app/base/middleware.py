def middleware_list(package, names):
    return [f"{package}.{name}" for name in names]