from django.core.management.base import BaseCommand
from main.factories import RegionFactory, AdFactory, UserFactory, GarageFactory


class Command(BaseCommand):
    help = 'Generate test data'

    def add_arguments(self, parser):
        parser.add_argument('--count', type=int, help='Количество записей которое будет сгенерировано')

    def handle(self, *args, **options):
        for _ in range(0, options['count']):
            region = RegionFactory()
            user = UserFactory()
            garage = GarageFactory()
            AdFactory(user=user, region=region, content_object=garage)

        self.stdout.write(self.style.SUCCESS('Тестовые данные успешно сгенерированы!'))
