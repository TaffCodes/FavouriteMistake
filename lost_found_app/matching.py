from .models import LostItem, FoundItem, ItemMatch 

def parse_vision_labels(vision_response):
    """
    Parses vision labels and extracts their confidence scores.
    """
    label_score = {}
    for part in vision_response.split(','):
        part = part.strip()
        if '(' in part and ')' in part:
            label, score_str = part.split('(')
            score = float(score_str.rstrip(')'))
            label_score[label.strip().lower()] = score
        else:
            label_score[part.lower()] = 1.0  # Default score if missing
    return label_score

def calculate_weighted_label_score(lost_labels_str, found_labels_str):
    lost_labels = parse_vision_labels(lost_labels_str)
    found_labels = parse_vision_labels(found_labels_str)
    
    common_score = 0.0
    total_possible = 0.0
    for label, lost_score in lost_labels.items():
        if label in found_labels:
            found_score = found_labels[label]
            common_score += min(lost_score, found_score)
        total_possible += lost_score  # Using lost item's total as a baseline
    
    return common_score / total_possible if total_possible > 0 else 0.0

# def find_matches_for_item(item, is_found=False):
#     matches = []
#     if not item.vision_labels:
#         return matches
    
#     # Get items to compare against
#     compare_items = LostItem.objects.all() if is_found else FoundItem.objects.all()
    
#     for compare_item in compare_items:
#         if not compare_item.vision_labels:
#             continue
        
#         # Use weighted label score from Cloud Vision
#         match_score = calculate_weighted_label_score(item.vision_labels, compare_item.vision_labels)
        
#         # Adjust threshold based on experimental tuning
#         if match_score > 0.65:
#             if is_found:
#                 match, created = ItemMatch.objects.get_or_create(
#                     lost_item=compare_item,
#                     found_item=item,
#                     defaults={'match_score': match_score}
#                 )
#             else:
#                 match, created = ItemMatch.objects.get_or_create(
#                     lost_item=item,
#                     found_item=compare_item,
#                     defaults={'match_score': match_score}
#                 )
#             matches.append((compare_item, item))
#     return matches

def find_matches_for_item(item, is_found=False):
    matches = []
    if not item.vision_labels:
        return matches
    
    # Get items to compare against, excluding rejected matches
    compare_items = LostItem.objects.exclude(
        itemmatch__status="rejected"
    ) if is_found else FoundItem.objects.exclude(
        itemmatch__status="rejected"
    )
    
    for compare_item in compare_items:
        if not compare_item.vision_labels:
            continue
        
        match_score = calculate_weighted_label_score(item.vision_labels, compare_item.vision_labels)
        
        # Adjust threshold based on experimental tuning
        if match_score > 0.65:
            match, created = ItemMatch.objects.get_or_create(
                lost_item=compare_item if is_found else item,
                found_item=item if is_found else compare_item,
                defaults={'match_score': match_score}
            )
            # Skip already accepted matches
            if not created and match.status == "accepted":
                continue  
            matches.append((compare_item, item))
    return matches

