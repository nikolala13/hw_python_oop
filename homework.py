import typing
from dataclasses import dataclass, asdict


@dataclass
class InfoMessage:
    """Создание информационного сообщения о тренировке."""
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
        'Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        return self.MESSAGE.format(**asdict(self))


@dataclass
class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65
    M_IN_KM = 1000
    MIN_IN_H = 60

    action: int
    duration: float
    weight: float

    def get_distance(self) -> float:
        """Получаем дистанцию в километрах."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получаем среднюю скорость движения в км/ч."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получаем кол-во затраченных калорий на тренировку."""
        ...

    def show_training_info(self) -> InfoMessage:
        """Возвращаем сообщение с информацией о выполненной тренировке."""
        message = InfoMessage(
            training_type=type(self).__name__,
            duration=self.duration,
            distance=self.get_distance(),
            speed=self.get_mean_speed(),
            calories=self.get_spent_calories()
        )
        return message


class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER_RUNNING = 18
    CALORIES_MEAN_SPEED_SHIFT_RUNNING = 1.79

    def get_spent_calories(self) -> float:
        """Получаем кол-во израсходованных каллорий за тренировку."""
        return (
            (
                self.CALORIES_MEAN_SPEED_MULTIPLIER_RUNNING
                * self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT_RUNNING)
            * self.weight / self.M_IN_KM
            * (
                self.duration * self.MIN_IN_H))


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    CALORIES_WEIGHT_MULTIPLIER = 0.035
    CALORIES_SPEED_HEIGHT_MULTIPLIER = 0.029
    CM_IN_M = 100
    KMH_IN_MSEC = round(1000 / 3600, 3)

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получаем кол-во израсходованных каллорий за тренировку."""
        return ((self.CALORIES_WEIGHT_MULTIPLIER
                * self.weight
                + ((self.get_mean_speed()
                 * self.KMH_IN_MSEC)
                 ** 2
                 / (self.height / self.CM_IN_M))
                * self.CALORIES_SPEED_HEIGHT_MULTIPLIER
                * self.weight)
                * self.duration
                * self.MIN_IN_H)


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP = 1.38
    CALORIES_MEAN_SPEED_MULTIPLIER_SWIMMING = 1.1
    CALORIES_MEAN_SPEED_SHIFT_SWIMMING = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int) -> None:

        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_distance(self) -> float:
        """Получаем дистанцию, которую преодолели за тренировку"""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получаем среднюю скорость во время тренировки."""
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Получаем кол-во израсходованных каллорий за тренировку."""
        return ((self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_MULTIPLIER_SWIMMING)
                * self.CALORIES_MEAN_SPEED_SHIFT_SWIMMING
                * self.weight
                * self.duration)


def read_package(workout_type: str, data: typing.List[int]):
    """Определяем вид тренировки по данным, полученным от "трекера"."""
    select_workout_type: typing.Dict[str, workout_type(Training)] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    try:
        return select_workout_type[workout_type](*data)
    except KeyError as K:
        print(f'Неизвестный вид тренировки {K}')


def main(training: Training) -> None:
    """Возвращаем строку с информацией о тренировке."""
    info = training.show_training_info()
    return print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        main(read_package(workout_type, data))
