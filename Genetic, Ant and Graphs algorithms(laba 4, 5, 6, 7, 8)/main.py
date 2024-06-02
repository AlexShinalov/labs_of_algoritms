import os
import matplotlib.pyplot as plt
import pandas as pd
import imageio
import random


class Individual: #конкретный индивид в популяции

    def __init__(self, start, end, mutationSteps, function):
        # пределы поиска минимума
        self.start = start
        self.end = end
        self.x = random.triangular(self.start, self.end, mode=(self.start+self.end)/2)  # позиция индивида по Х
        self.y = random.triangular(self.start, self.end, mode=(self.start+self.end)/2)  # позиция индивида по Y
        self.score = 0  # значение функции, которую реализует индивид
        self.function = function  # передаем саму функцию
        self.mutationSteps = mutationSteps  # количество шагов мутации
        self.calculateFunction()  # считаем сразу значение функции

    def calculateFunction(self) -> None:
        #подсчет значений
        self.score = self.function(self.x, self.y)

    def mutate(self) -> None:
        #мутация индивида
        def mutation_rule(p):

            # функция мутации
            delta = 0
            for i in range(1, self.mutationSteps + 1):
                if random.random() < 1 / self.mutationSteps:
                    delta += 1 / (2 ** i)
            if random.randint(0, 1):
                delta = self.end * delta
            else:
                delta = self.start * delta
            p += delta
            if p < 0:
                p = max(p, self.start)
            else:
                p = min(p, self.end)
            return p
        # отклонение по x
        self.x = mutation_rule(self.x)
        # отклонение по У
        self.y = mutation_rule(self.y)
        # пересчитываем значение функции после мутации (x, y)
        self.calculateFunction()


class Genetic:
    #генетический алгоритм
    def __init__(self,
                 numberOfIndividuals,  # размер популяции
                 crossoverRate,  # какая часть популяции должна производить потомство
                 mutationSteps,  # количество шагов мутации
                 chanceMutations,  # шанс особи на мутацию
                 numberGeneration,  # количество поколений
                 function,  # функция для поиска минимума
                 start, end):  # область поиска

        self.numberOfIndividuals = numberOfIndividuals
        self.crossoverRate = crossoverRate
        self.mutationSteps = mutationSteps
        self.chanceMutations = chanceMutations
        self.numberGeneration = numberGeneration
        self.function = function
        self.start = start
        self.end = end
        # самое минимальное значение в популяции
        self.bestScore = float('inf')
        # точка мигимального значения
        self.xy = [float('inf'), float('inf')]
        # Создаём дата-фрейм для резкльтатов
        self.data = pd.DataFrame()

    def crossover(self, parent1: Individual, parent2: Individual) -> [Individual, Individual]:
        # Функция для скрещивания двух родителей

        # создаем 2-х новых детей
        child1 = Individual(self.start, self.end, self.mutationSteps, self.function)
        child2 = Individual(self.start, self.end, self.mutationSteps, self.function)
        # создаем новые координаты для детей
        child1.x, child1.y = parent1.x, parent2.y
        child2.x, child2.y = parent2.x, parent1.y
        return child1, child2

    def startGenetic(self) -> None:
        # будем собирать данные для gif и table.csv
        dataForGIF = []
        dataForTable = []

        # создаем стартовую популяцию
        pack = [self.start, self.end, self.mutationSteps, self.function]
        population = [Individual(*pack) for _ in range(self.numberOfIndividuals)]

        # запуск алгоритма
        for _ in range(self.numberGeneration):
            # сортируем популяцию по значению score
            population = sorted(population, key=lambda item: item.score)
            #отрисовка графика в GIF
            oneStepDataX = [individual.x for individual in population]
            oneStepDataY = [individual.y for individual in population]
            dataForGIF.append([oneStepDataX, oneStepDataY])

            # берем лучший % индивидов, которых будем скрещивать между собой
            bestPopulation = population[:int(self.numberOfIndividuals * self.crossoverRate)]

            #проводим скрещивание
            children = []
            for _ in range(len(bestPopulation)):
                # находим случайную пару для каждого индивида и скрещиваем
                individual_mom = random.choice(bestPopulation)
                individual_dad = random.choice(bestPopulation)
                child1, child2 = self.crossover(individual_mom, individual_dad)
                children.append(child1)
                children.append(child2)
            # добавляем всех группу потомков в нашу популяцию
            population.extend(children)

            for individual in population:
                # проводим мутации для каждого индивида с вероятностью chanceMutations
                if random.choices((0, 1), weights=[1 - self.chanceMutations, self.chanceMutations])[0]:
                    individual.mutate()
            # отбираем лучших индивидов после мутации
            population = sorted(population, key=lambda item: item.score)
            population = population[:self.numberOfIndividuals]
            # записываем в таблицу
            dataForTable.append([population[0].x, population[0].y, population[0].score])
            # запомним лучшего индивида который имеет наилучшее значение экстремума
            if population[0].score < self.bestScore:
                # Мы это делаем потому что все данные мутируют в каждом поколении
                self.bestScore = population[0].score
                self.xy = [population[0].x, population[0].y]

        # Сохраняем, рисуем gif
        snapshot_arr = []
        i = 0
        for x, y in dataForGIF:
            i += 1
            snapshot_name = f"source/g{i}.png"
            fig, ax = plt.subplots()
            fig.suptitle(f"Поколение: {i}")
            fig.patch.set_facecolor("#d1dbe0")
            ax.set_xlabel("Хромосомы данного покления")
            ax.plot(x, y, 'ko')
            ax.set_xlim(min(x) - 2, max(x) + 2)
            ax.set_ylim(min(y) - 2, max(y) + 2)
            plt.savefig(snapshot_name, dpi=70, bbox_inches='tight')
            plt.close()
            snapshot_arr.append(snapshot_name)

        with imageio.get_writer('source/genetic.gif', mode='I') as writer:
            for filename in snapshot_arr:
                image = imageio.imread(filename)
                writer.append_data(image)

        # Сохраняем таблицу
        self.data = pd.DataFrame(dataForTable)
        self.data.columns = ['X', 'Y', 'Лучший результат']


def genetic_algorithm(numberOfIndividuals, numberGeneration, mutationSteps, crossoverRate, chanceMutations, start, end,
                      function) -> [[float, float], float, pd.DataFrame]:
    if not os.path.isdir('source'):
        os.mkdir('source')
    a = Genetic(numberOfIndividuals=int(numberOfIndividuals),
                numberGeneration=int(numberGeneration),
                mutationSteps=int(mutationSteps),
                crossoverRate=float(1),
                chanceMutations=float(chanceMutations),
                function=function,
                start=min(int(start), int(end)),
                end=max(int(start), int(end)))
    a.startGenetic()
    return a.xy, a.bestScore, a.data
