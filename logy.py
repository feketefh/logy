from colorama import Fore, Style, init
import datetime

init()


class Logger():
    levels = {
        "DEBUG": Fore.CYAN,
        "INFO": Fore.BLUE,
        "SUCCESS": Fore.GREEN,
        "WARNING": Fore.YELLOW,
        "ERROR": Fore.RED,
        "CRITICAL": Fore.MAGENTA
    }


    def __init__(self, tree = None, colorScheme = None, variables = None):
        self.tree: list = tree
        self.colorScheme: dict = colorScheme or self.levels
        self.variables: dict = variables

    def console(self, message, level="INFO", useBuiltIns=True):
        """Send a logs to the terminal with the log and the log level ( levels: SUCCESS, INFO, WARNING, ERROR, CRITICAL, DEBUG )"""
        time = datetime.datetime.now().strftime("%H:%M:%S")
        levelColored = f"{self.colorScheme.get(level.upper(), Fore.WHITE)}{level.upper()}{Style.RESET_ALL}"

        builtIns = {
            "{message}": message,
            "{time}":    time,
            "{level}":   levelColored,
        }

        parts = []
        if self.tree:
            for branch in self.tree:
                result = branch
                if self.variables:
                    for key, value in self.variables.items():
                        result = result.replace(key, value)
                if useBuiltIns:
                    for key, value in builtIns.items():
                        result = result.replace(key, value)
                parts.append(result)
            output = " ".join(parts)
        else:
            output = message

        print(output + Style.RESET_ALL)

    def save(self, message, level="INFO", filename="app.log"):
        time = datetime.datetime.now().strftime("%H:%M:%S")
        with open(filename, "a") as logFile:
            logFile.write(f"[{time}] {level.upper()} - {message}\n")

    def log(self, message, level="INFO", filename="app.log"):
            self.console(message, level)
            self.save(message, level, filename)
