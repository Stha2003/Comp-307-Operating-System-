import tkinter as tk
from tkinter import messagebox, simpledialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter.ttk as ttk

class MemoryManagement:
    def __init__(self, total_size):
        self.total_size = total_size
        self.memory = [None] * total_size
        self.processes = {}
        self.allocation_attempts = 0
        self.successful_allocations = 0
        self.algorithm_efficiency = {}

    def display_memory(self):
        memory_status = "Memory Allocation:\n"
        for i in range(self.total_size):
            if self.memory[i] is None:
                memory_status += f"[{i}]: Free\n"
            else:
                memory_status += f"[{i}]: Process {self.memory[i]}\n"
        return memory_status

    def visualize_memory(self):
        data = ['Free' if x is None else f'P{x}' for x in self.memory]
        fig, ax = plt.subplots(figsize=(10, 2))
        ax.bar(range(self.total_size), [1] * self.total_size, color=['blue' if x == 'Free' else 'red' for x in data])
        ax.set_yticks([])
        ax.grid(False)
        ax.spines['top'].set_visible(False)
        for i, txt in enumerate(range(self.total_size)):
            ax.text(i, 0, str(txt), ha='center', va='bottom', fontsize=7, color='black')
        return fig

    def calculate_fragmentation(self):
        free_blocks = 0
        free_size = 0
        for i in range(self.total_size):
            if self.memory[i] is None:
                free_blocks += 1
                if free_blocks > 1:
                    free_size += 1
                else:
                    free_size = 1
            else:
                free_blocks = 0

        fragmentation = 0
        if self.total_size > 0:
            fragmentation = (free_size / self.total_size) * 100

        return fragmentation

