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
                if lost_labels & found_labels:  # Check for common labels
                    matches.append((lost_item, found_item))
    return matches