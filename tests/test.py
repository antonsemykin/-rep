import pytest

def inc(x):
    return x + 1


def test_answer():
    assert inc(3) == 5


    

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
