import logging

# custom_time_format = '%Y-%m-%d %H:%M:%S'
custom_time_format = '%H:%M'
logging.basicConfig(
    level=logging.DEBUG,
    # filename="page_analyzer.log",
    # filemode="w",
    format="%(asctime)s %(name)s %(levelname)s %(message)s",
    datefmt=custom_time_format
)

log = logging.getLogger(__name__)
log.info('Logger is active!')
