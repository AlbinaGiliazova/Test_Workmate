from typing import Dict
import re
from collections import defaultdict, Counter


# Регистрация доступных отчётов
REPORTS: Dict[str, "Report"] = {}

def register_report(cls):
    REPORTS[cls.name] = cls
    return cls


class Report:
    """
    Базовый класс отчёта. Каждый отчёт должен:
     - иметь атрибут name
     - реализовывать process_line(line: str)
     - реализовывать generate() -> str
    """
    name: str

    def process_line(self, line: str) -> None:
        raise NotImplementedError

    def generate(self) -> str:
        raise NotImplementedError


@register_report
class HandlersReport(Report):
    """
    Отчёт 'handlers': по каждому API-эндпоинту считаем
    сколько строк логов django.request пришло каждого уровня.
    """
    name = "handlers"
    _line_re = re.compile(
        r'^\S+ \S+\s+'           # timestamp
        r'(?P<level>DEBUG|INFO|WARNING|ERROR|CRITICAL)\s+'
        r'django\.request:\s+'
        r'(\w+|Internal Server Error:)\s+'                # HTTP method
        r'(?P<path>/\S+)'        # endpoint
    )

    LEVELS = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

    def __init__(self) -> None:
        # path -> Counter(level -> count)
        self._counts: Dict[str, Counter] = defaultdict(Counter)
        self._total: int = 0

    def process_line(self, line: str) -> None:
        m = self._line_re.match(line)
        if not m:
            return
        lvl = m.group("level")
        path = m.group("path")
        self._counts[path][lvl] += 1
        self._total += 1

    def generate(self) -> str:
        if self._total == 0:
            return "No requests found.\n"

        # соберём все эндпоинты в отсортированном виде
        paths = sorted(self._counts.keys())

        # вычислим ширину столбцов
        handler_col_width = max(len("HANDLER"), max((len(p) for p in paths), default=0)) + 2
        level_col_widths = {}
        for lvl in self.LEVELS:
            max_data = max(
                [self._counts[p].get(lvl, 0) for p in paths] + [lvl],
                key=lambda x: len(str(x))
            )
            level_col_widths[lvl] = len(str(max_data)) + 2

        # формируем шапку
        lines = []
        lines.append(f"Total requests: {self._total}\n")
        header = "HANDLER".ljust(handler_col_width)
        for lvl in self.LEVELS:
            header += lvl.ljust(level_col_widths[lvl])
        lines.append(header)

        # строки с данными
        for p in paths:
            row = p.ljust(handler_col_width)
            for lvl in self.LEVELS:
                cnt = self._counts[p].get(lvl, 0)
                row += str(cnt).ljust(level_col_widths[lvl])
            lines.append(row)

        # итоговая строка с суммами по уровням
        total_row = " ".ljust(handler_col_width)
        for lvl in self.LEVELS:
            s = sum(self._counts[p].get(lvl, 0) for p in paths)
            total_row += str(s).ljust(level_col_widths[lvl])
        lines.append(total_row)

        return "\n".join(lines) + "\n"
