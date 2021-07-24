
from typing import Callable, Dict, List, Optional, Tuple, Type


class CommandArgument:
    def __init__(self, args: List[Type]) -> None:
        self.length = len(args)
        self.args = args


class CommandFunction:
    def __init__(self, function: Callable, arg: CommandArgument = None) -> None:
        self.function = function
        self.arg = arg

    def run(self, args: Optional[List[str]]):
        a = self.arg.args
        r = (a[i](args[i]) for i in range(self.arg.length))
        self.function(*r)


class CommandCompiler:
    def __init__(self, commandList: Dict[int, Dict[str, CommandFunction]], help: str = "") -> None:
        commandList[0]["help"]=CommandFunction(self.help)
        self.commandList = commandList
        self.helpInfo: str = help

    def compiled(self, cmd: List[str]):
        cl = self.commandList
        if len(cmd) == 1:
            self.help()
            return
        key = cmd[1]
        length = len(cmd)-2
        args = cmd[2:]
        if length not in cl:
            raise ValueError("找不到指定函数")
        else:
            if key not in cl[length]:
                raise ValueError("找不到指定函数")
            else:
                self.run(cl[length][key], args)

    def help(self):
        print(self.helpInfo)

    def run(self, cf: CommandFunction, args: List[str]):
        cf.run(args)


class EasyCommandCompiler(CommandCompiler):
    def __init__(self, commandList: Dict[int, Dict[str, Tuple[Callable, List[Type]]]], help: str = "") -> None:
        commandList[0]["help"]=(self.help,[])
        self.commandList = commandList
        self.helpInfo = help

    def run(self, cf: Tuple[Callable, List[Type]], args: List[str]):
        r = (cf[1][i](args[i]) for i in range(len(args)))
        cf[0](*r)
