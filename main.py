import math
import os
import random
import matplotlib.pyplot as plt
import numpy as np


class Population:
    def __init__(self, starting_population, target):
        self.creatures = []
        self.target_iterations = target

        self.habitat = Habitat()

        share_count = 0
        steal_count = 0
        for i in range(starting_population):
            temp = BlueCreature()
            self.creatures.append(temp)
            if temp.nature == "Share":
                share_count += 1
            elif temp.nature == "Steal":
                steal_count += 1

        self.num_died = 0
        self.num_reproduced = 0
        self.iterations = 0

        self.x_array1 = []
        self.y_array1 = []  # Avg Mutation chance
        self.y_array2 = []  # Population Each iteration

        self.y_array3 = []  # Track Nature of Steal
        self.y_array4 = []  # Track Nature of Share
        self.y_array5 = []  # Track number of Blue Creatures
        self.y_array6 = []  # Track number of Red Creatures
        self.y_array7 = []  # Track number of Green Creatures

    def iterate(self):
        temp = self.creatures
        average_mutation_chance = 0
        share_count = 0
        steal_count = 0
        blue_count = 0
        red_count = 0
        green_count = 0
        for creature in self.creatures:
            if creature.nature == "Share":
                share_count += 1
            elif creature.nature == "Steal":
                steal_count += 1
            if creature.type == "Blue":
                blue_count += 1
            elif creature.type == "Red":
                red_count += 1
            elif creature.type == "Green":
                green_count += 1

            creature.days_alive += 1  # increment the amount of days alive for each creature.

            average_mutation_chance += creature.mutation_chance
            if self.check_reproduce(creature):
                temp_creature = creature.reproduce()
                if temp_creature.nature == "Share":
                    share_count += 1
                elif temp_creature.nature == "Steal":
                    steal_count += 1
                if creature.has_different_stats():
                    if creature.nature == "Share":
                        # temp_creature.set_stats(creature.reproduce_rate, creature.mutation_chance,
                        #                       creature.death_rate, creature.nature)
                        temp_creature.mutations = creature.mutations
                    elif creature.nature == "Steal":
                        # temp_creature.set_stats(creature.reproduce_rate, creature.mutation_chance,
                        #                        creature.death_rate, creature.nature)
                        temp_creature.mutations = creature.mutations

                if self.check_mutation(temp_creature):
                    x = random.randrange(0, 3)
                    match x:
                        case 0:
                            temp_creature.reproduce_rate += 1
                        case 1:
                            temp_creature.mutation_chance += 1
                        case 2:
                            temp_creature.death_rate += 1
                    temp_creature.mutations += 1

                temp.append(temp_creature)
                self.num_reproduced += 1

            # kill the creature if it dies from random chance, or the creature lives past its lifetime
            elif self.check_die(creature) or creature.days_alive >= creature.lifetime:
                self.num_died += 1
                temp.remove(creature)
                if creature.nature == "Share":
                    share_count -= 1
                elif creature.nature == "Steal":
                    steal_count -= 1
                del creature

        self.creatures = temp
        self.iterations += 1
        if self.iterations % int(self.target_iterations*0.016) == 0 or self.iterations == self.target_iterations:
            if len(self.creatures) > 0:
                self.y_array1.append(float(average_mutation_chance) / len(self.creatures))
            else:
                self.y_array1.append(0)
            self.y_array2.append(len(self.creatures))
            self.x_array1.append(self.iterations)
            self.y_array3.append(steal_count)
            self.y_array4.append(share_count)
            self.y_array5.append(blue_count)
            self.y_array6.append(red_count)
            self.y_array7.append(green_count)
            print(f'Iteration: {self.iterations}')
            print(len(self.creatures))



    def check_reproduce(self, creature):
        if creature.nature == "Share":
            return self.get_random(creature.reproduce_rate + 1)
        return self.get_random(creature.reproduce_rate)

    def check_die(self, creature):
        if creature.nature == "Steal":
            return self.get_random(creature.death_rate + int(0.01 * len(self.creatures)) + 1)
        else:
            return self.get_random(creature.death_rate + int(0.01 * len(self.creatures)))

    def check_mutation(self, creature):
        return self.get_random(creature.mutation_chance)

    def get_random(self, num):
        if random.randrange(0, 1000) <= num:
            return True


class Creature:

    def __init__(self):
        # self.mutations = 0
        self.nature = random.choice(["Share", "Steal"])
        self.days_alive = 0
        self.lifetime = 1
        self.days_since_last_eaten = 0  # Keep track of the last time the creature ate
        self.need_to_eat_every = 0  # Keep track of how often the creature needs to eat
        # self.reproduce_rate = 100
        # self.death_rate = 110
        # self.mutation_chance = 1

    def set_stats(self, reproduce_rate, mutation_chance, death_rate, nature):
        # self.mutations = 0
        self.reproduce_rate = reproduce_rate
        self.death_rate = death_rate
        self.mutation_chance = mutation_chance
        self.nature = nature

    def reproduce(self):
        val = random.randrange(0, 100)
        if val == 0:
            return GreenCreature()

    def has_different_stats(self):
        return (self.reproduce_rate != 100) or (self.mutation_chance != 1) or (self.death_rate != 110)


