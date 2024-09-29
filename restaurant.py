class Restaurant:
    def __init__(self, plate_tables):
        self.money = 0
        self.foods = ["egg"]
        self.queue = []
        self.plate_tables = plate_tables
    def get_money(self):
        return self.money
    def get_queue_size(self):
        return len(self.queue)
    def get_top_queue(self):
        return self.queue[-5:]
    def add_to_queue(self, person):
        self.queue.append(person)
    def give_food(self):
        if len(self.queue) < 1:
            return
        for plate_table in self.plate_tables:
            if plate_table.has_food():
                last_person = self.queue.pop(0)
                last_person.eat(plate_table.get_food())
    def update(self, delta_time):
        self.give_food()