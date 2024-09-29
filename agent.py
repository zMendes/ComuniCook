import random


class Comunity():
    def __init__(self, restaurant):
        self.people = []
        for _ in range(random.randint(2, 5)):
            self.people.append(Person())
        self.happiness = 100
        self.restaurant = restaurant

    def update(self, delta_time):
        self.try_add_person()
        for person in self.people:
            person.hunger += 1 * delta_time
            if person.hunger > 100:
                self.people.remove(person)
                del person
            if person.try_to_join_queue(self.restaurant):
                self.is_someone_giving_position()
        self.update_happiness()

    def is_someone_giving_position(self):
        """Check if there is someone willing to change position in the queue to make it shorter"""
        queue = self.restaurant.queue
        current_person = queue[-1]
        i = len(queue) - 1
        for j in range(0, i):
            next_person = queue[j]
            if next_person.hunger < current_person.hunger and random.random() < 0.5:
                print(f"Person with hunger {current_person.hunger} gets position of person with hunger {next_person.hunger}")
                queue[i], queue[j] = queue[j], queue[i]
                return

    def try_add_person(self):
        if random.random() < 0.0001 * self.happiness/10: #this ration seems good enough for now
            self.people.append(Person())

    def update_happiness(self):
        self.happiness = 100 - \
            sum([person.hunger for person in self.people]) / \
            len(self.people) if len(self.people) > 0 else 100

    def get_happiness(self):
        match = {
            0: "Very Unhappy",
            1: "Unhappy",
            2: "Neutral",
            3: "Happy",
            4: "Very Happy",
            5: "Perfect"
        }
        return match[int(self.happiness) // 20]

    def get_size(self):
        return len(self.people)

class Person():
    def __init__(self):
        self.hunger = random.randint(0, 80)
        self.is_on_queue = False

    def eat(self, food):
        self.hunger -= food.nutrition
        food.kill()
        food = None

    def try_to_join_queue(self, restaurant):
        if self.is_on_queue:
            return False
        if random.random() * self.hunger > 50:
            self.is_on_queue = True
            restaurant.add_to_queue(self)
            return True
        return False