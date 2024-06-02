from math import *
import matplotlib.pyplot as plt
import pandas as pd
import imageio
import random
import os

class Particle:
    def __init__(self, start_range, end_range, current_speed_ratio, local_speed_ratio, global_speed_ratio, target_function):
        # Инициализация частицы
        self.start_range = start_range
        self.end_range = end_range
        self.current_speed_ratio = current_speed_ratio
        self.local_speed_ratio = local_speed_ratio
        self.global_speed_ratio = global_speed_ratio
        self.target_function = target_function
        # Текущая позиция (инициализируется случайно в заданном диапазоне)
        self.current_position = [random.uniform(self.start_range, self.end_range), random.uniform(self.start_range, self.end_range)]
        self.score = self.target_function(*self.current_position)
        # Лучшая локальная позиция
        self.local_best_position = self.current_position[:]
        self.local_best_score = self.score
        # Глобальная лучшая позиция
        self.global_best_position = []
        # Скорость (инициализируется случайно в заданном диапазоне)
        search_range = abs(self.end_range - self.start_range)
        self.speed = [random.uniform(-search_range, search_range), random.uniform(-search_range, search_range)]

    def nextIteration(self) -> None:
        # Вычисление следующей итерации для частицы
        rnd_current_best_position = [random.random(), random.random()]
        rnd_global_best_position = [random.random(), random.random()]
        velocity_ratio = self.local_speed_ratio + self.global_speed_ratio
        common_velocity_ratio = 2 * self.current_speed_ratio / abs(
            2 - velocity_ratio - sqrt(abs(velocity_ratio ** 2 - 4 * velocity_ratio)))

        # Рассчет изменения скорости
        mult_local = list(map(lambda x: x * common_velocity_ratio * self.local_speed_ratio, rnd_current_best_position))
        mult_global = list(map(lambda x: x * common_velocity_ratio * self.global_speed_ratio, rnd_global_best_position))

        between_local_and_cur_pos = [self.local_best_position[0] - self.current_position[0], self.local_best_position[1] - self.current_position[1]]
        between_global_and_cur_pos = [self.global_best_position[0] - self.current_position[0], self.global_best_position[1] - self.current_position[1]]

        new_velocity1 = list(map(lambda x: x * common_velocity_ratio, self.speed))
        new_velocity2 = [coord1 * coord2 for coord1, coord2 in zip(mult_local, between_local_and_cur_pos)]
        new_velocity3 = [coord1 * coord2 for coord1, coord2 in zip(mult_global, between_global_and_cur_pos)]
        self.speed = [coord1 + coord2 + coord3 for coord1, coord2, coord3 in
                      zip(new_velocity1, new_velocity2, new_velocity3)]

        # Обновление текущей позиции и оценка функции
        self.current_position = [coord1 + coord2 for coord1, coord2 in zip(self.current_position, self.speed)]
        self.score = self.target_function(*self.current_position)
        # Обновление лучшей локальной позиции, если текущая оценка лучше
        if self.score < self.local_best_score:
            self.local_best_position = self.current_position[:]
            self.local_best_score = self.score


class SwarmAlgorithm:
    def __init__(self,
                 swarm_size,
                 num_generations,
                 current_speed_ratio,
                 local_speed_ratio,
                 global_speed_ratio,
                 start_range, end_range,
                 target_function):

        self.swarm_size = swarm_size
        self.current_speed_ratio = current_speed_ratio
        self.local_speed_ratio = local_speed_ratio
        self.global_speed_ratio = global_speed_ratio
        self.num_generations = num_generations
        self.target_function = target_function
        self.start_range = start_range
        self.end_range = end_range
        self.global_best_position = []
        self.global_best_score = float('inf')
        self.swarm = []
        self.createSwarm()
        self.data = pd.DataFrame()

    def createSwarm(self) -> None:
        # Создание роя частиц
        pack = [self.start_range, self.end_range, self.current_speed_ratio, self.local_speed_ratio, self.global_speed_ratio, self.target_function]
        self.swarm = [Particle(*pack) for _ in range(self.swarm_size)]
        # Нахождение начальной лучшей позиции
        for particle in self.swarm:
            if particle.local_best_score < self.global_best_score:
                self.global_best_score = particle.local_best_score
                self.global_best_position = particle.local_best_position

    def startSwarm(self) -> None:
        # Запуск метода роя
        dataForGIF = []
        dataForTable = []
        for _ in range(self.num_generations):
            oneDataX = []
            oneDataY = []
            for particle in self.swarm:
                oneDataX.append(particle.current_position[0])
                oneDataY.append(particle.current_position[1])
                particle.global_best_position = self.global_best_position
                particle.nextIteration()
                if particle.score < self.global_best_score:
                    self.global_best_score = particle.score
                    self.global_best_position = particle.local_best_position
                dataForTable.append([self.global_best_position[0], self.global_best_position[1], self.global_best_score])
            dataForGIF.append([oneDataX, oneDataY])

        # Создание анимации GIF и сохранение данных в таблицу
        snapshot_arr = []
        i = 0
        for x, y in dataForGIF:
            i += 1
            snapshot_name = f"s/g{i}.png"
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

        with imageio.get_writer('s/swarm.gif', mode='I') as writer:
            for filename in snapshot_arr:
                image = imageio.imread(filename)
                writer.append_data(image)

        self.data = pd.DataFrame(dataForTable)
        self.data.columns = ['X', 'Y', 'BestScore_F(x,y)']


def swarm_algorithm_custom(swarm_size, num_generations, current_speed_ratio, local_speed_ratio, global_speed_ratio,
                    start_range, end_range, target_function) -> [[float, float], float, pd.DataFrame]:
    if not os.path.isdir('s'):
        os.mkdir('s')
    a = SwarmAlgorithm(swarm_size=int(swarm_size),
              num_generations=int(num_generations),
              current_speed_ratio=float(current_speed_ratio),
              local_speed_ratio=float(local_speed_ratio),
              global_speed_ratio=float(global_speed_ratio),
              target_function=target_function,
              start_range=min(int(start_range), int(end_range)),
              end_range=max(int(start_range), int(end_range)))
    a.startSwarm()
    return a.global_best_position, a.global_best_score, a.data
