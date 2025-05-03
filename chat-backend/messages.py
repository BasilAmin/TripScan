import csv
import os
from typing import List, Dict
from datetime import datetime

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
    
    # Open the CSV file for reading
    with open(file_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)  # Use DictReader to read rows as dictionaries
        for row in reader:
            messages.append(row)  # Append each row (message) to the list

    return messages

# Example usage
if __name__ == "__main__":
    # Read all messages from the CSV file
    messages = read_messages_from_csv()
    for message in messages:
        print(message)
