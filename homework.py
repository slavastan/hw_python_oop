class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self, training_type, duration, distance, speed, calories):
        self.training_type = training_type  # имя класса тренировки
        self.duration = duration  # длительность тренировки в часах
        self.distance = distance  # дистанция в километрах
        self.speed = speed  # средняя скорость
        self.calories = calories  # количество килокалорий

    def get_message(self):
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65  # расстояние за 1 шаг
    M_IN_KM = 1000  # метры в километры

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
    ) -> None:
        self.action = action  # число шагов или гребков
        self.duration = duration  # время тренировки
        self.weight = weight  # вес спортсмена

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        message = InfoMessage(
            self.__class__.__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories(),
        )
        return message


class Running(Training):
    """Тренировка: бег."""
    coeff_calorie_1 = 18  # коэф калорий
    coeff_calorie_2 = 20

    def __init__(self, action: int, duration: float, weight: float) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        return (
            (
                self.coeff_calorie_1 * self.get_mean_speed()
                - self.coeff_calorie_2
            ) * self.weight / self.M_IN_KM * (self.duration * 60)
        )


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    coeff_calorie_3 = 0.035
    coeff_calorie_4 = 0.029

    def __init__(
        self, action: int, duration: float, weight: float, height
    ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return (
            self.coeff_calorie_3 * self.weight
            + (self.get_mean_speed() ** 2 // self.height)
            * self.coeff_calorie_4 * self.weight
        ) * (self.duration * 60)


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38  # расстояние за 1 гребок
    coeff_calorie_5 = 1.1
    coeff_calorie_6 = 2.0

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        length_pool: float,
        count_pool: int,
    ) -> None:
        super().__init__(action, duration, weight)
        self.lenght_pool = length_pool  # длина бассейна в метрах
        self.count_pool = count_pool  # сколько раз переплыли бассейн

    def get_distance(self) -> float:
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        return (
            self.lenght_pool * self.count_pool / self.M_IN_KM / self.duration
        )

    def get_spent_calories(self) -> float:

        return (
            (self.get_mean_speed() + self.coeff_calorie_5)
            * self.coeff_calorie_6 * self.weight
        )


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    type = {
        "SWM": Swimming,
        "RUN": Running,
        "WLK": SportsWalking,
    }
    return type[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == "__main__":
    packages = [
        ("SWM", [720, 1, 80, 25, 40]),
        ("RUN", [15000, 1, 75]),
        ("WLK", [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
