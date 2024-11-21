import queue
from datetime import datetime
import csv


# Team Member 2: Ticket Processing, Availability Tracking & Real-Time Feedback

def process_tickets(self, number_tickets):
    """Process tickets based on priority (VIP first, then Regular), and provide real-time feedback."""
    print("\n----- Processing Tickets -----")
    tickets_processed = 0

    # Process VIP tickets first
    while not self.vip_queue.empty() and tickets_processed < number_tickets:
        user = self.vip_queue.get()
        user_info = self.user_data[user]

        # Process VIP ticket
        print(f"Processed VIP Ticket for {user} (Registered At: {user_info['time']})")
        self.log_transaction(user, success=True)  # Log the transaction
        tickets_processed += 1
        user_info['quantity'] -= 1

        # If all tickets for this user are processed, remove the user from the system
        if user_info['quantity'] == 0:
            del self.user_data[user]

    # Process Regular tickets next
    while not self.regular_queue.empty() and tickets_processed < number_tickets:
        user = self.regular_queue.get()
        user_info = self.user_data[user]

        # Process Regular ticket
        print(f"Processed Regular Ticket for {user} (Registered At: {user_info['time']})")
        self.log_transaction(user, success=True)  # Log the transaction
        tickets_processed += 1
        user_info['quantity'] -= 1

        # If all tickets for this user are processed, remove the user from the system
        if user_info['quantity'] == 0:
            del self.user_data[user]

    # Real-time feedback
    if tickets_processed == 0:
        print("No tickets available to process.")
    else:
        print(f"Processed {tickets_processed} tickets.")


def display_ticket_availability(self):
    """Provide real-time feedback on ticket availability."""
    print("\n----- Ticket Availability -----")
    print(f"VIP Tickets Remaining: {self.vip_tickets_available}")
    print(f"Regular Tickets Remaining: {self.regular_tickets_available}")
