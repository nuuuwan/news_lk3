import os

from news_lk3 import NewspaperFactory


def main():
    for newspaper_class in NewspaperFactory.list_all_classes():
        for url in newspaper_class.get_index_urls():
            os.system(f"open -a firefox {url}")


if __name__ == "__main__":
    main()
