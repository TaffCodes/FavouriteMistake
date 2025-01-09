from .models import LostItem, FoundItem

def find_matches():
    matches = []
    lost_items = LostItem.objects.all()
    found_items = FoundItem.objects.all()
    for lost_item in lost_items:
        for found_item in found_items:
            if lost_item.vision_labels and found_item.vision_labels:
                lost_labels = set(lost_item.vision_labels.split(', '))
                found_labels = set(found_item.vision_labels.split(', '))
                print(f"Comparing lost item {lost_item.name} with found item {found_item.name}")
                print(f"Lost labels: {lost_labels}")
                print(f"Found labels: {found_labels}")
                if lost_labels & found_labels:  # Check for common labels
                    print(f"Match found: {lost_item.name} and {found_item.name}")
                    matches.append((lost_item, found_item))
    print(f"Total matches found: {len(matches)}")
    return matches