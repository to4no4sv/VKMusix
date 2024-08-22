import asyncio
from functools import wraps, partial


class SyncToAsync:
    def __init__(self, func):
        self.func = func


    def __get__(self, instance, owner):
        return partial(self.__call__, instance)


    def __call__(self, instance, *args, **kwargs):
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                return self.func(instance, *args, **kwargs)

            else:
                return loop.run_until_complete(self.func(instance, *args, **kwargs))

        except RuntimeError:
            newLoop = asyncio.new_event_loop()
            asyncio.set_event_loop(newLoop)
            result = newLoop.run_until_complete(self.func(instance, *args, **kwargs))
            newLoop.close()
            return result

        finally:
            asyncio.set_event_loop(loop)


def asyncFunction(func):
    @wraps(func)
    async def wrapper(instance, *args, **kwargs):
        return await func(instance, *args, **kwargs)
    return SyncToAsync(wrapper)