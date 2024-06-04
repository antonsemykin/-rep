# GeometryDash.py
---

## Схема игры

1. Игрок - квадрат, который движется вперёд по плоской поверхности, падает в ямы и при нажатии подпрыгивает
   
2. Уровень - полоса препятствий с разными усложнениями. После смерти уровень начинается с начала
   
3. Управление:
   1) В любой момент игры пользователь может нажать Esc, чтобы закрыть игру
   2) В главном меню - цифры, чтобы выбрать уровень, а также пробел, чтобы начать игру
   3) Во время игры - пробел или стрелка вверх для прыжка
   4) После смерти или при прохождении уровня - пробел, чтобы начать уровень заново или перейти на следующий соответственно (если уровень последний, пробел завершит игру)

4. Цель игры - пройти уровни, собрав все монеты


## Функциональные возможности:

1. Отрисовка уровня:
   - *Описание:* Пользователь может вручную создать файл в формате .csv с определенным набором символов в текстовом редакторе, либо добавить изменения в уже существующие файлы и при старте выбрать уровень, на котором он хочет играть. Игра загрузит информацию из .csv файлов и отрисует уровень основываясь на написанных символах. В игре присутствует 2 уровня и при прохождении первого вы сразу отправитесь на следующий. Таким образом можно добавлять любое колисчество разных уровней.

2. Создание усложнений на уровнях:
   - *Описание:* В предложенных уровнях существуют разные усложнения, такие как:
      * __сферы__, которые дают увеличенный прыжок и возможность самого прыжка находясь в воздухе;
      * __батуты__(положительные и отрицательные), которые с силой отталкивают игрока вверх или вниз при соприкосновении;
      * __шипы__, убивающие игрока;
      * __стены-ловушки__, через которые можно проходить;
      * __монеты__, сбор которых определяет качество прохождения уровня;
   Приложение непрерывно проверяет положение игрока на игровом поле и определяет, происходит ли столкновение с препятствием. В случае столкновения, с 
игроком сразу происходит то или иное событие, определяемое предметом.

3. Сбор статистики за игру:
   - *Описание:* Приложение отслеживает действия игрока во время игры, такие как количество собранных монет и количество попыток на данный уровень, а также выводит на экран полосу, по которой можно понять положение игрока относительно старта и финиша. Статистика сохраняется для последующего просмотра пользователем после прохождения уровня.
