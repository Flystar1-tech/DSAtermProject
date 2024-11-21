# Ticket Sales System

A Python-based ticket management system for events that supports VIP and Regular tickets. This system provides functionalities for user registration, ticket processing, queue management, cancellation of tickets, real-time sales summaries, and transaction logging.

---

## **Features**

### 1. User Registration
- Users can register for **VIP** or **Regular** tickets.
- Registration checks ticket availability.
- Adds users to the appropriate queue based on ticket type.

### 2. Queue Management
- Maintains separate queues for VIP and Regular tickets.
- Ensures **VIP tickets are prioritized** during processing.

### 3. Ticket Processing
- Processes tickets based on priority (VIP first).
- Updates sold tickets and logs each transaction.

### 4. Ticket Cancellation
- Allows users to cancel all or part of their tickets.
- Frees up canceled tickets for other users.

### 5. Sales Summary
- Displays the number of tickets sold and remaining for each type.

### 6. Transaction Logging
- Logs all events (registration, processing, cancellation) to a CSV file.

### 7. Interactive Menu
- User-friendly, text-based interface for easy navigation.

---

## **Menu Options**
1. **Register for Tickets**: Register for VIP or Regular tickets.
2. **Display Queues**: View the current status of the VIP and Regular ticket queues.
3. **Process Tickets**: Process tickets in order of priority.
4. **Cancel Tickets**: Cancel a specific number of tickets.
5. **Display Sales Summary**: View real-time ticket sales and availability.
6. **Exit**: Exit the program.

---

## **Classes and Methods**

### **`TicketSalesSystem` Class**
Handles the core functionalities of the ticketing system.

#### **Key Methods**
1. **`__init__`**:
   - Initializes data structures, queues, and ticket availability.
   - Sets up the transaction log file.

2. **`register_user()`**:
   - Registers users for tickets after validating input and checking availability.

3. **`process_tickets(number_tickets)`**:
   - Processes tickets in priority order.
   - Updates queues and logs processed tickets.

4. **`cancel_ticket()`**:
   - Allows users to cancel specific quantities of tickets.

5. **`display_queues()`**:
   - Displays the current VIP and Regular ticket queues.

6. **`summary()`**:
   - Provides a summary of ticket sales and availability.

7. **`log_transaction(user_name, success, reason)`**:
   - Logs all actions to a CSV file for tracking.

8. **`menu()`**:
   - Interactive menu for accessing the system’s functionalities.

---

## **Transaction Logging**
- Transactions are logged in a file named `transactions.csv`.
- Logged fields include:
  - **User Name**
  - **Ticket Type**
  - **Status** (e.g., Success, Failed, Canceled)
  - **Timestamp**

---

## **Usage Instructions**

### **1. Run the Program**

python ticket_sales_system.py


# Future Enhancements

## 1. Dynamic Ticket Limits
- Allow administrators to configure ticket availability dynamically.
- Provide an interactive interface for modifying ticket limits without restarting the system.

## 2. Enhanced Error Handling
- Implement robust error logs for better debugging.
- Gracefully handle invalid inputs and unexpected exceptions.

## 3. Web-Based Interface
- Transition from the current console-based system to a user-friendly web-based dashboard.
- Include features like real-time queue management, ticket processing, and cancellation through a graphical interface.

---

# Dependencies

## Python Version
- **Python 3.7+**

## Required Libraries
- **queue**
- **datetime**
- **csv**
