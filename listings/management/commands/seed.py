from django.core.management.base import BaseCommand
from listings.models import Listing
from faker import Faker
import random

class Command(BaseCommand):
    help = 'Seed the database with sample listings'

    def handle(self, *args, **kwargs):
        fake = Faker()
        Listing.objects.all().delete()

        for _ in range(20):
            Listing.objects.create(
                name=fake.sentence(nb_words=4),
                description=fake.paragraph(nb_sentences=5),
                price_per_night=round(random.uniform(50, 500), 2),
                location=fake.city(),
                available=random.choice([True, False])
            )

        self.stdout.write(self.style.SUCCESS('Successfully seeded listings.'))
