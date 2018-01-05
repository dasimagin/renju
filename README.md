# Renju

This is a public repo of study project. It's designed for 2nd year students of computer science faculty (HSE + Yandex).

Intially the project was inspired by beautifull work [Mastering the game of Go with deep neural networks and tree search](AlphaGo.pdf) from DeepMind. This article describes the first bot (AlphaGo) to beat a human professional Go player without handicaps on a full-sized 19×19 board. It was chosen by Science journal as one of the breakthrough of the year runner-ups in 2016. The model uses a Monte Carlo tree search algorithm to find its moves. Estimation of positions is based on 3 ANNs which are learned by extensive training, both from human and computer plays.

At this moment (5 Jan 2018) there is one more paper [Mastering the game of Go without human knowledge](AlphaGoZero.pdf). It is logical development of previous work. The new bot (AlphaGo Zero) is created without using data from human games, and stronger than any previous version.

This project is purely educational. So, students are invited to learn technologies, ideas and implementation details of AlphaGo bot and then implement own one for Renju game.
