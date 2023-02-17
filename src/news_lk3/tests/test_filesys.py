import unittest

from news_lk3.core import filesys


class TestFileSys(unittest.TestCase):
    def test_get_article_file_only(self):
        TEST_URL = 'https://www.google.com'
        self.assertEqual(
            'fe82f1d1.json',
            filesys.get_article_file_only(TEST_URL),
        )

    def test_get_article_file(self):
        TEST_URL = 'https://www.google.com'
        self.assertEqual(
            '/tmp/news_lk3_data/fe82f1d1.json',
            filesys.get_article_file(TEST_URL),
        )


if __name__ == '__main__':
    unittest.main()
