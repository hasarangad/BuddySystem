import tkinter as tk
from tkinter import messagebox


# BuddySystem class manages memory allocation and deallocation using the buddy system algorithm
class BuddySystem:
    def __init__(self, total_memory):

        self.total_memory = total_memory  # Total memory available
        self.free_list = {total_memory: [0]}  # Dictionary to track free blocks by size

    def allocate(self, size):

        block_size = self._next_power_of_two(size)  # Find the smallest power of two >= size

        # Iterate over free blocks to find a suitable block
        for b_size in sorted(self.free_list.keys()):
            if b_size >= block_size and self.free_list[b_size]:
                start_address = self.free_list[b_size].pop(0)  # Allocate the block
                if not self.free_list[b_size]:
                    del self.free_list[b_size]  # Remove empty lists

                # Split blocks until the desired size is reached
                while b_size > block_size:
                    b_size //= 2
                    self.free_list.setdefault(b_size, []).append(start_address + b_size)

                return start_address

        return None  # Allocation failed

    def free(self, address, size):

        block_size = self._next_power_of_two(size)
        buddy_address = address ^ block_size  # Compute buddy address

        # Merge blocks with their buddies if possible
        while block_size < self.total_memory:
            if buddy_address in self.free_list.get(block_size, []):
                self.free_list[block_size].remove(buddy_address)
                if not self.free_list[block_size]:
                    del self.free_list[block_size]

                address = min(address, buddy_address)
                block_size *= 2
                buddy_address = address ^ block_size
            else:
                break

        self.free_list.setdefault(block_size, []).append(address)  # Add the block back to the free list

    def _next_power_of_two(self, n):

        if n == 0:
            return 1
        power = 1
        while power < n:
            power *= 2
        return power

    def display_memory(self):

        state = ""
        for size, blocks in sorted(self.free_list.items()):
            state += f"Block size {size}: {blocks}\n"
        return state


# BuddySystemApp class creates the GUI for interacting with the buddy system
class BuddySystemApp:
    def __init__(self, root):

        self.buddy_system = BuddySystem(1024)  # Initialize with 1024 bytes
        self.root = root
        self.root.title("Buddy System Simulator")

        # Memory State Display
        self.memory_state_label = tk.Label(root, text="Memory State:")
        self.memory_state_label.pack()

        self.memory_state_display = tk.Text(root, height=10, width=50, state=tk.DISABLED)
        self.memory_state_display.pack()

        # Allocate Memory Section
        self.allocate_label = tk.Label(root, text="Allocate Memory (bytes):")
        self.allocate_label.pack()

        self.allocate_entry = tk.Entry(root)
        self.allocate_entry.pack()

        self.allocate_button = tk.Button(root, text="Allocate", command=self.allocate_memory)
        self.allocate_button.pack()

        # Free Memory Section
        self.free_label = tk.Label(root, text="Free Memory (start address, size):")
        self.free_label.pack()

        self.free_entry = tk.Entry(root)
        self.free_entry.pack()

        self.free_button = tk.Button(root, text="Free", command=self.free_memory)
        self.free_button.pack()

        # Initialize memory state display
        self.update_memory_state()

    def update_memory_state(self):

        state = self.buddy_system.display_memory()
        self.memory_state_display.config(state=tk.NORMAL)
        self.memory_state_display.delete(1.0, tk.END)
        self.memory_state_display.insert(tk.END, state)
        self.memory_state_display.config(state=tk.DISABLED)

    def allocate_memory(self):

        try:
            size = int(self.allocate_entry.get())
            address = self.buddy_system.allocate(size)
            if address is not None:
                messagebox.showinfo("Allocation Successful", f"Allocated {size} bytes at address {address}.")
            else:
                messagebox.showwarning("Allocation Failed", "Not enough memory to allocate.")
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid integer size.")
        self.update_memory_state()

    def free_memory(self):

        try:
            input_text = self.free_entry.get()
            address, size = map(int, input_text.split(","))
            self.buddy_system.free(address, size)
            messagebox.showinfo("Free Successful", f"Freed {size} bytes starting at address {address}.")
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid address and size separated by a comma.")
        self.update_memory_state()


# Main program entry point
if __name__ == "__main__":
    root = tk.Tk()  # Create the main application window
    app = BuddySystemApp(root)  # Instantiate the BuddySystemApp
    root.mainloop()  # Start the Tkinter event loop
