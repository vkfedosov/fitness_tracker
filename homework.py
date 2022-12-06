from dataclasses import dataclass, asdict
from typing import Dict, Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    MESSAGE = (
        'Тип тренировки: {training_type}; '
        'Длительность: {duration:.3f} ч.; '
        'Дистанция: {distance:.3f} км; '
        'Ср. скорость: {speed:.3f} км/ч; '
        'Потрачено ккал: {calories:.3f}.'
    )

    def get_message(self) -> str:
        """Возвращает информационное сообщение тренировки."""
        return self.MESSAGE.format(**asdict(self))


class Training:
    """Базовый класс тренировки, описывающий любой из видов тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MIN_IN_HOUR: int = 60

    def __init__(self, action: int, duration: float, weight: float) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Выполняет расчёт дистанции, которую пользователь преодолел
        за тренировку.
        """
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Выполняет расчёт средней скорости движения во время тренировки."""
        mean_speed = self.get_distance() / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Выполняет расчёт количества потраченных калорий за тренировку.
        Логика подсчёта калорий для каждого вида тренировки своя и описана в
        соответствующем классе.
        """
        raise NotImplementedError('Метод не может быть вызван напрямую')

    def show_training_info(self) -> InfoMessage:
        """Возвращает информационное сообщение о выполненной тренировке."""
        training_info = InfoMessage(
            self.__class__.__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )
        return training_info


class Running(Training):
    """Класс описывающий тренировку – бег."""
    FIRST_COEFFICIENT: float = 18
    SECOND_COEFFICIENT: float = 20

    def get_spent_calories(self) -> float:
        """Выполняет расчёт количества потраченных калорий за тренировку
        – бег.
        """
        spent_calories = ((self.FIRST_COEFFICIENT * self.get_mean_speed()
                          - self.SECOND_COEFFICIENT) * self.weight
                          / self.M_IN_KM * self.duration * self.MIN_IN_HOUR)
        return spent_calories


class SportsWalking(Training):
    """Класс описывающий тренировку – спортивная ходьба."""
    FIRST_COEFFICIENT: float = 0.035
    SECOND_COEFFICIENT: float = 0.029

    def __init__(self, action: int, duration: float,
                 weight: float, height: int) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Выполняет расчёт количества потраченных калорий за тренировку
        – спортивная ходьба.
        """
        spent_calories = ((self.FIRST_COEFFICIENT * self.weight
                          + (self.get_mean_speed() ** 2 // self.height)
                          * self.SECOND_COEFFICIENT * self.weight)
                          * self.duration * self.MIN_IN_HOUR)
        return spent_calories


class Swimming(Training):
    """Класс описывающий тренировку – плавание."""
    FIRST_COEFFICIENT: float = 1.1
    SECOND_COEFFICIENT: float = 2
    LEN_STEP: float = 1.38

    def __init__(self, action: int, duration: float, weight: float,
                 length_pool: int, count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Выполняет расчёт средней скорости движения во время тренировки
        – плавание.
        """
        mean_speed = (self.length_pool * self.count_pool / self.M_IN_KM
                      / self.duration)
        return mean_speed

    def get_spent_calories(self) -> float:
        """Выполняет расчёт количества потраченных калорий за тренировку
        – плавание.
        """
        spent_calories = ((self.get_mean_speed() + self.FIRST_COEFFICIENT)
                          * self.SECOND_COEFFICIENT * self.weight)
        return spent_calories


def read_package(workout: str, data: list) -> Training:
    """Определяет тип тренировки и создаёт объект соответствующего класса,
    передав ему на вход параметры, полученные во втором аргументе.
    """
    training_type: Dict[str, Type[Training]] = {
        'RUN': Running,
        'WLK': SportsWalking,
        'SWM': Swimming,
    }
    try:
        return training_type[workout](*data)
    except KeyError as ke:
        print(f'Ключ {ke} не найден в словаре')


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
