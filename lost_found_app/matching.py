from .models import LostItem, FoundItem, ItemMatch

def calculate_match_score(lost_labels, found_labels):
    lost_set = set(lost_labels)
    found_set = set(found_labels)
    common_labels = lost_set.intersection(found_set)
    return len(common_labels) / max(len(lost_set), len(found_set))

def find_matches_for_item(item, is_found=False):
    matches = []
    # Parse vision labels
    if not item.vision_labels:
        return matches
    item_labels = set(label.split('(')[0].strip() for label in item.vision_labels.split(','))
    
    # Get items to compare against
    user = item.user
    if is_found:
        compare_items = LostItem.objects.filter(user=user)
        current_item = item
    else:
        compare_items = FoundItem.objects.filter(user=user)
        current_item = item
        
    # Find matches
    for compare_item in compare_items:
        if not compare_item.vision_labels:
            continue
        compare_labels = set(label.split('(')[0].strip() 
                           for label in compare_item.vision_labels.split(','))
        
        match_score = calculate_match_score(item_labels, compare_labels)
        
        # If match score > threshold, create match
        if match_score > 0.3:  # Adjust threshold as needed
            if is_found:
                match, created = ItemMatch.objects.get_or_create(
                    lost_item=compare_item,
                    found_item=current_item,
                    defaults={'match_score': match_score}
                )
            else:
                match, created = ItemMatch.objects.get_or_create(
                    lost_item=current_item, 
                    found_item=compare_item,
                    defaults={'match_score': match_score}
                )
            matches.append((compare_item, current_item))
    return matches