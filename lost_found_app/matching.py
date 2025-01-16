# from .models import LostItem, FoundItem

# def find_matches():
#     matches = []
#     lost_items = LostItem.objects.all()
#     found_items = FoundItem.objects.all()
#     for lost_item in lost_items:
#         for found_item in found_items:
#             if lost_item.vision_labels and found_item.vision_labels:
#                 lost_labels = set(lost_item.vision_labels.split(', '))
#                 found_labels = set(found_item.vision_labels.split(', '))
#                 print(f"Comparing lost item {lost_item.name} with found item {found_item.name}")
#                 print(f"Lost labels: {lost_labels}")
#                 print(f"Found labels: {found_labels}")
#                 if lost_labels & found_labels:  # Check for common labels
#                     print(f"Match found: {lost_item.name} and {found_item.name}")
#                     matches.append((lost_item, found_item))
#     print(f"Total matches found: {len(matches)}")
#     return matches

from .models import LostItem, FoundItem, ItemMatch
import json


def calculate_match_score(lost_labels, found_labels):
    lost_set = set(lost_labels)
    found_set = set(found_labels)
    common_labels = lost_set.intersection(found_set)
    return len(common_labels) / max(len(lost_set), len(found_set))

def find_matches_for_item(item, is_found=False):
    # Parse vision labels
    if not item.vision_labels:
        return
    item_labels = set(label.split('(')[0].strip() for label in item.vision_labels.split(','))
    
    # Get items to compare against
    if is_found:
        compare_items = LostItem.objects.all()
        current_item = item
    else:
        compare_items = FoundItem.objects.all()
        current_item = item
        
    # Find matches
    for compare_item in compare_items:
        if not compare_item.vision_labels:
            continue
        compare_labels = set(label.split('(')[0].strip() 
                           for label in compare_item.vision_labels.split(','))
        
        match_score = calculate_match_score(item_labels, compare_labels)
        
        # If match score > threshold, create match
        if match_score > 0.1:  # Adjust threshold as needed
            if is_found:
                ItemMatch.objects.get_or_create(
                    lost_item=compare_item,
                    found_item=current_item,
                    defaults={'match_score': match_score}
                )
            else:
                ItemMatch.objects.get_or_create(
                    lost_item=current_item, 
                    found_item=compare_item,
                    defaults={'match_score': match_score}
                )