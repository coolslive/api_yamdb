import csv

from django.conf import settings
from django.core.management import BaseCommand

from reviews.models import (
    Category, Comment, Genre, GenreConnect, Review, Title,
)
from users.models import User

TABLES_DICT = {
    User: "users.csv",
    Category: "category.csv",
    Genre: "genre.csv",
    Title: "titles.csv",
    Review: "review.csv",
    Comment: "comments.csv",
}


class Command(BaseCommand):
    help = "Загрузка фикстур"

    @staticmethod
    def import_users_from_csv():
        """Импорт пользователей из CSV-файла в базу данных"""
        with open(settings.BASE_DIR / "static/data/users.csv", "rt") as f:
            f.readline()
            obj_list = []
            for row in csv.reader(f, dialect="excel"):
                obj_list.append(
                    User(
                        id=row[0],
                        username=row[1],
                        email=row[2],
                        role=row[3],
                        bio=row[4],
                        first_name=row[5],
                        last_name=row[6],
                    ),
                )
        User.objects.bulk_create(obj_list)

    @staticmethod
    def import_categories_from_csv():
        """Импорт из CSV-файла в базу данных"""
        with open(settings.BASE_DIR / "static/data/category.csv", "rt") as f:
            f.readline()
            obj_list = []
            for row in csv.reader(f, dialect="excel"):
                obj_list.append(
                    Category(
                        id=row[0],
                        name=row[1],
                        slug=row[2],
                    ),
                )
            Category.objects.bulk_create(obj_list)

    @staticmethod
    def import_comments_from_csv():
        """Импорт из CSV-файла в базу данных"""
        with open(settings.BASE_DIR / "static/data/comments.csv", "rt") as f:
            f.readline()
            obj_list = []
            for row in csv.reader(f, dialect="excel"):
                obj_list.append(
                    Comment(
                        id=row[0],
                        review=Review.objects.get(id=row[1]),
                        text=row[2],
                        author=User.objects.get(id=row[3]),
                        pub_date=row[4],
                    ),
                )
            Comment.objects.bulk_create(obj_list)

    @staticmethod
    def import_genres_from_csv():
        """Импорт из CSV-файла в базу данных"""
        with open(settings.BASE_DIR / "static/data/genre.csv", "rt") as f:
            f.readline()
            obj_list = []
            for row in csv.reader(f, dialect="excel"):
                obj_list.append(
                    Genre(
                        id=row[0],
                        name=row[1],
                        slug=row[2],
                    ),
                )
            Genre.objects.bulk_create(obj_list)

    @staticmethod
    def import_titles_from_csv():
        """Импорт из CSV-файла в базу данных"""
        with open(settings.BASE_DIR / "static/data/titles.csv", "rt") as f:
            f.readline()
            obj_list = []
            for row in csv.reader(f, dialect="excel"):
                obj_list.append(
                    Title(
                        id=row[0],
                        name=row[1],
                        year=row[2],
                        category=Category.objects.get(id=row[3]),
                    ),
                )
            Title.objects.bulk_create(obj_list)

    @staticmethod
    def import_reviews_from_csv():
        """Импорт из CSV-файла в базу данных"""
        with open(settings.BASE_DIR / "static/data/review.csv", "rt") as f:
            f.readline()
            obj_list = []
            for row in csv.reader(f, dialect="excel"):
                obj_list.append(
                    Review(
                        id=row[0],
                        title=Title.objects.get(id=row[1]),
                        text=row[2],
                        author=User.objects.get(id=row[3]),
                        score=row[4],
                        pub_date=row[5],
                    ),
                )
            Review.objects.bulk_create(obj_list)

    @staticmethod
    def import_genre_titles_from_csv():
        """Импорт из CSV-файла в базу данных"""
        with open(
            settings.BASE_DIR / "static/data/genre_title.csv", "rt"
        ) as f:
            f.readline()
            obj_list = []
            for row in csv.reader(f, dialect="excel"):
                obj_list.append(
                    GenreConnect(
                        id=row[0],
                        title=Title.objects.get(id=row[1]),
                        genre=Genre.objects.get(id=row[2]),
                    ),
                )
            GenreConnect.objects.bulk_create(obj_list)

    def handle(self, *args, **options):
        try:
            self.import_users_from_csv()
            self.import_categories_from_csv()
            self.import_titles_from_csv()
            self.import_reviews_from_csv()
            self.import_genres_from_csv()
            self.import_comments_from_csv()
            self.import_genre_titles_from_csv()
        except Exception as e:
            self.stdout.write(self.style.ERROR(e))
            raise e
        self.stdout.write(
            self.style.SUCCESS("Данные CSV были успешно импортированы!")
        )
