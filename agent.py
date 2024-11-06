import random
from utils import tprint
from constants import INITIAL_COMUNITY_SIZE


class Comunity():
    def __init__(self, restaurant):
        self.people = []
        for _ in range(random.randint(*INITIAL_COMUNITY_SIZE)):
            self.people.append(Person())
        self.happiness = 100
        self.restaurant = restaurant
        self.time_since_last_check = 0
        self.restaurant.set_community(self)

    def update(self, delta_time):
        self.try_add_person(delta_time)
        for person in self.people:
            person.hunger += 1 * delta_time
            if person.hunger > 100:
                self.remove_person(person)
            elif person.try_to_join_queue(self.restaurant, delta_time):
                self.is_someone_giving_position()
        self.update_happiness()

    def is_someone_giving_position(self):
        """Check if there is someone willing to change position in the queue based on hunger levels"""
        queue = self.restaurant.queue
        current_person = queue[-1]  # Last person in the queue
        i = len(queue) - 1
        for j in range(0, i):
            next_person = queue[j]

            hunger_difference = current_person.hunger - next_person.hunger
            if hunger_difference > 0:
                swap_probability = min(
                    1.0, hunger_difference / (current_person.hunger + 20))

                if random.random() < swap_probability:
                    tprint(f"Person with hunger {int(
                        current_person.hunger)} gets position of person with hunger {int(next_person.hunger)}")
                    queue[i], queue[j] = queue[j], queue[i]
                    return

    def try_add_person(self, deltatime):
        self.time_since_last_check += deltatime

        if self.time_since_last_check >= 3:
            self.time_since_last_check = 0

            base_chance = 10
            scaled_chance = max(0, base_chance + ((self.happiness - 50) / 5))
            chance = random.randint(0, 100)
            if chance <= scaled_chance:
                tprint("New person joined the community.")
                # add 5% of the total comunity size or 1 person
                n = max(1, len(self.people) // 20)
                for _ in range(n):
                    self.people.append(Person())

    def find_hungry_person(self, threshold=80):
        for person in self.people:
            if person.hunger >= threshold:
                return person
        return None

    def remove_person(self, person):
        tprint("Person is leaving the community")
        self.restaurant.remove_from_queue(person)
        self.people.remove(person)

    def update_happiness(self):
        if self.time_since_last_check >= 2:
            self.happiness = 120 - \
                sum(person.hunger for person in self.people) / \
                len(self.people) if len(self.people) > 0 else 0

    def get_happiness(self):
        match = {
            0: "Very Unhappy",
            1: "Unhappy",
            2: "Neutral",
            3: "Happy",
            4: "Very Happy",
            5: "Perfect",
            6: "Perfect"
        }
        return match[int(self.happiness) // 20]

    def get_size(self):
        return len(self.people)


class Person():
    def __init__(self):
        self.hunger = random.randint(0, 80)
        self.is_on_queue = False
        self.time_since_last_try = 0

    def __str__(self):
        return f"Person ({self.hunger:.2f})"

    def receive_food(self, food, community):
        if self.share_food(community, food):
            return

        self.eat(food)

    def share_food(self, community, food):
        if self.hunger < 50:
            hungry_person = community.find_hungry_person(threshold=80)
            if hungry_person:
                shared_nutrition = food.nutrition // 3
                food.nutrition -= shared_nutrition
                tprint(f"{self} shares {shared_nutrition} nutrition with {hungry_person}")
                hungry_person.hunger = max(0, hungry_person.hunger - shared_nutrition)
                self.eat(food)
                return True
        return False

    def eat(self, food):
        self.hunger = max(0, self.hunger - food.nutrition)
        food.kill()
        food = None
        self.is_on_queue = False

    def try_to_join_queue(self, restaurant, delta_time):
        if self.is_on_queue or self.time_since_last_try < 1:
            self.time_since_last_try += delta_time
            return False
        self.time_since_last_try = 0
        if self.hunger >= 90:
            tprint("Person is at their limit, person is joining the queue")
            self.is_on_queue = True
            restaurant.add_to_queue(self)
            return True

        max_queue_length = 10
        queue_factor = max(0, 1 - (len(restaurant.queue) / max_queue_length))
        join_probability = (self.hunger / 100) * (queue_factor * 0.2)

        if random.random() < join_probability:
            tprint("Person with hunger", self.hunger,
                   "decides to join the queue")
            self.is_on_queue = True
            restaurant.add_to_queue(self)
            return True

        return False
