import code
import io
import os
import sys
import tokenize
import traceback

class DoubleQuoteError(Exception):
    """Raised when double quotes are found in code."""

def myexcepthook(type, value, tb):
    if type is DoubleQuoteError:
        traceback.print_tb(tb, limit=1)
        print("SyntaxError: Double quotes are not allowed.")
    else:
        # -1 to prevent seeing the first frame, that shows this is a custom console!
        traceback.print_exception(type, value, tb, limit=-1)

sys.excepthook = myexcepthook


class CustomConsole(code.InteractiveConsole):
    def runsource(
        self,
        source: str,
        filename: str = "<stdin>",
        symbol: str = "single",
    ) -> bool:
        # First, check if it could be incomplete input, return True if it is.
        # This will allow it to keep taking input
        try:
            if code.compile_command(source) == None:
                return True
        except:
            pass

        try:
            source_file = io.BytesIO(source.encode())
            tokens = tokenize.tokenize(source_file.readline)
            if any(token.type == tokenize.STRING and token.string.startswith('"') for token in tokens):
                raise DoubleQuoteError

            code_obj = compile(source, filename, mode=symbol)
        except (ValueError, SyntaxError):
            # Let the original implementation take care of incomplete input / errors
            return super().runsource(source, filename, symbol)

        self.runcode(code_obj)
        return False


# For tab completion and arrow key support
if sys.platform != "win32":
    import readline

    readline.parse_and_bind("tab: complete")

CustomConsole().interact(banner="", exitmsg="")
# To kill interactive mode, if -i flag was passed
os._exit(0)
