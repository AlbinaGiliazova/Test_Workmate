import argparse
from errors import OptionsError


def main():
    """Главная функция."""
    parser = argparse.ArgumentParser(
        description='Отчёт о логах.'
    )
    parser.add_argument('logs',
                        nargs='+',  # 1 или более файлов.
                        type=argparse.FileType('r'),  # Открыть файлы.
                        help='Пути к файлам логов')
    parser.add_argument('-report',
                        default='handlers.txt',
                        help='Название отчёта (по умолчанию %(default)s)')  
    args = parser.parse_args()
    logs = args.logs
    report_name = args.report


if __name__ == '__main__':
    main()
