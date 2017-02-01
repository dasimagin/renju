#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import random

urls = [
    'http://www.liveinternet.ru/users/renju/',
    'http://renjuoffline.com/get_games.php',
    'http://renjubase.narod.ru/index/0-4',
    'http://beerliker.narod.ru/downloads.html',
    'http://www.renju.net/downloads/games.php',
    'http://web.archive.org/web/20110202004044/http://renju.gambler.ru/bdt/',
]

students = ['Вадим', 'Виталий', 'Алексей', 'Андрей', 'Юра']

random.seed('Справедливое распределение')

for url in urls:
    print(random.choice(students), url)
