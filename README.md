[![CI/CD GitHub Actions](https://github.com/antonsemykin/gtest/actions/workflows/test-action.yml/badge.svg)](https://github.com/antonsemykin/-rep/.github/workflows/main.yml)
[![Coverage Status](https://coveralls.io/repos/antonsemykin/-rep/badge.svg?branch=main)](https://coveralls.io/github/antonsemykin/-rep?branch=main)
[![Quality Gate](https://sonarcloud.io/api/project_badges/measure?project=antonsemykin_-rep&metric=alert_status)](https://sonarcloud.io/dashboard?id=antonsemykin_-rep)
[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=antonsemykin_-rep&metric=bugs)](https://sonarcloud.io/summary/new_code?id=antonsemykin_-rep)
[![Code smells](https://sonarcloud.io/api/project_badges/measure?project=antonsemykin_-rep&metric=code_smells)](https://sonarcloud.io/dashboard?id=antonsemykin_-rep)


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

### 3. 


## Функциональные модели

[docs/functions.md](docs/functions.md)

## Структурные модели

[docs/struct.md](docs/struct.md)

## Поведенческие модели

[docs/behavior.md](docs/behavior.md)
