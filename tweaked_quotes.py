import code
import os
import sys

class CustomConsole(code.InteractiveConsole):
    def runsource(
        self,
        source: str,
        filename: str = "<stdin>",
        symbol: str = "single",
    ) -> bool:
        import code
        import io
        import tokenize

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
                print("SyntaxError: Double quotes are not allowed.")
                return False

            code_obj = compile(source, filename, mode=symbol)
        except (ValueError, SyntaxError):
            # Let the original implementation take care of incomplete input / errors
            return super().runsource(source, filename, symbol)

        self.runcode(code_obj)
        return False


if "-i" in sys.orig_argv or len(sys.orig_argv) == 1:
    # For tab completion and arrow key support
    if sys.platform != "win32":
        import readline

        readline.parse_and_bind("tab: complete")

    CustomConsole().interact(banner="", exitmsg="")
    # To kill interactive mode, if -i flag was passed
    os._exit(0)
