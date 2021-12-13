import logging

logging.basicConfig(
    level=logging.CRITICAL,
    # format=f'[{appname}] - %(levelname)s [%(asctime)s] %(message)s',
    format=f'[{appname}] %(asctime)s  %(message)s',
    datefmt='%H:%M:%S',
)
