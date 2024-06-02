# Функция для позиционной перестановки
def swap_positions(seq, pos1, pos2):
    seq[pos1], seq[pos2] = seq[pos2], seq[pos1]
    return seq

# Запросить у пользователя три целых числа
numbers = [int(x) for x in input("Введите три числа через пробел: ").split()]

# Проверить, что введено ровно три числа
if len(numbers) != 3:
    print("Пожалуйста, введите ровно три числа.")
else:
    # Создать копию введенной последовательности
    new_sequence = numbers.copy()

    # Позиционная перестановка чисел
    new_sequence = swap_positions(new_sequence, 0, 2)

    # Вычислить сумму всех чисел новой последовательности
    sum_of_numbers = sum(new_sequence)

    # Вычислить разность всех чисел новой последовательности
    diff_of_numbers = new_sequence[0] - new_sequence[1] - new_sequence[2]

    # Вычислить произведение всех чисел новой последовательности
    product_of_numbers = new_sequence[0] * new_sequence[1] * new_sequence[2]

    # Вычислить результаты деления
    division_results = [round(new_sequence[i] / numbers[i], 2) for i in range(3)]

    # Вычислить результаты деления с остатком
    modulo_results = [new_sequence[i] % numbers[1] for i in range(3)]

    # Вывести результаты
    print(f"Вы ввели последовательность: {numbers}")
    print(f"Новая последовательность: {new_sequence}")
    print(f"Сумма всех чисел: {sum_of_numbers}")
    print(f"Разность всех чисел: {diff_of_numbers}")
    print(f"Произведение всех чисел: {product_of_numbers}")
    print(f"Деления чисел последовательностей: {division_results[0]} {division_results[1]} {division_results[2]}")
    print(f"Деление с остатком: {modulo_results[0]} {modulo_results[1]} {modulo_results[2]}")
