# Renju

This is a public repo of study project. It's designed for 2nd year students of computer science faculty (HSE + Yandex).

#### AlphaGo
Intially the project was inspired by beautifull work [Mastering the game of Go with deep neural networks and tree search](AlphaGo.pdf) from DeepMind. This article describes the first bot (AlphaGo) to beat a human professional Go player without handicaps on a full-sized 19×19 board. It was chosen by Science journal as one of the breakthrough of the year runner-ups in 2016. The model uses a Monte Carlo tree search algorithm to find its moves. Estimation of positions is based on 3 ANNs which are learned by extensive training, both from human and computer plays.

#### AlphaGo Zero
At this moment (5 Jan 2018) there is one more paper [Mastering the game of Go without human knowledge](AlphaGoZero.pdf). It is logical development of previous work. The new bot (AlphaGo Zero) is created without using data from human games, and stronger than any previous version.

#### Goals
This project is purely educational. So, students are invited to learn technologies, ideas and implementation details of AlphaGo bot and then implement own one for Renju game.

#### Requirements
Your solution should freely run on ubuntu 14+ and Python 3.4 or be compiled with clang (avoid completely new language constructions for compatibility). You also should provide instructions on how to use your application, overview of parameters and code examples of running. A more detailed list of points below:

1. Specify all requirements and version of packages:
 * All python packages
 * All additional deb packages
2. Datasets and additional data that you use
3. prepare – script that uploads all essential data, e.g. model parameters.
4. train – script that train your model from scratch.
5. demo – demo game agent vs human
