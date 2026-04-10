from typing import Optional
from colorama import Fore, Style, init
from contextlib import contextmanager
import datetime
import time
import os
import re

init()


class Logger:
    levels = {
        "DEBUG": Fore.CYAN,
        "INFO": Fore.BLUE,
        "SUCCESS": Fore.GREEN,
        "WARNING": Fore.YELLOW,
        "ERROR": Fore.RED,
        "CRITICAL": Fore.MAGENTA,
    }

    def __init__(
        self,
        tree: Optional[list] = None,
        levelColorScheme: Optional[dict] = None,
        variables: Optional[dict] = None,
        devider: Optional[str] = None,
    ):
        self.tree: Optional[list] = tree or None
        self.colorScheme: dict = levelColorScheme or self.levels
        self.variables: Optional[dict] = variables if variables else None
        self.devider: str = devider or "-"
        self._indentLevel: int = 0

    def _stripAnsi(self, text: str) -> str:
        return re.sub(r"\x1b\[[0-9;]*m", "", text)

    def _buildLogs(
        self,
        message: str,
        level: str = "INFO",
        useBuiltIns: bool = True,
        groupLevel: Optional[int] = None,
    ):
        time = datetime.datetime.now().strftime("%H:%M:%S")
        levelColored = f"{self.colorScheme.get(level.upper(), Fore.WHITE)}{level.upper()}{Style.RESET_ALL}"

        builtIns = {
            "{message}": message,
            "{time}": time,
            "{level}": levelColored,
            "{resetStyle}": Style.RESET_ALL,
            "{black}": Fore.BLACK,
            "{red}": Fore.RED,
            "{blue}": Fore.BLUE,
            "{bold}": Style.BRIGHT,
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

        if groupLevel is not None:
            if groupLevel < 0:
                raise ValueError("Invalid value for 'groupLevel': Expected number >= 0")
            indent = "  " * groupLevel
        else:
            indent = "  " * self._indentLevel

        return indent + output

    def setGroupLevel(self, groupLevel: int = 0) -> None:
        if groupLevel < 0:
            raise ValueError("Invalid value for 'groupLevel': Expected number >= 0")
        self._indentLevel = groupLevel

    def console(
        self,
        message: str,
        level: str = "INFO",
        useBuiltIns: bool = True,
        groupLevel: Optional[int] = None,
    ):
        """Send a logs to the terminal with the log and the log level

        builtIns = {
            "{message}": message,
            "{time}": time,
            "{level}": levelColored,
            "{resetStyle}": Style.RESET_ALL,
            "{black}": Fore.BLACK,
            "{red}": Fore.RED,
            "{blue}": Fore.BLUE,
            "{bold}": Style.BRIGHT,
        }
        user-defined variables overwrite builtins"""

        output: str = self._buildLogs(message, level, useBuiltIns, groupLevel)
        print(output + Style.RESET_ALL)

    def save(
        self,
        message: str,
        level: str = "INFO",
        logFile: str = "app.log",
        useBuiltIns: bool = True,
        groupLevel: Optional[int] = None,
    ):

        output: str = self._stripAnsi(
            self._buildLogs(message, level, useBuiltIns, groupLevel)
        )
        with open(logFile, "a") as filename:
            filename.write(f"{output}\n")

    def log(
        self,
        message: str,
        level: str = "INFO",
        logFile: str = "app.log",
        useBuiltIns: bool = True,
        groupLevel: Optional[int] = None,
    ):
        if groupLevel:
            self.console(message, level, useBuiltIns, groupLevel=groupLevel)
            self.save(message, level, logFile, useBuiltIns, groupLevel)
        else:
            self.console(message, level, useBuiltIns)
            self.save(message, level, logFile, useBuiltIns)

    def devide(self) -> None:
        cmdSize = os.get_terminal_size()
        line = self.devider * cmdSize.columns
        print(line)

    @contextmanager
    def timer(
        self, label: str, level: str = "DEBUG", warnAfter: Optional[float] = None
    ):
        start: float = time.perf_counter()
        yield
        elapsed: float = time.perf_counter() - start
        ms: float = elapsed * 1000
        tresholdLevel: str = "WARNING" if (warnAfter and ms > warnAfter) else level
        self.console(f"{label} took {ms}ms", level=tresholdLevel)