class BlueCreature(Creature):

    def __init__(self, reproduce_rate=100, mutation_rate=1, death_rate=110, nature=""):
        super().__init__()
        self.mutations = 0
        self.nature = nature if nature != "" else random.choice(["Share", "Steal"])
        self.reproduce_rate = reproduce_rate
        self.death_rate = death_rate
        self.mutation_chance = mutation_rate
        self.lifetime = 50
        self.type = "Blue"

        self.need_to_eat_every = 5  # Keep track of how often the creature needs to eat

    def reproduce(self):
        val = random.randrange(0, 100)
        if val == 0:
            return GreenCreature(nature=self.nature)
        else:
            return BlueCreature(nature=self.nature)


class GreenCreature(Creature):

    def __init__(self, reproduce_rate=110, mutation_rate=2, death_rate=115, nature=""):
        super().__init__()
        self.mutations = 0
        self.nature = nature if nature != "" else random.choice(["Share", "Steal"])
        self.reproduce_rate = reproduce_rate
        self.death_rate = death_rate
        self.mutation_chance = mutation_rate
        self.lifetime = 50
        self.type = "Green"

        self.need_to_eat_every = 5  # Keep track of how often the creature needs to eat

    def reproduce(self):
        val = random.randrange(0, 500)
        if val == 0:
            return RedCreature(nature=self.nature)
        else:
            return GreenCreature(nature=self.nature)


class RedCreature(Creature):

    def __init__(self, reproduce_rate=103, mutation_rate=1, death_rate=107, nature=""):
        super().__init__()
        self.mutations = 0
        self.nature = nature if nature != "" else random.choice(["Share", "Steal"])
        self.reproduce_rate = reproduce_rate
        self.death_rate = death_rate
        self.mutation_chance = mutation_rate
        self.lifetime = 70
        self.type = "Red"

        self.need_to_eat_every = 5  # Keep track of how often the creature needs to eat

    def reproduce(self):
        return RedCreature(nature=self.nature)

class Predator:
    def __init__(self):
        pass

class Habitat:
    def __init__(self, produce_amount=10):
        self.produce = produce_amount  # the number of produce the habitat produces each iteration


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    target = 1000
    pop = Population(400, target=target)
    GreenCreature()
    while pop.iterations != target:
        pop.iterate()

    f, ax = plt.subplots(2, 2)
    plt.subplots_adjust(wspace=0.3, hspace=0.4)

    # plt.plot(pop.x_array1)
    # plt.plot(pop.y_array1)
    # plt.figure()

    # plt.subplot(211)
    ax[0][0].plot(pop.x_array1, pop.y_array1)
    # plt.scatter(pop.x_array1, pop.y_array1, )
    ax[0][0].set(xlabel="Iterations", ylabel="Mutation Chance")
    # plt.xlabel("Iterations")
    # plt.ylabel("Mutation Chance")

    # plt.figure(2)
    # plt.subplot(212)
    ax[0][1].plot(pop.x_array1, pop.y_array2)
    # plt.scatter(pop.x_array1, pop.y_array2)
    ax[0][1].set(xlabel="Iterations", ylabel="Population")
    # plt.ylabel("Population")
    # plt.xlabel("Iterations")
    ax[1][0].plot(pop.x_array1, pop.y_array3, label="Steal")
    ax[1][0].plot(pop.x_array1, pop.y_array4, label="Share")
    ax[1][0].set(xlabel="Iterations", ylabel="Steal/Share Nature")
    # ax[1][1].set(xlabel="Iterations", ylabel="Share Nature")
    ax[1][0].legend()

    ax[1][1].plot(pop.x_array1, pop.y_array5, label="Blue")
    ax[1][1].plot(pop.x_array1, pop.y_array6, label="Red", color="r")
    ax[1][1].plot(pop.x_array1, pop.y_array7, label="Green", color='g')
    ax[1][1].set(xlabel="Iterations", ylabel="Creature Type")
    ax[1][1].legend()
    # plt.ylabel("Population With Nature")
    # plt.xlabel("Iterations")

    count = 0
    path = "/Users/christianwagenknecht/PycharmProjects/Population Simulation/Saved Graphs/graphs000.pdf"
    while os.path.exists(path):
        print("pause")
        count += 1
        if count < 10:
            path = f'/Users/christianwagenknecht/PycharmProjects/Population Simulation/Saved Graphs/graphs00{count}.pdf'
        elif count < 100:
            path = f'/Users/christianwagenknecht/PycharmProjects/Population Simulation/Saved Graphs/graphs0{count}.pdf'
    if count < 10:
        plt.savefig(f'Saved Graphs/graphs00{count}.pdf')
    elif count < 100:
        plt.savefig(f'Saved Graphs/graphs0{count}.pdf')


    plt.show()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
