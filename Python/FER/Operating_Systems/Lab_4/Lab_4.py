class OnDemandPaging:
    def __init__(self, memory_size, page_size):
        self.page_size = page_size
        self.num_frames = memory_size // page_size
        self.page_table = {}
        self.frame_table = [None] * self.num_frames
        self.memory = [None] * memory_size
        self.next_frame = 0
        self.time = 0

    def access_memory(self, logical_address):
        page_number = logical_address // self.page_size
        offset = logical_address % self.page_size

        if page_number in self.page_table:
            frame_number = self.page_table[page_number]
        else:
            frame_number = self.next_frame
            self.page_table[page_number] = frame_number
            self.frame_table[frame_number] = page_number
            self.next_frame = (self.next_frame + 1) % self.num_frames

        physical_address = frame_number * self.page_size + offset
        self.memory[physical_address] = self.time  # Simulate data write
        self.time += 1

        self.print_state(logical_address, physical_address)

    def print_state(self, logical_address, physical_address):
        print(f"Logical Address: {logical_address}, Physical Address: {physical_address}")
        print("Page Table:", self.page_table)
        print("Frame Table:", self.frame_table)
        print("Memory:", self.memory[:64])
        print("\n")

# Simulate a computer with 16-bit addresses and 64-byte page size
memory_size = 256  # For simplicity, using 256 bytes of physical memory
page_size = 64
paging = OnDemandPaging(memory_size, page_size)

# Sample memory access requests
requests = [10, 70, 130, 190, 15, 80, 140, 200]

for req in requests:
    paging.access_memory(req)
