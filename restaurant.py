from utils import tprint, Items


class Restaurant:
    def __init__(self, plate_tables):
        self.money = 11100
        self.foods = ["egg"]
        self.queue = []
        self.plate_tables = plate_tables
        self.community = None

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

    def remove_from_queue(self, person):
        if person in self.queue:
            self.queue.remove(person)

    def give_food(self):
        if len(self.queue) < 1:
            return
        for plate_table in self.plate_tables:
            if plate_table.has_food():
                if len(self.queue) < 1:
                    return
                last_person = self.queue.pop(0)
                tprint("Giving food to person with hunger:", last_person.hunger)
                last_person.eat(plate_table.get_food())

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
