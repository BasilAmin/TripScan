# algorithm entirely made by ChatGPT

# Sample data for destinations
destination_data = [
    {
        "city": "Barcelona",
        "tags": {
            "Hiking": 4.5,
            "Food": 5.0,
            "Nightclubs": 4.0,
            "Culture": 5.0
        }
    },
    {
        "city": "Amsterdam",
        "tags": {
            "Food": 4.5,
            "Nightclubs": 5.0,
            "Culture": 4.0,
            "Outdoors": 3.5
        }
    },
    {
        "city": "Tokyo",
        "tags": {
            "Food": 5.0,
            "Culture": 5.0,
            "Nightclubs": 4.5,
            "Hiking": 3.0
        }
    },
    {
        "city": "Reykjavik",
        "tags": {
            "Hiking": 5.0,
            "Outdoors": 4.5,
            "Culture": 3.5
        }
    }
]

def aggregate_preferences(group_preferences):
    """
    Aggregate the preferences of the group to calculate average weights for each tag.
    """
    aggregated = {}
    for preferences in group_preferences:
        for tag, weight in preferences.items():
            if tag not in aggregated:
                aggregated[tag] = []
            aggregated[tag].append(weight)

    # Calculate average weights
    average_weights = {tag: sum(weights) / len(weights) for tag, weights in aggregated.items()}
    return average_weights

def find_best_destinations(group_preferences, destination_data, top_n=3):
    """
    Find the best destinations based on group preferences and destination data.
    """
    # Step 1: Aggregate group preferences
    aggregated_preferences = aggregate_preferences(group_preferences)
    
    # Step 2: Calculate scores for each destination
    destination_scores = {}

    for destination in destination_data:
        score = 0
        matching_tags_count = 0
        
        for tag, weight in aggregated_preferences.items():
            if tag in destination['tags']:
                score += weight * destination['tags'][tag]
                matching_tags_count += 1
        
        # Normalize score by the number of matching tags
        if matching_tags_count > 0:
            score /= matching_tags_count
        
        destination_scores[destination['city']] = score

    # Step 3: Sort destinations by score
    sorted_destinations = sorted(destination_scores.items(), key=lambda x: x[1], reverse=True)
    
    # Return top N destinations
    return sorted_destinations[:top_n]

# Example usage
if __name__ == "__main__":
    # Sample group preferences
    group_preferences = [
        {"Food": 5, "Hiking": 3, "Nightclubs": 4},
        {"Food": 4, "Culture": 5, "Nightclubs": 5},
        {"Hiking": 4, "Outdoors": 3, "Culture": 4}
    ]

    # Find the best destinations for the group
    best_destinations = find_best_destinations(group_preferences, destination_data, top_n=3)

    # Print the results
    print("Top Destinations for the Group Trip:")
    for city, score in best_destinations:
        print(f"{city}: Score = {score:.2f}")
