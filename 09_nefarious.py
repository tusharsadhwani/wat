import sys

def password_tracer(frame, event, arg):
    tmpfile = open('/tmp/tracelog', 'a')
    if event != 'call':
        return

    if not (
        'password' in frame.f_code.co_name
        or 'password' in frame.f_code.co_varnames
    ):
        return

    print("Called", frame.f_code.co_name, file=tmpfile)
    for name in frame.f_code.co_varnames:
        print("    Argument", name, "is", frame.f_locals[name], file=tmpfile)
    
    print("----------", file=tmpfile)

sys.settrace(password_tracer)
