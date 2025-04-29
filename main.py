import argparse
from errors import OptionsError


def get_options(args):
    """Получение и проверка параметров командной строки."""
    logs = args.logs
    if not logs:
        raise OptionsError()
    logs = logs.split(' ')
    
    report_name = args.report
    if not report_name:
        report_name = 'handlers.txt'
    return logs, report_name


def main():
    """Главная функция."""
    parser = argparse.ArgumentParser(
        description='Отчёт о логах.'
    )
    parser.add_argument('logs', help='пути к файлам логов')
    parser.add_argument('-report',
                        default='handlers.txt',
                        help='название отчёта (по умолчанию %(default)s)')  
    args = parser.parse_args()
    logs, report_name = get_options(args)
    




if __name__ == '__main__':
    main()
