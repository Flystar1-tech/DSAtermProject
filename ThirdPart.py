import csv
import queue
from datetime import datetime
# Team Member 3: Transaction Logging, Interface & Additional Tasks


def initialize_log(self):
    with open(self.transaction_log_file, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["User Name", "Ticket Type", "Time of Request", "Status", "Reason"])


def log_transaction(self, user_name, success, reason=None):
    with open(self.transaction_log_file, "a", newline="") as file:
        writer = csv.writer(file)
        if success:
            writer.writerow(
                [user_name, self.user_data[user_name]['ticket_type'], self.user_data[user_name]['time'], "Success", ""])
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

