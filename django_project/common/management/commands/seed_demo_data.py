from django.core.management.base import BaseCommand

from common.sample_data import DEMO_PASSWORD, seed_demo_data


class Command(BaseCommand):
    help = "Seed demo users, fixtures, scores, stats, highlights, broadcasts, and press releases."

    def handle(self, *args, **options):
        summary = seed_demo_data()
        self.stdout.write(self.style.SUCCESS("Demo data is ready."))
        self.stdout.write(
            "Created users: {users}, matches: {matches}, scores: {scores}, stats: {stats}, highlights: {highlights}, broadcasts: {broadcasts}, press: {press}".format(
                **summary
            )
        )
        self.stdout.write(f"Demo password for seeded users: {DEMO_PASSWORD}")
