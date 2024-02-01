"""Script for generating sample data for the project
"""
import csv
import random
from typing import List

from faker import Faker

fake = Faker()


def create_users(num_records: int) -> None:
    """Creates sample user data and outputs to CSV

    :param num_records: Number of records to create
    :type num_records: int
    """
    file_name = "users.csv"
    headers = ["user_id", "first_name", "last_name", "email", "created_at", "updated_at"]
    data = []
    for index in range(num_records):
        data.append(
            [
                index + 1,
                fake.first_name(),
                fake.last_name(),
                fake.safe_email(),
                str(fake.date_time()),
                str(fake.date_time()),
            ]
        )
    write_to_csv(file_name, headers, data)


def create_blogs(num_records: int) -> None:
    """Creates sample blog data and outputs to CSV

    :param num_records: Number of records to create
    :type num_records: int
    """
    file_name = "blogs.csv"
    headers = ["blog_id", "user_id", "blog_title", "blog_content", "created_at", "updated_at"]
    data = []
    for index in range(num_records):
        data.append(
            [
                index + 1,
                index + 1,
                fake.word(),
                fake.paragraph(nb_sentences=1),
                str(fake.date_time()),
                str(fake.date_time()),
            ]
        )
    write_to_csv(file_name, headers, data)


def create_comments(num_records: int) -> None:
    """Creates sample comment data and outputs to CSV

    :param num_records: Number of records to create
    :type num_records: int
    """
    file_name = "comments.csv"
    headers = ["comment_id", "blog_id", "user_id", "content", "created_at", "updated_at"]
    data = []
    for index in range(num_records):
        data.append(
            [
                index + 1,
                random.randint(1, num_records),
                random.randint(1, num_records),
                fake.paragraph(nb_sentences=1),
                str(fake.date_time()),
                str(fake.date_time()),
            ]
        )
    write_to_csv(file_name, headers, data)


def create_favorites(num_records: int) -> None:
    """Creates sample favorite data and outputs to CSV

    :param num_records: Number of records to create
    :type num_records: int
    """
    file_name = "favorites.csv"
    headers = ["favorite_id", "blog_id", "user_id", "favorite_date", "created_at", "updated_at"]
    data = []
    for index in range(num_records):
        data.append(
            [
                index + 1,
                random.randint(1, num_records),
                random.randint(1, num_records),
                str(fake.date()),
                str(fake.date_time()),
                str(fake.date_time()),
            ]
        )
    write_to_csv(file_name, headers, data)


def create_opinions(num_records: int) -> None:
    """Creates sample blog opinion data and outputs to CSV

    :param num_records: Number of records to create
    :type num_records: int
    """
    file_name = "blog_opinions.csv"
    headers = ["opinion_id", "blog_id", "user_id", "opinion", "created_at", "updated_at"]
    data = []
    for index in range(num_records):
        data.append(
            [
                index + 1,
                random.randint(1, num_records),
                random.randint(1, num_records),
                random.randint(0, 1),
                str(fake.date_time()),
                str(fake.date_time()),
            ]
        )
    write_to_csv(file_name, headers, data)


def create_tags(num_records: int) -> None:
    """Creates sample blog tag data and outputs to CSV

    :param num_records: Number of records to create
    :type num_records: int
    """
    file_name = "blog_tags.csv"
    headers = ["tag_id", "blog_id"]
    data = []
    for _ in range(num_records):
        data.append([random.randint(1, 10), random.randint(1, num_records)])
    write_to_csv(file_name, headers, data)


def write_to_csv(file_name: str, headers: List[str], data: List[List[str]]):
    """Writes lists of data to a CSV file

    :param file_name: name of the file to output
    :type file_name: str
    :param headers: headers for the columns of data
    :type headers: List[str]
    :param data: data to write to CSV
    :type data: List[List[str]]
    """
    with open(f"sample_data/{file_name}", "w", encoding="UTF8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(data)


if __name__ == "__main__":
    create_users(100)
    create_blogs(100)
    create_comments(100)
    create_favorites(100)
    create_opinions(100)
    create_tags(100)
