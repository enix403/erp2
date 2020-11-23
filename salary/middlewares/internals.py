from .runner import MiddlewareRunner


class ViewDef:
    def __init__(self, name):
        self.name = name

    def matches(self, name):
        return self.name == name


class RouteGroup:
    def __init__(self, middlewares=[], children=[]):
        self.middleware_runner = MiddlewareRunner()
        self.middleware_runner.set_middlewares(middlewares)
        self.children = children

    def process_middleware(self):
        self.middleware_runner.process()
        for child in self.children:
            if isinstance(child, RouteGroup):
                child.process_middleware()

    def get_handler(self, name, handler_next):
        for child in self.children:
            if isinstance(child, RouteGroup):
                child_handle = child.get_handler(name, handler_next)
                if child_handle is not None:
                    return self.middleware_runner.apply(child_handle)
            elif isinstance(child, ViewDef):
                if child.matches(name):
                    return self.middleware_runner.apply(handler_next)
        return None
