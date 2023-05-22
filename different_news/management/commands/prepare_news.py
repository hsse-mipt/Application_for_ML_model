from django.core.management.base import BaseCommand
from different_news.utils import update_news


class Command(BaseCommand):
    help = "Единоразовый парсинг новостей для стартовой страницы"

    def handle(self, *args, **options):
        update_news()
