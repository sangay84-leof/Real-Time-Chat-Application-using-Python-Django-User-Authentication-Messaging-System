class CircularQueue:
    """
    A Circular Queue implementation for the Chat Application.
    It has a fixed size and overwrites the oldest message when full.
    """
    def __init__(self, capacity):
        self.capacity = capacity
        self.queue = [None] * capacity
        self.front = 0
        self.rear = -1
        self.size = 0

    def enqueue(self, message):
        """
        Add a message to the queue.
        If the queue is full, it overwrites the oldest message.
        """
        if self.is_full():
            # If full, move front to overwrite the oldest message
            self.front = (self.front + 1) % self.capacity
            self.size -= 1  # Decrease size temporarily as we are about to overwrite
        
        self.rear = (self.rear + 1) % self.capacity
        self.queue[self.rear] = message
        self.size += 1
        print(f"Message sent: '{message}'")

    def dequeue(self):
        """
        Remove the oldest message from the queue.
        """
        if self.is_empty():
            print("Chat history is empty.")
            return None
        
        removed_message = self.queue[self.front]
        self.front = (self.front + 1) % self.capacity
        self.size -= 1
        print(f"Deleted oldest message: '{removed_message}'")
        return removed_message

    def is_full(self):
        """Check if the queue is full."""
        return self.size == self.capacity

    def is_empty(self):
        """Check if the queue is empty."""
        return self.size == 0

    def display(self):
        """
        Display all messages in the correct order (from oldest to newest).
        """
        if self.is_empty():
            print("Chat history is empty.")
            return

        print("\n--- Chat History ---")
        # Start from front and iterate 'size' times
        idx = self.front
        for i in range(self.size):
            print(f"{i + 1}. {self.queue[idx]}")
            idx = (idx + 1) % self.capacity
        print("--------------------\n")


def main():
    # Chat History size of 5
    chat_queue = CircularQueue(5)

    while True:
        print("\n=== Chat Application Menu ===")
        print("1. Send a message")
        print("2. View chat history")
        print("3. Delete oldest message")
        print("4. Exit")
        
        choice = input("Enter your choice (1-4): ")

        if choice == '1':
            msg = input("Enter message: ")
            chat_queue.enqueue(msg)
        elif choice == '2':
            chat_queue.display()
        elif choice == '3':
            chat_queue.dequeue()
        elif choice == '4':
            print("Exiting Chat Application. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")

if __name__ == "__main__":
    main()
