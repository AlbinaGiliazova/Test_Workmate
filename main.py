import argparse
import os
import sys

from reports import Report, REPORTS


def parse_args():
    parser = argparse.ArgumentParser(
        description="Анализ django-логов и формирование отчётов"
    )
    parser.add_argument(
        "logs",
        nargs="+",
        help="пути к файлам логов"
    )
    parser.add_argument(
        "--report", "-r",
        required=True,
        choices=list(REPORTS.keys()),
        help="название отчёта"
    )
    return parser.parse_args()


def main():
    """Главная функция."""
    args = parse_args()

    # проверим, что все файлы существуют
    for path in args.logs:
        if not os.path.isfile(path):
           sys.exit(f"Error: log file not found: {path}")

    # создаём экземпляр нужного отчёта
    reportcls = REPORTS[args.report]
    report: Report = reportcls()

    # читаем все файлы построчно
    for path in args.logs:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                report.process_line(line)

    # печатаем результат
    print(report.generate(), end="") 


if __name__ == '__main__':
    main()
