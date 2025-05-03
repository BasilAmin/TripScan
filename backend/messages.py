import csv
import os
from typing import List, Dict
from datetime import datetime
import pandas as pd
from .models import *

def save_message_to_csv(user_id: str, content: str, file_path: str = "messages.csv") -> int:
    """Saves a message to a CSV file and returns the message_id, which is the row number.

    Args:
        user_id (str): The ID of the user sending the message.
        content (str): The content of the message.
        file_path (str): The path to the CSV file. Defaults to "messages.csv".

    Returns:
        int: The message_id, which corresponds to the row number where the message was added.
    """
    # Calculate the message_id based on the number of rows already in the file (row count)
    message_id = 1
    if os.path.exists(file_path):
        with open(file_path, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            # Skip header row if it exists
            next(reader, None)
            message_id = sum(1 for row in reader) + 1  # Increment row count for new message_id

    # Get the current timestamp
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Format the timestamp

    # Open the CSV file in append mode
    with open(file_path, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        
        # Write the header if the file is empty
        if f.tell() == 0:
            writer.writerow(["message_id", "user_id", "content", "timestamp"])  # Write header
        
        # Write the message as a new row, including timestamp
        writer.writerow([message_id, user_id, content, timestamp])  # Write message with timestamp

    return message_id

def read_messages_from_csv(file_path: str = "messages.csv") -> List[Dict[str, str]]:
    """Reads messages from a CSV file and returns them as a list of dictionaries.

    Args:
        file_path (str): The path to the CSV file. Defaults to "messages.csv".

    Returns:
        List[Dict[str, str]]: A list of messages, where each message is represented as a dictionary.
    """
    messages = []

    # Check if the file exists before attempting to read
    if not os.path.exists(file_path):
        # If the file doesn't exist, return an empty list
        return messages
    
    # Open the CSV file for reading
    with open(file_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)  # Use DictReader to read rows as dictionaries
        for row in reader:
            messages.append(row)  # Append each row (message) to the list

    return messages


def load_trip_data_from_csv(file_path: str) -> list[TripData]:
    """Loads trip data from a CSV file and returns a list of TripData instances.

    Args:
        file_path (str): The path to the CSV file containing trip data.

    Returns:
        list[TripData]: A list of TripData instances.
    """
    trips = []
    try:
        df = pd.read_csv(file_path)
        for index, row in df.iterrows():
            trip = TripData(
                user_id=row['user_id'],
                origin_city=row['origin_city'],
                start_date=row['start_date'],
                end_date=row['end_date']
            )
            trips.append(trip)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"An error occurred while loading trip data: {e}")

    return trips


def get_llm_formatted_chat(messages_file: str) -> str:
    """Endpoint to send messages and trip data to the LLM.

    Args:
        messages_file (str): The path to the CSV file containing messages.

    Returns:
        str: Formatted input string for the LLM.
    """
    # Read messages and trip data
    messages = read_messages_from_csv(messages_file)

    # Send the formatted data to the LLM API
    formatted_chat_data = "\n".join(f"{msg['user_id']}: {msg['content']}" for msg in messages)
    
    # Format trip information for each trip
    final_data = f"\n\nChat Data:\n{formatted_chat_data}"
    return final_data

def get_llm_formatted_date(trips_file: str) -> str:
    """Endpoint to send messages and trip data to the LLM.

    Args:
        trips_file (str): The path to the CSV file containing trip data.

    Returns:
        str: Formatted input string for the LLM.
    """
    # Read trip data
    trips = load_trip_data_from_csv(trips_file)

    # Format trip information for each trip
    trip_info_strings = [
        f"Trip Information:\nOrigin City: {trip.origin_city}\nStart Date: {trip.start_date}\nEnd Date: {trip.end_date}"
        for trip in trips
    ]
    final_data = "\n\n".join(trip_info_strings) 

    return final_data

def save_trip_data_to_csv(user_id: str, origin_city: str, start_date: str, end_date: str, file_path: str = "trips.csv"):
    """Saves or updates trip data for a user in a CSV file."""
    updated = False
    rows = []

    # If the file exists, read current rows
    if os.path.exists(file_path):
        with open(file_path, mode='r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["user_id"] == user_id:
                    row = {
                        "user_id": user_id,
                        "origin_city": origin_city,
                        "start_date": start_date,
                        "end_date": end_date
                    }
                    updated = True
                rows.append(row)

    # If not updated, it's a new entry
    if not updated:
        rows.append({
            "user_id": user_id,
            "origin_city": origin_city,
            "start_date": start_date,
            "end_date": end_date
        })

    # Write everything back to the file
    with open(file_path, mode='w', newline='', encoding='utf-8') as f:
        fieldnames = ["user_id", "origin_city", "start_date", "end_date"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

# Example usage
if __name__ == "__main__":
    # Generate sample trips.csv
    sample_trips = [
        ("NYC", "2023-10-01", "2023-10-10"),
        ("LAX", "2023-11-01", "2023-11-05"),
        ("ORD", "2023-12-15", "2023-12-20")
    ]
    
    for origin_city, start_date, end_date in sample_trips:
        save_trip_data_to_csv(origin_city, start_date, end_date)

    # Generate sample messages.csv
    sample_messages = [
        ("User1", "I love hiking and exploring nature."),
        ("User2", "I prefer relaxing on the beach and enjoying the sun."),
        ("User3", "What are the best hiking trails near NYC?")
    ]
    
    for user_id, content in sample_messages:
        save_message_to_csv(user_id, content)

    # Get formatted input for the LLM
    formatted_input = get_llm_formatted_chat('messages.csv')
    
    # Print the formatted input
    print(formatted_input)
