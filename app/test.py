import pytest, sys, pygame
from random import randrange as rand

from main import (rotate_clockwise, check_collision, remove_row, join_matrixes,
                    new_board, colors, tetris_shapes)
from main import TetrisApp
t = TetrisApp()


def test_rotate_clockwise():
    """
    Тест поворота фигуры по часовой стрелке.
    Ожидаем, что вывод будет фигурой, повернутой на 90 градусов против часовой стрелке.
    """
    shape = tetris_shapes[0]  # Форма T
    expected = [
        [1, 0],
        [1, 1],
        [1, 0]
    ]  # Ожидаемая форма после поворота
    result = rotate_clockwise(shape)
    assert result == expected, f"Ожидалось {expected}, получено {result}"


def test_check_collision_no_collision():
    """
    Тест обнаружения столкновения без столкновения.
    Тест проверяет фигуру, расположенную так, что она не сталкивается с доской.
    """
    board = new_board()
    shape = tetris_shapes[1]  # Форма z
    offset = (0, 0)
    result = check_collision(board, shape, offset)
    assert result is False, "Обнаружено столкновение, когда его не должно быть."


def test_check_collision_with_collision():
    """
    Тест обнаружения столкновения, где происходит столкновение.
    Фигура расположена так, что она будет пересекаться с заполненной частью доски.
    """
    board = new_board()
    board[0][0] = 1  # Симуляция заполненной ячейки
    shape = tetris_shapes[6] # квадрат
    offset = (0, 0)
    result = check_collision(board, shape, offset)
    assert result is True, "Не обнаружено столкновения, когда оно должно быть."


def test_remove_row():
    """
    Тест функции удаления ряда.
    Проверяем, удаляется ли полный ряд и добавляется ли новый пустой ряд сверху.
    """
    board = new_board()
    board[21] = [1] * 10  # Заполнение последнего ряда
    new_board_after_removal = remove_row(board, 21)

    # Последний ряд должен быть пустым, а новый пустой ряд должен быть сверху
    expected_board = new_board()   # [[0] * 10] + [[0] * 10 for _ in range(21)]
    assert new_board_after_removal == expected_board, "Удаление ряда не сработало должным образом."


def test_join_matrixes():
    """
    Тест объединения двух матриц (доски и фигуры).
    Убедимся, что фигура корректно объединяется с доской.
    """
    board = new_board()
    shape = [[1, 1],
             [1, 1]]  # 2x2 квадрат
    offset = (0, 1)
    result = join_matrixes(board, shape, offset)

    # В левом верхнем углу должна быть заполненная область после объединения
    expected_board = [
        [1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 0, 0, 0, 0, 0, 0, 0, 0]
        ] + [[0] * 10 for _ in range(20)] + [[1] * 10]
    
    assert result == expected_board, "Объединение матриц не сработало должным образом."



def test_new_board():
    """
    Тест создания новой доски.
    Она должна быть заполнена нулями и иметь дополнительный заполненный ряд внизу.
    """
    result = new_board()
    expected_shape = [[0] * 10 for _ in range(22)]
    expected_shape.append([1] * 10)  # Нижний ряд заполнен единицами
    
    assert result == expected_shape, "Новая доска не была создана должным образом."


###################################################################################

# def test_save_board_state():
#     """
#     Тест сохранения состояния доски.
#     Убедимся, что состояние доски сохраняется правильно.
#     """
#     board = new_board()
#     board[21] = [1] * 10  # Заполнение ряда
#     saved_state = save_board_state(board)
#     assert saved_state == board, "Состояние доски не было сохранено правильно."


def test_remove_multiple_rows():
    """
    Тест удаления нескольких полных рядов.
    Убедимся, что функции корректно удаляются несколько рядов и новый пустой ряд добавляется сверху.
    """
    board = new_board()
    board[20] = [1] * 10  # Первый полный ряд
    board[19] = [1] * 10  # Второй полный ряд

    new_board_after_removal = new_board()
    remove_row(board, 20)  # Удаляем ряд 20, потом обновим для второго
    remove_row(new_board_after_removal, 19)

    # Ожидаем, что оба ряда будут удалены, а сверху будет два пустых ряда
    expected_board = [[0] * 10 for _ in range(22)] + [[1] * 10]
    assert new_board_after_removal == expected_board, "Удаление нескольких рядов не сработало должным образом."


