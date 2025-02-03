from django.core.management.base import BaseCommand
from lost_found_app.models import LostItem, ItemMatch
from lost_found_app.matching import find_matches_for_item

class Command(BaseCommand):
    help = 'Rerun matching algorithm for all lost items'

    def handle(self, *args, **kwargs):
        # Clear existing matches
        ItemMatch.objects.all().delete()
        self.stdout.write('Cleared existing matches')

        # # Get all lost items
        # lost_items = LostItem.objects.all()
        # total = lost_items.count()
        
        # # Rerun matching for each lost item
        # for index, lost_item in enumerate(lost_items, 1):
        #     matches = find_matches_for_item(lost_item, is_found=False)
        #     self.stdout.write(f'Processed item {index}/{total}: {lost_item.name} - Found {len(matches)} matches')

        # self.stdout.write(self.style.SUCCESS('Successfully rematched all items'))