class FixedSizePartitioning(MemoryManagement):
    def __init__(self, total_size, partition_size):
        super().__init__(total_size)
        self.partition_size = partition_size
        self.partitions = [None] * (total_size // partition_size)

    def allocate(self, process_id, size, strategy='first_fit'):
        if size > self.partition_size:
            messagebox.showerror("Error", f"Process {process_id} requires more memory than partition size.")
            return False

        if strategy == 'first_fit':
            for i in range(len(self.partitions)):
                if self.partitions[i] is None:
                    self.partitions[i] = process_id
                    start = i * self.partition_size
                    end = start + size
                    for j in range(start, end):
                        self.memory[j] = process_id
                    if process_id in self.processes:
                        self.processes[process_id].append((start, end))
                    else:
                        self.processes[process_id] = [(start, end)]
                    return True
        elif strategy == 'best_fit':
            best_fit_index = -1
            best_fit_size = float('inf')
            for i in range(len(self.partitions)):
                if self.partitions[i] is None:
                    if self.partition_size - size < best_fit_size:
                        best_fit_size = self.partition_size - size
                        best_fit_index = i
            if best_fit_index != -1:
                self.partitions[best_fit_index] = process_id
                start = best_fit_index * self.partition_size
                end = start + size
                for j in range(start, end):
                    self.memory[j] = process_id
                if process_id in self.processes:
                    self.processes[process_id].append((start, end))
                else:
                    self.processes[process_id] = [(start, end)]
                return True
        elif strategy == 'next_fit':
            last_index = 0
            for i in range(last_index, len(self.partitions)):
                if self.partitions[i] is None:
                    self.partitions[i] = process_id
                    start = i * self.partition_size
                    end = start + size
                    for j in range(start, end):
                        self.memory[j] = process_id
                    if process_id in self.processes:
                        self.processes[process_id].append((start, end))
                    else:
                        self.processes[process_id] = [(start, end)]
                    last_index = i
                    return True
            for i in range(0, last_index):
                if self.partitions[i] is None:
                    self.partitions[i] = process_id
                    start = i * self.partition_size
                    end = start + size
                    for j in range(start, end):
                        self.memory[j] = process_id
                    if process_id in self.processes:
                        self.processes[process_id].append((start, end))
                    else:
                        self.processes[process_id] = [(start, end)]
                    last_index = i
                    return True

        messagebox.showerror("Error", f"Failed to allocate memory for Process {process_id}")
        return False

    def deallocate(self, process_id):
        if process_id in self.processes:
            allocations = self.processes.pop(process_id)
            for start, end in allocations:
                for j in range(start, end):
                    self.memory[j] = None
                partition_index = start // self.partition_size
                self.partitions[partition_index] = None
        else:
            messagebox.showerror("Error", f"Process {process_id} not found in memory.")

class UnequalSizePartitioning(MemoryManagement):
    def __init__(self, total_size, partition_sizes):
        super().__init__(total_size)
        self.partition_sizes = partition_sizes
        self.partitions = [None] * len(partition_sizes)
        self.partition_offsets = []
        offset = 0
        for size in partition_sizes:
            self.partition_offsets.append(offset)
            offset += size

    def allocate(self, process_id, size, strategy='first_fit'):
        if size > max(self.partition_sizes):
            messagebox.showerror("Error", f"Process {process_id} requires more memory than any partition size.")
            return False

        if strategy == 'first_fit':
            for i in range(len(self.partition_sizes)):
                if self.partitions[i] is None and size <= self.partition_sizes[i]:
                    self.partitions[i] = process_id
                    start = self.partition_offsets[i]
                    end = start + size
                    for j in range(start, end):
                        self.memory[j] = process_id
                    if process_id in self.processes:
                        self.processes[process_id].append((start, end))
                    else:
                        self.processes[process_id] = [(start, end)]
                    return True
        elif strategy == 'best_fit':
            best_fit_index = -1
            best_fit_size = float('inf')
            for i in range(len(self.partition_sizes)):
                if self.partitions[i] is None and self.partition_sizes[i] >= size:
                    if self.partition_sizes[i] - size < best_fit_size:
                        best_fit_size = self.partition_sizes[i] - size
                        best_fit_index = i
            if best_fit_index != -1:
                self.partitions[best_fit_index] = process_id
                start = self.partition_offsets[best_fit_index]
                end = start + size
                for j in range(start, end):
                    self.memory[j] = process_id
                if process_id in self.processes:
                    self.processes[process_id].append((start, end))
                else:
                    self.processes[process_id] = [(start, end)]
                return True
        elif strategy == 'next_fit':
            last_index = 0
            for i in range(last_index, len(self.partition_sizes)):
                if self.partitions[i] is None and size <= self.partition_sizes[i]:
                    self.partitions[i] = process_id
                    start = self.partition_offsets[i]
                    end = start + size
                    for j in range(start, end):
                        self.memory[j] = process_id
                    if process_id in self.processes:
                        self.processes[process_id].append((start, end))
                    else:
                        self.processes[process_id] = [(start, end)]
                    last_index = i
                    return True
            for i in range(0, last_index):
                if self.partitions[i] is None and size <= self.partition_sizes[i]:
                    self.partitions[i] = process_id
                    start = self.partition_offsets[i]
                    end = start + size
                    for j in range(start, end):
                        self.memory[j] = process_id
                    if process_id in self.processes:
                        self.processes[process_id].append((start, end))
                    else:
                        self.processes[process_id] = [(start, end)]
                    last_index = i
                    return True

        messagebox.showerror("Error", f"Failed to allocate memory for Process {process_id}")
        return False

    def deallocate(self, process_id):
        if process_id in self.processes:
            allocations = self.processes.pop(process_id)
            for start, end in allocations:
                for j in range(start, end):
                    self.memory[j] = None
                partition_index = next(i for i, offset in enumerate(self.partition_offsets) if offset == start)
                self.partitions[partition_index] = None
        else:
            messagebox.showerror("Error", f"Process {process_id} not found in memory.")

class DynamicPartitioning(MemoryManagement):
    def allocate(self, process_id, size, strategy='first_fit'):
        if strategy == 'first_fit':
            for i in range(self.total_size):
                if self.memory[i] is None:
                    if all(self.memory[j] is None for j in range(i, i + size)):
                        for j in range(i, i + size):
                            self.memory[j] = process_id
                        self.processes[process_id] = [(i, i + size)]
                        return True
        elif strategy == 'best_fit':
            best_fit_index = -1
            best_fit_size = float('inf')
            for i in range(self.total_size):
                if self.memory[i] is None:
                    free_block_size = 0
                    for j in range(i, self.total_size):
                        if self.memory[j] is None:
                            free_block_size += 1
                        else:
                            break
                    if free_block_size >= size and free_block_size < best_fit_size:
                        best_fit_size = free_block_size
                        best_fit_index = i
            if best_fit_index != -1:
                for j in range(best_fit_index, best_fit_index + size):
                    self.memory[j] = process_id
                self.processes[process_id] = [(best_fit_index, best_fit_index + size)]
                return True
        elif strategy == 'next_fit':
            last_index = 0
            for i in range(last_index, self.total_size):
                if self.memory[i] is None:
                    if all(self.memory[j] is None for j in range(i, i + size)):
                        for j in range(i, i + size):
                            self.memory[j] = process_id
                        self.processes[process_id] = [(i, i + size)]
                        last_index = i
                        return True
            for i in range(0, last_index):
                if self.memory[i] is None:
                    if all(self.memory[j] is None for j in range(i, i + size)):
                        for j in range(i, i + size):
                            self.memory[j] = process_id
                        self.processes[process_id] = [(i, i + size)]
                        last_index = i
                        return True

        messagebox.showerror("Error", f"Failed to allocate memory for Process {process_id}")
        return False

    def deallocate(self, process_id):
        if process_id in self.processes:
            allocations = self.processes.pop(process_id)
            for start, end in allocations:
                for j in range(start, end):
                    self.memory[j] = None
        else:
            messagebox.showerror("Error", f"Process {process_id} not found in memory.")

class BuddySystem(MemoryManagement):
    def __init__(self, total_size):
        super().__init__(total_size)
        self.free_blocks = {total_size: [0]}

    def allocate(self, process_id, size, strategy='first_fit'):
        block_size = 1
        while block_size < size:
            block_size *= 2

        if block_size not in self.free_blocks:
            block_size *= 2

        if block_size in self.free_blocks and self.free_blocks[block_size]:
            start = self.free_blocks[block_size].pop(0)
            if not self.free_blocks[block_size]:
                del self.free_blocks[block_size]
            for i in range(start, start + size):
                self.memory[i] = process_id
            self.processes[process_id] = [(start, start + size)]
            return True
        else:
            messagebox.showerror("Error", f"Failed to allocate memory for Process {process_id}")
            return False

    def deallocate(self, process_id):
        if process_id in self.processes:
            allocations = self.processes.pop(process_id)
            for start, end in allocations:
                for j in range(start, end):
                    self.memory[j] = None
                block_size = end - start
                if block_size in self.free_blocks:
                    self.free_blocks[block_size].append(start)
                else:
                    self.free_blocks[block_size] = [start]
        else:
            messagebox.showerror("Error", f"Process {process_id} not found in memory.")

class Paging(MemoryManagement):
    def __init__(self, total_size, page_size):
        super().__init__(total_size)
        self.page_size = page_size
        self.page_table = {}

    def allocate(self, process_id, size, strategy='first_fit'):
        num_pages = (size + self.page_size - 1) // self.page_size
        free_pages = [i for i in range(self.total_size // self.page_size) if all(self.memory[j] is None for j in range(i * self.page_size, (i + 1) * self.page_size))]
        
        if len(free_pages) < num_pages:
            messagebox.showerror("Error", f"Not enough free pages for Process {process_id}")
            return False

        if strategy == 'first_fit':
            allocated_pages = free_pages[:num_pages]
        elif strategy == 'best_fit':
            allocated_pages = free_pages[:num_pages]
        elif strategy == 'next_fit':
            allocated_pages = free_pages[:num_pages]

        for page in allocated_pages:
            for i in range(page * self.page_size, (page + 1) * self.page_size):
                self.memory[i] = process_id

        self.page_table[process_id] = allocated_pages
        return True

    def deallocate(self, process_id):
        if process_id in self.page_table:
            allocated_pages = self.page_table.pop(process_id)
            for page in allocated_pages:
                for i in range(page * self.page_size, (page + 1) * self.page_size):
                    self.memory[i] = None
        else:
            messagebox.showerror("Error", f"Process {process_id} not found in memory.")

class MemoryManagementSimulator:
    def __init__(self, master):
        self.master = master
        self.master.title("Memory Management Simulator")
        self.mm = None
        self.total_memory = 0
        self.allocation_attempts = 0
        self.successful_allocations = 0
        self.algorithm_efficiency = {}

        frame = ttk.Frame(master, padding=10)
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        frame.columnconfigure(1, weight=1)

        self.technique_var = tk.StringVar(value="fixed")
        self.technique_label = ttk.Label(frame, text="Memory Management Technique:")
        self.technique_label.grid(row=0, column=0, pady=5, sticky=tk.W)
        self.technique_menu = ttk.OptionMenu(frame, self.technique_var, "fixed", "fixed", "unequal", "dynamic", "buddy", "paging")
        self.technique_menu.grid(row=0, column=1, pady=5, sticky=tk.EW)

        self.total_memory_label = ttk.Label(frame, text="Total Memory Size:")
        self.total_memory_label.grid(row=1, column=0, pady=5, sticky=tk.W)
        self.total_memory_entry = ttk.Entry(frame)
        self.total_memory_entry.grid(row=1, column=1, pady=5, sticky=tk.EW)

        self.partition_label = ttk.Label(frame, text="Partition Size (fixed/unequal):")
        self.partition_label.grid(row=2, column=0, pady=5, sticky=tk.W)
        self.partition_entry = ttk.Entry(frame)
        self.partition_entry.grid(row=2, column=1, pady=5, sticky=tk.EW)

        self.page_size_label = ttk.Label(frame, text="Page Size (paging):")
        self.page_size_label.grid(row=3, column=0, pady=5, sticky=tk.W)
        self.page_size_entry = ttk.Entry(frame)
        self.page_size_entry.grid(row=3, column=1, pady=5, sticky=tk.EW)

        self.process_id_label = ttk.Label(frame, text="Process ID:")
        self.process_id_label.grid(row=4, column=0, pady=5, sticky=tk.W)
        self.process_id_entry = ttk.Entry(frame)
        self.process_id_entry.grid(row=4, column=1, pady=5, sticky=tk.EW)

        self.process_size_label = ttk.Label(frame, text="Process Size:")
        self.process_size_label.grid(row=5, column=0, pady=5, sticky=tk.W)
        self.process_size_entry = ttk.Entry(frame)
        self.process_size_entry.grid(row=5, column=1, pady=5, sticky=tk.EW)

        self.allocate_button = ttk.Button(frame, text="Allocate", command=self.allocate_memory)
        self.allocate_button.grid(row=6, column=0, pady=5, sticky=tk.EW)

        self.deallocate_button = ttk.Button(frame, text="Deallocate", command=self.deallocate_memory)
        self.deallocate_button.grid(row=6, column=1, pady=5, sticky=tk.EW)

        self.display_button = ttk.Button(frame, text="Display Memory", command=self.display_memory)
        self.display_button.grid(row=7, column=0, columnspan=2, pady=5, sticky=tk.EW)

        self.fragmentation_button = ttk.Button(frame, text="Calculate Fragmentation", command=self.calculate_fragmentation)
        self.fragmentation_button.grid(row=8, column=0, columnspan=2, pady=5, sticky=tk.EW)

        self.visualize_button = ttk.Button(frame, text="Visualize Memory", command=self.visualize_memory)
        self.visualize_button.grid(row=9, column=0, columnspan=2, pady=5, sticky=tk.EW)

        self.setup_button = ttk.Button(frame, text="Setup Memory Management", command=self.setup_memory_management)
        self.setup_button.grid(row=10, column=0, columnspan=2, pady=5, sticky=tk.EW)

        self.comparison_button = ttk.Button(frame, text="Compare Algorithms", command=self.compare_algorithms)
        self.comparison_button.grid(row=11, column=0, columnspan=2, pady=5, sticky=tk.EW)

    def setup_memory_management(self):
        total_memory = int(self.total_memory_entry.get())
        self.total_memory = total_memory
        technique = self.technique_var.get()

        if technique == "fixed":
            partition_size = int(self.partition_entry.get())
            self.mm = FixedSizePartitioning(total_memory, partition_size)
        elif technique == "unequal":
            partition_sizes = list(map(int, self.partition_entry.get().split(',')))
            self.mm = UnequalSizePartitioning(total_memory, partition_sizes)
        elif technique == "dynamic":
            self.mm = DynamicPartitioning(total_memory)
        elif technique == "buddy":
            self.mm = BuddySystem(total_memory)
        elif technique == "paging":
            page_size = int(self.page_size_entry.get())
            self.mm = Paging(total_memory, page_size)
        else:
            messagebox.showerror("Error", "Invalid memory management technique.")
            return

        messagebox.showinfo("Info", f"Memory Management System initialized with {technique} technique.")

    def allocate_memory(self):
        if self.mm is None:
            messagebox.showerror("Error", "Memory management system not initialized.")
            return

        process_id = int(self.process_id_entry.get())
        process_size = int(self.process_size_entry.get())

        if self.mm.allocate(process_id, process_size):
            
            self.successful_allocations += 1
        self.allocation_attempts += 1

        efficiency = (self.successful_allocations / self.allocation_attempts) * 100
        self.algorithm_efficiency[self.technique_var.get()] = efficiency

    def deallocate_memory(self):
        if self.mm is None:
            messagebox.showerror("Error", "Memory management system not initialized.")
            return

        process_id = int(self.process_id_entry.get())
        self.mm.deallocate(process_id)

    def display_memory(self):
        if self.mm is None:
            messagebox.showerror("Error", "Memory management system not initialized.")
            return

        memory_status = self.mm.display_memory()
        messagebox.showinfo("Memory Status", memory_status)

    def calculate_fragmentation(self):
        if self.mm is None:
            messagebox.showerror("Error", "Memory management system not initialized.")
            return

        fragmentation = self.mm.calculate_fragmentation()
        messagebox.showinfo("Fragmentation", f"Memory fragmentation: {fragmentation:.2f}%")

    def visualize_memory(self):
        if self.mm is None:
            messagebox.showerror("Error", "Memory management system not initialized.")
            return

        fig = self.mm.visualize_memory()
        root = tk.Tk()
        root.wm_title("Memory Visualization")

        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        root.mainloop()

    def compare_algorithms(self):
        labels = list(self.algorithm_efficiency.keys())
        efficiencies = list(self.algorithm_efficiency.values())

        fig, ax = plt.subplots()
        ax.bar(labels, efficiencies, color='blue')
        ax.set_xlabel('Memory Management Techniques')
        ax.set_ylabel('Efficiency (%)')
        ax.set_title('Comparison of Memory Management Techniques')

        for i, v in enumerate(efficiencies):
            ax.text(i, v + 0.5, f"{v:.2f}%", ha='center', va='bottom')

        root = tk.Tk()
        root.wm_title("Algorithm Comparison")

        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = MemoryManagementSimulator(root)
    root.mainloop()
