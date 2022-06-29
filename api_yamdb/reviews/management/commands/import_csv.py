import csv

from django.core.management.base import BaseCommand, CommandError

from reviews.models import Category, Comment, Genre, GenreTitle, Review, Title
from users.models import CustomUser


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('-f',
                            '--file',
                            action='store',
                            help='Input file .csv',
                            )

    def handle(self, *args, **options):
        if not options['file']:
            raise CommandError('you have to set up filepath')
        filepath = options['file']
        filename = filepath.split('/')[-1]
        if not filename.endswith('.csv'):
            raise CommandError('only .csv file allowed')
        model_name = filename.replace(
            '.csv', '').replace('_', ' ').title().replace(' ', '')
        with open(filepath, 'r', encoding='utf-8') as file:
            csv_file = csv.reader(file)
            next(csv_file)
            callbacks = {
                'Category': self.parse_csv_category(csv_file, model_name),
                'Genre': self.parse_csv_genre(csv_file, model_name),
                'Titles': self.parse_csv_title(csv_file, model_name),
                'Review': self.parse_csv_review(csv_file, model_name),
                'Comments': self.parse_csv_comment(csv_file, model_name),
                'GenreTitle': self.parse_csv_genreTitle(csv_file, model_name),
                'Users': self.parse_csv_users(csv_file, model_name)
            }
            try:
                callbacks[model_name]
            except KeyError:
                raise CommandError(f'No model named {model_name}')
            return

    def parse_csv_category(self, csv_file, model_name):
        if model_name == 'Category':
            for row in csv_file:
                Category.objects.update_or_create(name=row[1],
                                                  slug=row[2])
            self.stdout.write(
                self.style.SUCCESS(f'Successfully imported {model_name}\n'))
        return

    def parse_csv_genre(self, csv_file, model_name):
        if model_name == 'Genre':
            for row in csv_file:
                Genre.objects.update_or_create(name=row[1],
                                               slug=row[2])
            self.stdout.write(
                self.style.SUCCESS(f'Successfully imported {model_name}\n'))
        return

    def parse_csv_title(self, csv_file, model_name):
        if model_name == 'Titles':
            for row in csv_file:
                Title.objects.update_or_create(
                    name=row[1],
                    year=row[2],
                    category=Category.objects.get(id=row[3])
                )
            self.stdout.write(
                self.style.SUCCESS(f'Successfully imported {model_name}\n'))
        return

    def parse_csv_review(self, csv_file, model_name):
        if model_name == 'Review':
            for row in csv_file:
                Review.objects.update_or_create(
                    title=Title.objects.get(id=row[1]),
                    text=row[2],
                    author=CustomUser.objects.get(
                        id=row[3]),
                    score=row[4],
                    pub_date=row[5])
            self.stdout.write(
                self.style.SUCCESS(f'Successfully imported {model_name}\n'))
        return

    def parse_csv_comment(self, csv_file, model_name):
        if model_name == 'Comments':
            for row in csv_file:
                Comment.objects.update_or_create(
                    review=Review.objects.get(id=row[1]),
                    text=row[2],
                    author=CustomUser.objects.get(id=row[3]),
                    pub_date=row[4])
            self.stdout.write(
                self.style.SUCCESS(f'Successfully imported {model_name}\n'))
        return

    def parse_csv_genreTitle(self, csv_file, model_name):
        if model_name == 'GenreTitle':
            for row in csv_file:
                GenreTitle.objects.update_or_create(
                    title=Title.objects.get(id=row[1]),
                    genre=Genre.objects.get(id=row[2]))
            self.stdout.write(
                self.style.SUCCESS(f'Successfully imported {model_name}\n'))
        return

    def parse_csv_users(self, csv_file, model_name):
        if model_name == 'Users':
            for row in csv_file:
                CustomUser.objects.update_or_create(id=row[0], username=row[1],
                                                    email=row[2], role=row[3],
                                                    bio=row[4],
                                                    first_name=row[5],
                                                    last_name=row[6])
            self.stdout.write(
                self.style.SUCCESS(f'Successfully imported {model_name}\n'))
        return
