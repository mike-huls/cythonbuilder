import unittest

from src.cythonbuilder.services import logger, set_logger_debug_mode



class TestPyi_generator(unittest.TestCase):

    def setUp(self) -> None:
        # app_config.load_env()
        pass

    def test_logger(self):
        """ Mainly for 100% code coverage """

        self.assertEqual(20, logger.level)
        set_logger_debug_mode(logger=logger)
        self.assertEqual(10, logger.level)



