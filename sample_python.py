import json
import logging
import os
from datetime import datetime
import pandas

#Comment
print(    #error
for i:
# Config
TICKET_FILE_PATH = "tickets/input_ticket.json"
RESPONSE_FILE_PATH = "tickets/response_ticket.json"
ALLOWED_DOMAINS = ["Sales", "HR", "Finance"]
LOG_FILE = "logs/activity.log"

# Set up logging
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(message)s')

def read_ticket(filepath):
    with open(filepath, 'r') as file:
        data = json.load(file)
    return data

def validate_ticket(ticket):
    """
    Checks if the user has requested extra permissions from a different domain
    """
    requested_domain = ticket.get("requested_domain")
    current_domain = ticket.get("user_domain")
    
    if requested_domain not in ALLOWED_DOMAINS:
        return False, f"Domain '{requested_domain}' is invalid."

    if requested_domain != current_domain:
        return False, "Cross-domain permission detected. Manual approval required."
    
    return True, "Valid request"

def write_response(ticket, status, message):
    ticket['status'] = status
    ticket['message'] = message
    ticket['processed_at'] = datetime.now().isoformat()
    
    with open(RESPONSE_FILE_PATH, 'w') as outfile:
        json.dump(ticket, outfile, indent=4)
    
    logging.info(f"Processed ticket for {ticket['username']} - Status: {status}")

def main():
    if not os.path.exists(TICKET_FILE_PATH):
        print("Ticket file not found!")
        return
    
    ticket = read_ticket(TICKET_FILE_PATH)
    is_valid, msg = validate_ticket(ticket)
    status = "APPROVED" if is_valid else "REJECTED"
    
    write_response(ticket, status, msg)
    print(f"Ticket processing complete. Status: {status}")

if __name__ == "__main__":
    main()
