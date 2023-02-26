import time
import unittest

from utils import Log

from news_lk3.custom_newspapers import newspaper_class_list

MAX_ARTICLE_AGE = 86_400 * 1_000
MIN_ARTICLE_TITLE_LEN = 10
MAX_PARSE_ARTICLE_TIME = 120

SAFE_NEWSPAPER_CLASS_LIST = newspaper_class_list

log = Log('test_custom_newspaper')


def helper_test_parse(test_case, newspaper_class):
    log.debug(f'[helper_test_parse] {newspaper_class}')
    article_url = newspaper_class.get_test_article_url()

    time_start = time.time()
    article = newspaper_class.parse_article(article_url)

    delta_time = time.time() - time_start

    test_case.assertIsNotNone(article)
    # newspaper_id
    newspaper_id = newspaper_class.get_newspaper_id()
    test_case.assertEqual(newspaper_id, article.newspaper_id)
    # url
    test_case.assertEqual(article_url, article.url)
    # time_ut
    test_case.assertLess(article.time_ut, time_start)
    test_case.assertGreater(article.time_ut, time_start - MAX_ARTICLE_AGE)
    # original_lang
    test_case.assertEqual(
        newspaper_class.get_original_lang(), article.original_lang
    )
    # original_title
    test_case.assertGreater(
        len(article.original_title), MIN_ARTICLE_TITLE_LEN
    )

    # original_body_lines
    test_case.assertGreater(
        len(article.original_body_lines),
        0,
    )

    test_case.assertLess(
        delta_time,
        MAX_PARSE_ARTICLE_TIME,
        delta_time,
    )


class TestCase(unittest.TestCase):
    @unittest.skip('unstable test')
    def testParseSafe(self):
        for newspaper_class in SAFE_NEWSPAPER_CLASS_LIST:
            helper_test_parse(self, newspaper_class)


if __name__ == '__main__':
    unittest.main()
