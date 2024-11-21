import queue
from datetime import datetime
import csv
import requests

# Use the raw URL of the Markdown file
url = "https://raw.githubusercontent.com/Flystar1-tech/ReadMe/refs/heads/main/README.md"

try:
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for bad status codes
    md_content = response.text
    print("Markdown content retrieved successfully:")
    print(md_content)
except requests.exceptions.RequestException as e:
    print(f"Failed to fetch the file: {e}")


class TicketSalesSystem:
    def __init__(self):
        # Data structures
        self.user_data = {}
        self.vip_queue = queue.Queue()
        self.regular_queue = queue.Queue()

        # Ticket availability
        self.vip_tickets_available = 10
        self.regular_tickets_available = 20

        # Transaction log file
        self.transaction_log_file = "transactions.csv"
        self.initialize_log()

    # Team Member 1: User Registration & Ticket Queue Management
    def register_user(self):
        print(f'Hello, welcome to Ticket Sales!')
        print('To begin, please continue on the screen on your right.')

        while True:  # Loop until valid input is received
            try:
                user_name = input('Name:\n').title().strip()
                if not user_name:
                    print("Please enter a valid name")
                    continue
                number_tickets = int(input('How many tickets would you like to purchase?\n'))
                if number_tickets <= 0:
                    print("Please enter a valid number of tickets.")
                    continue
            except ValueError:
                print("Invalid input. Please enter a valid number of tickets.")
                continue

            ticket_type = input('Are you purchasing a VIP or Regular ticket? Enter "V" for VIP and "R" for Regular:\n').upper()
            registration_time = datetime.now().strftime("%m-%d-%Y %H:%M:%S")

            if ticket_type == 'V':
                if self.vip_tickets_available >= number_tickets:
                    self.user_data[user_name] = {'ticket_type': 'VIP', 'time': registration_time, 'quantity': number_tickets}
                    for _ in range(number_tickets):
                        self.vip_queue.put(user_name)
                    self.vip_tickets_available -= number_tickets
                    print(f'Thank you for purchasing {number_tickets} VIP ticket(s). You have been added to the VIP queue!')
                    break
                else:
                    print(f"Only {self.vip_tickets_available} VIP tickets are available. Please try again.")
                    self.log_transaction(user_name, success=False, reason="Not enough VIP tickets available")
            elif ticket_type == 'R':
                if self.regular_tickets_available >= number_tickets:
                    self.user_data[user_name] = {'ticket_type': 'Regular', 'time': registration_time, 'quantity': number_tickets}
                    for _ in range(number_tickets):
                        self.regular_queue.put(user_name)
                    self.regular_tickets_available -= number_tickets
                    print(f'Thank you for purchasing {number_tickets} Regular ticket(s). You have been added to the Regular queue!')
                    break
                else:
                    print(f"Only {self.regular_tickets_available} Regular tickets are available. Please try again.")
                    self.log_transaction(user_name, success=False, reason="Not enough Regular tickets available")
            else:
                print('Invalid ticket type. Please try again!')

    def display_queues(self):
        print('----- Current Queue -------')
        print('VIP Queue:')
        queue_vip = list(self.vip_queue.queue)
        for user in queue_vip:
            user_info = self.user_data[user]
            print(f"{user} (Ticket Type: {user_info['ticket_type']}, Quantity: {user_info['quantity']}, Registered At: {user_info['time']})")

        print("\nRegular Queue:")
        queue_regular = list(self.regular_queue.queue)
        for user in queue_regular:
            user_info = self.user_data[user]
            print(f"{user} (Ticket Type: {user_info['ticket_type']}, Quantity: {user_info['quantity']}, Registered At: {user_info['time']})")

    # Team Member 2: Ticket Processing, Availability Tracking & Real-Time Feedback
    def process_tickets(self, number_tickets):
        print("\n----- Processing Tickets -----")
        tickets_processed = 0

        # Process VIP tickets first
        while not self.vip_queue.empty() and tickets_processed < number_tickets:
            user = self.vip_queue.get()
            user_info = self.user_data[user]
            print(f"Processed VIP Ticket for {user} (Registered At: {user_info['time']})")
            self.log_transaction(user, success=True)
            tickets_processed += 1
            user_info['quantity'] -= 1
            if user_info['quantity'] == 0:
                del self.user_data[user]

        # Process Regular tickets
        while not self.regular_queue.empty() and tickets_processed < number_tickets:
            user = self.regular_queue.get()
            user_info = self.user_data[user]
            print(f"Processed Regular Ticket for {user} (Registered At: {user_info['time']})")
            self.log_transaction(user, success=True)
            tickets_processed += 1
            user_info['quantity'] -= 1
            if user_info['quantity'] == 0:
                del self.user_data[user]

        if tickets_processed == 0:
            print("No tickets available to process.")
        else:
            print(f"Processed {tickets_processed} tickets.")

    # Team Member 3: Transaction Logging, Interface & Additional Tasks
    def initialize_log(self):
        with open(self.transaction_log_file, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["User Name", "Ticket Type", "Time of Request", "Status", "Reason"])

    def log_transaction(self, user_name, success, reason=None):
        with open(self.transaction_log_file, "a", newline="") as file:
            writer = csv.writer(file)
            if success:
                writer.writerow([user_name, self.user_data[user_name]['ticket_type'], self.user_data[user_name]['time'], "Success", ""])
            else:
                writer.writerow([user_name, "N/A", datetime.now().strftime("%m-%d-%Y %H:%M:%S"), "Failure", reason])

    def summary(self):
        print("\n----- Ticket Sales Summary -----")
        print(f"VIP Tickets Sold: {10 - self.vip_tickets_available}")
        print(f"Regular Tickets Sold: {20 - self.regular_tickets_available}")
        print(f"VIP Tickets Remaining: {self.vip_tickets_available}")
        print(f"Regular Tickets Remaining: {self.regular_tickets_available}")

    def cancel_ticket(self):
        """Allow users to cancel specific quantities of tickets."""
        user_name = input("Enter your name to cancel tickets: ").title().strip()  # Ask for the user's name

        # Check if the user exists in the pending tickets
        if user_name in self.user_data:
            ticket_type = self.user_data[user_name]['ticket_type']
            total_quantity = self.user_data[user_name]['quantity']

            # Ask how many tickets the user wants to cancel
            try:
                cancel_quantity = int(
                    input(f"You have {total_quantity} {ticket_type} tickets. How many would you like to cancel? "))
                if cancel_quantity <= 0 or cancel_quantity > total_quantity:
                    print("Invalid quantity. Please enter a valid number.")
                    return
            except ValueError:
                print("Invalid input. Please enter a number.")
                return

            # Update ticket availability
            if ticket_type == "VIP":
                self.vip_tickets_available += cancel_quantity
                # Filter the VIP queue to remove the specified number of tickets
                filtered_vip_queue = queue.Queue()
                removed = 0
                while not self.vip_queue.empty():
                    current_user = self.vip_queue.get()
                    if current_user == user_name and removed < cancel_quantity:
                        removed += 1
                    else:
                        filtered_vip_queue.put(current_user)
                self.vip_queue = filtered_vip_queue
            elif ticket_type == "Regular":
                self.regular_tickets_available += cancel_quantity
                # Filter the Regular queue to remove the specified number of tickets
                filtered_regular_queue = queue.Queue()
                removed = 0
                while not self.regular_queue.empty():
                    current_user = self.regular_queue.get()
                    if current_user == user_name and removed < cancel_quantity:
                        removed += 1
                    else:
                        filtered_regular_queue.put(current_user)
                self.regular_queue = filtered_regular_queue

            # Update or remove the user's record
            remaining_tickets = total_quantity - cancel_quantity
            if remaining_tickets > 0:
                self.user_data[user_name]['quantity'] = remaining_tickets
                print(
                    f"{cancel_quantity} {ticket_type} ticket(s) have been canceled. You still have {remaining_tickets} ticket(s).")
            else:
                del self.user_data[user_name]
                print(f"All {ticket_type} ticket(s) for {user_name} have been canceled.")

        # If the user is not found at all
        else:
            print("No ticket found for this user.")

    # User-friendly menu system
    def menu(self):
        while True:
            print("\n--- Ticket System Menu ---")
            print("1. Register for Tickets")
            print("2. Display Queues")
            print("3. Process Tickets")
            print("4. Cancel Ticket")
            print("5. Display Ticket Sales Summary")
            print("6. Exit")
            choice = input("Enter your choice:\n")

            if choice == "1":
                self.register_user()
            elif choice == "2":
                self.display_queues()
            elif choice == "3":
                try:
                    number_tickets = int(input("Enter the number of tickets to process:\n"))
                    self.process_tickets(number_tickets)
                except ValueError:
                    print("Invalid input. Please enter a valid number.")
            elif choice == "4":
                self.cancel_ticket()
            elif choice == "5":
                self.summary()
            elif choice == "6":
                print("Exiting the system. Goodbye!")
                break
            else:
                print("Invalid choice. Please select a valid option.")


# Main Program
if __name__ == "__main__":
    ticket_system = TicketSalesSystem()
    ticket_system.menu()