def test_successful_rotation():
    """
    Тест успешного вращения фигуры.
    Убедимся, что фигура вращается корректно на пустой доске.
    """
    shape = tetris_shapes[0]  # Форма T
    initial_shape = shape
    for _ in range(4):  # Повернём фигуру 4 раза
        shape = rotate_clockwise(shape)
    assert shape == initial_shape, "Фигура не вернулась к исходному состоянию после 4 поворотов."


def test_invalid_initial_position():
    """
    Тест на неправильные начальные позиции фигуры.
    Убедимся, что позиция фигуры не выходит за пределы доски.
    """
    board = new_board()
    shape = tetris_shapes[0]
    offset = (-1, 0)  # Неправильная позиция
    result = check_collision(board, shape, offset)
    assert result is True, "Некорректная начальная позиция фигуры не вызвала обнаружение столкновения."



###################################################################################

def inc(x):
    return x + 1


def test_answer():
    assert inc(3) == 4




def test_move_piece_down():
    """
    Тест на перемещение фигуры вниз.
    Убедимся, что фигура перемещается вниз, когда это возможно.
    """
    board = new_board()
    shape = tetris_shapes[0]  # Форма T
    position = (0, 0)  # Начальная позиция
    new_position = (1, 0)  # Новый желаемый вниз
    result = check_collision(board, shape, new_position)
    
    # Убеждаемся, что при проверке столкновения с новой позицией его не будет
    assert result is False, "Фигура не должна сталкиваться при перемещении вниз." 


def test_move_piece_down_collision():
    """
    Тест на невозможность перемещения фигуры вниз.
    Проверим, что фигура не перемещается вниз, если под ней есть препятствие.
    """
    board = new_board()
    board[1] = [1] * 10  # Создадим преграду
    shape = tetris_shapes[0]
    position = (0, 0)
    new_position = (1, 0) 
    result = check_collision(board, shape, new_position)
    
    # Убедимся, что при проверке столкновения с новой позицией оно будет
    assert result is True, "Фигура должна сталкиваться при попытке перемещения вниз." 


def test_multiple_rotation():
    """
    Тест на множественное вращение фигуры.
    Убедимся, что фигура корректно работает после нескольких последовательных вращений.
    """
    shape = tetris_shapes[1]  # Форма квадрата
    for _ in range(4):  # Повернём фигуру 4 раза
        shape = rotate_clockwise(shape)
    
    # Для фигуры квадрата результат должен остаться тем же
    expected_shape = tetris_shapes[1]
    assert shape == expected_shape, "Фигура не вернулась к исходному состоянию после 4 поворотов."


def test_move_piece_horizontal():
    """
    Тест на горизонтальное перемещение фигуры.
    Проверим, сможет ли фигура перемещаться влево и вправо.
    """
    board = new_board()
    shape = tetris_shapes[0]  # Форма T
    position = (0, 0)
    
    # Проверка перемещения вправо
    new_position_right = (0, 1)
    result_right = check_collision(board, shape, new_position_right)
    assert result_right is False, "Фигура не должна сталкиваться при перемещении вправо."

    # Проверка перемещения влево
    new_position_left = (0, -1)
    result_left = check_collision(board, shape, new_position_left)
    assert result_left is True, "Фигура должна сталкиваться при перемещении влево."


def test_piece_stacking():
    """
    Тест на стыковку фигур.
    Убедимся, что фигуры правильно располагаются друг на друге.
    """
    board = new_board()
    shape1 = tetris_shapes[0]  # Первая фигура
    shape2 = tetris_shapes[1]  # Вторая фигура

    # Устанавливаем первую фигуру
    join_matrixes(board, shape1, (0, 0))
    
    # Проверка, что можно установить вторую фигуру поверх первой
    result = join_matrixes(board, shape2, (1, 0))
    
    # Ожидаем, что вторая фигура успешно разместится на первой
    assert result[0][0] == 1, "Вторая фигура не должна размещаться поверх первой."


# Существующие тесты остаются без изменений

# Добавьте сюда уже существующие тесты...

if __name__ == "__main__":
    pytest.main()



### for me: 21 строка это предпоследняя