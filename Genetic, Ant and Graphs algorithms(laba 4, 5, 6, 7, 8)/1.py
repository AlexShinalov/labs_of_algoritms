import os
import matplotlib.pyplot as plt
import pandas as pd
import imageio
import random


class Creature:  # Репрезентация сущности в популяции

    def __init__(self, start_val, end_val, mutation_steps, func):
        # Определение пределов для минимума
        self.start_val = start_val
        self.end_val = end_val
        self.x = random.triangular(self.start_val, self.end_val, mode=(self.start_val + self.end_val) / 2)  # Позиция сущности по X
        self.y = random.triangular(self.start_val, self.end_val, mode=(self.start_val + self.end_val) / 2)  # Позиция сущности по Y
        self.score = 0  # Значение функции, которую реализует сущность
        self.func = func  # Сама функция
        self.mutation_steps = mutation_steps  # Количество шагов мутации
        self.calculate_func_value()  # Вычисляем значение функции сразу

    def calculate_func_value(self) -> None:
        # Вычисление значений функции
        self.score = self.func(self.x, self.y)

    def mutate(self) -> None:
        # Мутация сущности
        def mutation_rule(param):

            # Функция мутации
            delta = 0
            for i in range(1, self.mutation_steps + 1):
                if random.random() < 1 / self.mutation_steps:
                    delta += 1 / (2 ** i)
            if random.randint(0, 1):
                delta = self.end_val * delta
            else:
                delta = self.start_val * delta
            param += delta
            if param < 0:
                param = max(param, self.start_val)
            else:
                param = min(param, self.end_val)
            return param

        # Отклонение по x
        self.x = mutation_rule(self.x)
        # Отклонение по y
        self.y = mutation_rule(self.y)
        # Пересчитываем значение функции после мутации (x, y)
        self.calculate_func_value()


class Evolutionary:

    def __init__(self,
                 num_creatures,  # Размер популяции
                 crossover_ratio,  # Часть популяции для потомства
                 mutation_steps,  # Количество шагов мутации
                 mutation_chance,  # Вероятность мутации
                 num_generations,  # Количество поколений
                 func,  # Функция для поиска минимума
                 start_val, end_val):  # Область поиска

        self.num_creatures = num_creatures
        self.crossover_ratio = crossover_ratio
        self.mutation_steps = mutation_steps
        self.mutation_chance = mutation_chance
        self.num_generations = num_generations
        self.func = func
        self.start_val = start_val
        self.end_val = end_val

        self.best_score = float('inf')
        self.xy = [float('inf'), float('inf')]
        self.data = pd.DataFrame()

    def crossbreed(self, parent1: Creature, parent2: Creature) -> [Creature, Creature]:
        # Функция для скрещивания двух родителей
        child1 = Creature(self.start_val, self.end_val, self.mutation_steps, self.func)
        child2 = Creature(self.start_val, self.end_val, self.mutation_steps, self.func)

        # Создаем новые координаты для детей
        child1.x, child1.y = parent1.x, parent2.y
        child2.x, child2.y = parent2.x, parent1.y
        return child1, child2

    def initiate_evolution(self) -> None:
        gif_data = []
        table_data = []

        # Создаем стартовую популяцию
        pack = [self.start_val, self.end_val, self.mutation_steps, self.func]
        population = [Creature(*pack) for _ in range(self.num_creatures)]

        for _ in range(self.num_generations):
            # Сортируем популяцию по значению score
            population = sorted(population, key=lambda item: item.score)
            x_values = [creature.x for creature in population]
            y_values = [creature.y for creature in population]
            gif_data.append([x_values, y_values])

            # Лучший % сущностей для скрещивания
            best_population = population[:int(self.num_creatures * self.crossover_ratio)]

            # Скрещивание
            children = []
            for _ in range(len(best_population)):
                individual_mom = random.choice(best_population)
                individual_dad = random.choice(best_population)
                child1, child2 = self.crossbreed(individual_mom, individual_dad)
                children.append(child1)
                children.append(child2)

            population.extend(children)

            for creature in population:
                # Мутация с вероятностью mutation_chance
                if random.choices((0, 1), weights=[1 - self.mutation_chance, self.mutation_chance])[0]:
                    creature.mutate()

            population = sorted(population, key=lambda item: item.score)
            population = population[:self.num_creatures]

            table_data.append([population[0].x, population[0].y, population[0].score])

            if population[0].score < self.best_score:
                self.best_score = population[0].score
                self.xy = [population[0].x, population[0].y]

        # Создаем gif
        snapshot_arr = []
        i = 0
        for x, y in gif_data:
            i += 1
            snapshot_name = f"source/g{i}.png"
            fig, ax = plt.subplots()
            fig.suptitle(f"Generation: {i}")
            fig.patch.set_facecolor("#d1dbe0")
            ax.set_xlabel("Chromosomes of this generation")
            ax.plot(x, y, 'ko')
            ax.set_xlim(min(x) - 2, max(x) + 2)
            ax.set_ylim(min(y) - 2, max(y) + 2)
            plt.savefig(snapshot_name, dpi=70, bbox_inches='tight')
            plt.close()
            snapshot_arr.append(snapshot_name)

        with imageio.get_writer('source/evolutionary.gif', mode='I') as writer:
            for filename in snapshot_arr:
                image = imageio.imread(filename)
                writer.append_data(image)

        # Сохраняем таблицу
        self.data = pd.DataFrame(table_data)
        self.data.columns = ['X', 'Y', 'Best Score']

# Функция генетического алгоритма
def evolutionary_algorithm(num_creatures, num_generations, mutation_steps, crossover_ratio, mutation_chance,
                           start_val, end_val, func) -> [[float, float], float, pd.DataFrame]:
    if not os.path.isdir('source'):
        os.mkdir('source')

    ev = Evolutionary(num_creatures=int(num_creatures),
                      num_generations=int(num_generations),
                      mutation_steps=int(mutation_steps),
                      crossover_ratio=float(1),
                      mutation_chance=float(mutation_chance),
                      func=func,
                      start_val=min(int(start_val), int(end_val)),
                      end_val=max(int(start_val), int(end_val)))

    ev.initiate_evolution()
    return ev.xy, ev.best_score, ev.data
