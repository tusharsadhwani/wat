import builtins
import functools
def new_print(orig_print, *a, **kw):
    orig_print("Hello .meetup!")

orig_print = builtins.print
builtins.print = functools.partial(new_print, orig_print)
