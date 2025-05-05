import json
from faker import Faker
import random

fake = Faker()

def generate_scenario():
    # Generate random date conflicts
    months = ["January", "February", "March", "April", "May", "June", 
              "July", "August", "September", "October", "November", "December"]
    constraints = [
        "work schedule", "school holidays", "family events", 
        "budget constraints", "weather preferences", "flight prices"
    ]
    
    # Create 2-4 users with conflicting dates
    num_users = random.randint(2, 4)
    users = []
    base_month = random.choice(months)
    
    for i in range(num_users):
        offset = random.randint(0, 3)
        start_day = random.randint(1, 15)
        end_day = start_day + random.randint(3, 10)
        users.append({
            "name": fake.first_name(),
            "dates": f"{base_month} {start_day + offset}-{end_day + offset}",
            "constraint": random.choice(constraints)
        })
    
    # Generate conversation
    conversation = "\n".join(
        [f"{user['name']}: I can only travel {user['dates']} ({user['constraint']})." 
         for user in users]
    )
    
    # Generate AI compromise (simplified)
    overlap = f"{base_month} {max(int(u['dates'].split()[1].split('-')[0]) for u in users)}-{min(int(u['dates'].split()[1].split('-')[1]) for u in users)}"
    options = [
        overlap + " (overlapping dates)",
        f"Split trip: {base_month} {random.randint(1, 10)}-15 and {random.randint(16, 28)}-30",
        "Alternative month: " + random.choice([m for m in months if m != base_month])
    ]
    
    return {
        "input": conversation,
        "output": "Compromise options: 1) " + " 2) ".join(options)
    }

# Generate 1000 scenarios
with open("travel_negotiation_dataset.jsonl", "w") as f:
    for _ in range(1000):
        f.write(json.dumps(generate_scenario()) + "\n")