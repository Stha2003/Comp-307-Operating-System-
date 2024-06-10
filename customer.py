class Customer:
    def __init__(self, id, arrival_time):
        self.id = id
        self.arrival_time = arrival_time
        self.start_time = None
        self.end_time = None

    def __repr__(self):
        return f"Customer(id={self.id}, arrival_time={self.arrival_time}, start_time={self.start_time}, end_time={self.end_time})"
