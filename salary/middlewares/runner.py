from typing import TypeVar, Generic
from types import FunctionType

T = TypeVar('T')

class MiddlewareContext(Generic[T]):
    payload: T
    handler: FunctionType

    def __init__(self, payload: T, handler: FunctionType):
        self.payload = payload
        self.handler = handler


class MiddlewareRunner:
    def __init__(self):
        self._middleware_array = []
        self._applied = None

    def set_middlewares(self, middlewares):
        self._middleware_array.clear()
        for m in middlewares:
            self.add_middleware(m)

    def add_middleware(self, middleware):
        self._middleware_array.append(middleware)

    def _dispatch(self, ctx: MiddlewareContext):
        return ctx.handler(ctx.payload)

    def process(self):
        last = self._dispatch
        for m in reversed(self._middleware_array):
            last = m(last)
        self._applied = last

    def apply(self, handler):
        def _exc(payload):
            if self._applied is not None:
                return self._applied(MiddlewareContext(payload, handler))
            return None

        return _exc
