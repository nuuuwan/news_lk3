import unittest

from news_lk3.core import filesys


class TestFileSys(unittest.TestCase):
    def test_get_dir_article_shard(self):
        TEST_ARTICLE_FILE_ONLY = '12345678.json'
        self.assertEqual(
            '/tmp/news_lk3_data/articles/12',
            filesys.get_dir_article_shard(TEST_ARTICLE_FILE_ONLY),
        )

    def test_get_article_file_only(self):
        TEST_URL = 'https://www.google.com'
        self.assertEqual(
            'fe82f1d1.json',
            filesys.get_article_file_only(TEST_URL),
        )

    def test_get_article_file(self):
        TEST_URL = 'https://www.google.com'
        self.assertEqual(
            '/tmp/news_lk3_data/articles/fe/fe82f1d1.json',
            filesys.get_article_file(TEST_URL),
        )


if __name__ == '__main__':
    unittest.main()
