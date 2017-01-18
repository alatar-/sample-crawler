import argparse
import datetime
import logging
import schedule
import time

from crawler import crawl_catalog, crawl_changes


def set_logging(debug):
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s %(levelname)-8s %(name)-16s %(message)s',
        datefmt='%H:%M:%S',
    )


def execute(args):
    if args.mode == 'store':
        crawl_catalog(args.timestamp)
    
    if args.mode == 'detect':
        crawl_changes()
        if 'schedule' in args:
            schedule.every(args.schedule).minutes.do(crawl_changes)
            while True:
                schedule.run_pending()
                time.sleep(1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Otomoto-crawler runner.')
    subparsers = parser.add_subparsers(dest='mode')
    subparsers.required = True
    
    parser_mode_store = subparsers.add_parser('store', help="crawl and store the catalog offers")
    parser_mode_store.add_argument('-t', '--timestamp', metavar='TS', type=lambda s: datetime.datetime.strptime(s, '%Y-%m-%dT%H:%M'),
                                   help='limit crawling to offers newer than TS, e.g. 2017-01-17T12:00')
    
    parser_mode_detect = subparsers.add_parser('detect', help="detect finalized transations and congratulate sellers")
    parser_mode_detect.add_argument('-s', '--schedule', metavar='M', type=int, nargs='?', const=60, default=argparse.SUPPRESS,
                                    help='schedule iterative execution every M minutes')

    parser.add_argument('--debug', action='store_true', help="enable debug loggers")

    args = parser.parse_args()
    set_logging(args.debug)
    execute(args)
