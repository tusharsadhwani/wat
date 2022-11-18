from contextlib import suppress
import inspect
import sys
from textwrap import dedent

def has_goto(frame):
    return 'goto' in frame.f_code.co_names

def tracer(frame, event, arg):
    if event == 'call':
        if has_goto(frame):
            # for this new frame, only trace exceptions and returns
            frame.f_trace_lines = False
            code = inspect.getsource(frame)
            new_code = f'from goto import with_goto\n\n@with_goto\n{dedent(code)}\nprint(myrange(2, 5))'
            exec(new_code)

        return None

sys.settrace(tracer)

def myrange(start, stop):
    i = start
    result = []

    label .begin
    if i == stop:
        goto .end

    result.append(i)
    i += 1
    goto .begin

    label .end
    return result

with suppress(NameError):
    print(myrange(2, 5))
