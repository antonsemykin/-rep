import pytest, sys, pygame
from random import randrange as rand

from main import (rotate_clockwise, check_collision, remove_row, join_matrixes,
                    new_board, colors, tetris_shapes)
from main import TetrisApp
t = TetrisApp()


def test_remove_row():
    """
    Тест функции удаления ряда.
    Проверяем, удаляется ли полный ряд и добавляется ли новый пустой ряд сверху.
    """
    board = new_board()
    board[21] = [1] * 10  
    new_board_after_removal = remove_row(board, 21)

    
    expected_board = new_board()   
    assert new_board_after_removal == expected_board, "Удаление ряда не сработало должным образом."

def test_remove_multiple_rows():
    """
    Тест удаления нескольких полных рядов.
    Убедимся, что функцией корректно удаляются несколько рядов и новый пустой ряд добавляется сверху.
    """
    board = new_board()
    board[21] = [1] * 10
    board[22] = [1] * 10
    
    remove_row(board, 20)
    remove_row(board, 21)
    
    
    expected_board = [[0] * 10 for _ in range(20)] + [[1] * 10]
    assert board == expected_board, "Удаление нескольких рядов не сработало должным образом."

def test_remove_empty_rows():
    """
    Тест удаления одной пустой строки.
    Убедимся, что функцией корректно удаляется пустой ряд
    """
    board = new_board()
    remove_row(board, 20)

    expected_board = [[0] * 10 for _ in range(21)] + [[1] * 10]
    assert board == expected_board, "Удаление пустой строки не сработало должным образом."






def test_four_rotations():
    """
    Тест на множественное вращение фигуры.
    Убедимся, что фигура корректно работает после 4 последовательных вращений.
    """
    shape = tetris_shapes[3]  
    for _ in range(4):  
        shape = rotate_clockwise(shape)
    expected_shape = tetris_shapes[3]
    assert shape == expected_shape, "Фигура не вернулась к исходному состоянию после 4 поворотов."

def test_two_rotations():
    """
    Тест на множественное вращение фигуры.
    Убедимся, что симметричная фигура корректно работает после 2 последовательных вращений.
    """
    shape = tetris_shapes[2]  
    for _ in range(2):  
        shape = rotate_clockwise(shape)
    expected_shape = tetris_shapes[2]
    assert shape == expected_shape, "Симметричная фигура не вернулась к исходному состоянию после 2 поворотов."

def test_rotate_clockwise():
    """
    Тест поворота фигуры по часовой стрелке.
    Ожидаем, что вывод будет фигурой, повернутой на 90 градусов против часовой стрелке.
    """
    shape = tetris_shapes[0]  
    expected = [
        [1, 0],
        [1, 1],
        [1, 0]
    ]  
    result = rotate_clockwise(shape)
    assert result == expected, f"Ожидалось {expected}, получено {result}"






def test_join_matrixes():
    """
    Тест объединения двух матриц (доски и фигуры).
    Убедимся, что фигура корректно объединяется с доской.
    """
    board = new_board()
    shape = [[1, 1],
             [1, 1]]  
    offset = (0, 1)
    result = join_matrixes(board, shape, offset)

    
    expected_board = [
        [1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 0, 0, 0, 0, 0, 0, 0, 0]
        ] + [[0] * 10 for _ in range(20)] + [[1] * 10]
    
    assert result == expected_board, "Объединение матриц не сработало должным образом."

def test_empty_matrixes():
    """
    Тест объединения двух пустых матриц (доски и фигуры).
    Убедимся, что пустая фигура корректно объединяется с пустой доской.
    """
    board = [[0] * 10 for _ in range (23)]
    shape = [[0, 0],
             [0, 0]]
    offset = (0, 1)
    result = join_matrixes(board, shape, offset)

    expected_board = [[0] * 10 for _ in range (23)]
    assert expected_board == result, "Объединение пустых матриц не сработало должным образом."

def test_big_matrixes():
    """
    Тест объединения двух пустых матриц (доски и фигуры).
    Убедимся, что пустая фигура корректно объединяется с пустой доской.
    """
    board = new_board()
    shape = [[0, 0], [0, 0]] #[[1] * 10 for _ in range (23)]
    offset = (0, 1)
    result = join_matrixes(board, shape, offset)

    expected_board = new_board()
    assert expected_board == result, f"Объединение матриц с большой фигурой не сработало должным образом."





if __name__ == "__main__":
    pytest.main()
