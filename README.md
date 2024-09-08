# Tetris.py

## Описание игры

Tetris — это классическая арканоидная игра, в которой игроки управляют падающими фигурами, которые состоят из четырех квадратов. Игроки должны поворачивать и перемещать фигуры, чтобы заполнить горизонтальные линии на игровом поле. Когда линия полностью заполняется, она исчезает, и игрок получает очки. Цель игры — набирать как можно больше очков, не допуская заполнения экрана фигурами.

## Схема игры

- Игровое поле: вертикально ориентированная область, где падают фигуры.
- Фигуры: семь различных форм (I, O, T, S, Z, J, L), которые случайным образом появляются в верхней части экрана.
- Очки: количество набранных очков за удаленные линии.

## Функциональные возможности

### 1. Поворот фигуры

**Краткое описание сценария:**
Пользователь может вращать фигуру, нажимая клавишу "Вверх".

**Подробное описание:**
Когда игрок нажимает клавишу "Вверх", приложение проверяет, может ли текущая фигура быть повернута, учитывая ее положение на игровом поле и уже занятые клетки. Если поворот возможен, приложение изменяет ориентацию фигуры и обновляет ее отображение, обеспечивая корректное визуальное представление.

---

### 2. Удаление линии

**Краткое описание сценария:**
Приложение автоматически удаляет заполненные линии, когда они появляются.

**Подробное описание:**
Игровое поле постоянно проверяется на наличие полностью заполненных линий. Если такая линия обнаруживается, приложение удаляет ее с поля, что приводит к изменению других линий выше, которые опускаются вниз. Игрок получает очки на основе количества удаленных линий. Это позволяет поддерживать игровой процесс и добавляет элемент стратегии.

---

### 3. Просмотр следующей фигуры

**Краткое описание сценария:**
Пользователь может видеть следующую фигуру, чтобы планировать свои действия.

**Подробное описание:**
При каждой появлении новой фигуры приложение получает её тип и отображает в специальном окне, находящемся рядом с игровым полем. Это дает игроку возможность заранее оценить, какую фигуру он получит следующей, что помогает принимать стратегические решения о том, как управлять текущей фигурой. Визуализация следующей фигуры также добавляет элемент предвкушения и бросает вызов игроку.


## Функциональные модели

[docs/functions.md](docs/functions.md)

## Структурные модели

[docs/struct.md](docs/struct.md)

## Поведенческие модели

[docs/behavior.md](docs/behavior.md)

## Оценка покрытия тестами Coveralls
[![Coverage Status](https://coveralls.io/repos/github/antonsemykin/-rep/badge.png?branch=main)](https://coveralls.io/github/antonsemykin/-rep?branch=main)
