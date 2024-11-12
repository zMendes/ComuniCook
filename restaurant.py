from utils import tprint, Items


class Restaurant:
    def __init__(self, plate_tables, entities):
        self.money = 11100
        self.foods = ["egg"]
        self.queue = []
        self.plate_tables = plate_tables
        self.community = None
        self.queue_start_x = 100
        self.queue_start_y = 200
        self.queue_spacing = 40
        self.entities = entities

    def set_community(self, community):
        self.community = community

    def get_money(self):
        return self.money

    def get_queue_size(self):
        return len(self.queue)

    def get_top_queue(self):
        return self.queue[-5:]

    def add_to_queue(self, person):
        self.queue.append(person)
        index = len(self.queue) - 1
        person.set_position(
            self.queue_start_x + index * self.queue_spacing,
            self.queue_start_y
        )
        self.entities.append(person)
    def remove_from_queue(self, person):
        if person in self.queue:
            self.queue.remove(person)
            self.update_queue()
            self.entities.remove(person)

    def give_food(self):
        if len(self.queue) < 1:
            return
        for plate_table in self.plate_tables:
            if plate_table.has_food():
                if len(self.queue) < 1:
                    return
                last_person = self.queue.pop(0)
                self.entities.remove(last_person)
                tprint("Giving food to person with hunger:", last_person.hunger)
                last_person.receive_food(plate_table.get_food(), self.community)
                self.update_queue()

    def update_queue(self):
        """Update each person's position in the queue based on their index."""
        for index, person in enumerate(self.queue):
            x = self.queue_start_x + index * self.queue_spacing
            y = self.queue_start_y
            person.set_position(x, y)
            person.is_on_queue = True  # Ensure each person in the queue is marked as such


    def buy(self, item):
        match (item):
            case Items.OVEN:
                if self.money >= 100:
                    self.money -= 100
                    return True
            case Items.SUPER_OVEN:
                if self.money >= 300:
                    self.money -= 300
                    return True
            case Items.PLATE_TABLE:
                if self.money >= 200:
                    self.money -= 200
                    return True
            case Items.ASSISTANT:
                if self.money >= 1000:
                    self.money -= 1000
                    return True
        return False

    def update(self, delta_time):
        self.money += delta_time * self.community.get_size()/10
        self.give_food()
