from dataclasses import dataclass, asdict
from typing import Dict, Type


@dataclass
class InfoMessage:
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    MESSAGE = (
        'Тип тренировки: {}; '
        'Длительность: {:.3f} ч.; '
        'Дистанция: {:.3f} км; '
        'Ср. скорость: {:.3f} км/ч; '
        'Потрачено ккал: {:.3f}.'
    )

    def get_message(self) -> str:
        return self.MESSAGE.format(*asdict(self).values())


class Training:
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000

    def __init__(self, action: int, duration: float, weight: float) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        mean_speed = self.get_distance() / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        pass

    def show_training_info(self) -> InfoMessage:
        training_info = InfoMessage(
            self.__class__.__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )
        return training_info


class Running(Training):
    FIRST_COEFFICIENT: float = 18
    SECOND_COEFFICIENT: float = 20

    def get_spent_calories(self) -> float:
        spent_calories = ((self.FIRST_COEFFICIENT * self.get_mean_speed()
                          - self.SECOND_COEFFICIENT) * self.weight
                          / self.M_IN_KM * self.duration * 60)
        return spent_calories


class SportsWalking(Training):
    FIRST_COEFFICIENT: float = 0.035
    SECOND_COEFFICIENT: float = 0.029

    def __init__(self, action: int, duration: float,
                 weight: float, height: int) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        spent_calories = ((self.FIRST_COEFFICIENT * self.weight
                          + (self.get_mean_speed() ** 2 // self.height)
                          * self.SECOND_COEFFICIENT * self.weight)
                          * self.duration * 60)
        return spent_calories


class Swimming(Training):
    FIRST_COEFFICIENT: float = 1.1
    SECOND_COEFFICIENT: float = 2
    LEN_STEP: float = 1.38

    def __init__(self, action: int, duration: float, weight: float,
                 length_pool: int, count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        mean_speed = (self.length_pool * self.count_pool / self.M_IN_KM
                      / self.duration)
        return mean_speed

    def get_spent_calories(self) -> float:
        """Выполняет расчёт количества потраченных калорий за тренировку
         - плавание.
        """
        spent_calories = ((self.get_mean_speed() + self.FIRST_COEFFICIENT)
                          * self.SECOND_COEFFICIENT * self.weight)
        return spent_calories


def read_package(workout: str, data: list) -> Training:
    """Определяет тип тренировки и создает объект соответствующего класса,
     передав ему на вход параметры, полученные во втором аргументе.
    """
    training_type: Dict[str, Type[Training]] = {
        'RUN': Running,
        'WLK': SportsWalking,
        'SWM': Swimming
    }
    return training_type[workout](*data)


def main(training: Training) -> None:
    """Печатает сообщение с данными о тренировке полученного от
    метода get_message(), передав ему на вход объект класса InfoMessage
    метода show_training_info().
     """
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]
    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
