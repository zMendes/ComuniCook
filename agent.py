import random


class Comunity():
    def __init__(self):
        self.people = []
        for _ in range(random.randint(2, 5)):
            self.people.append(Person())
        self.happiness = 100

    def update(self, delta_time):
        self.try_add_person()
        for person in self.people:
            person.hunger += 1 * delta_time
            if person.hunger > 100:
                self.people.remove(person)
                del person
        self.update_happiness()

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

    def get_5most_hungry(self):
        return sorted(self.people, key=lambda x: x.hunger, reverse=True)[:5]

    def giveFood(self, food):
        hungriest = sorted(self.people, key=lambda x: x.hunger, reverse=True)[0]
        hungriest.eat(food)




class Person():
    def __init__(self):
        self.hunger = random.randint(0, 80)

    def eat(self, food):
        self.hunger = 0
        food.kill()
        food = None