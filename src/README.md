## Competition

### Rules
1. Each player plays **N** games for white and black with each opponent.
2. For the victory is awarded 3 points, a draw costs 1 point.
3. In case of an error in the execution time, the player is counted a defeat.
4. Agent has no more that **T** seconds per one move.
5. The game can't last more than **M** moves.
6. Initialization time **I**.

**N = 5 games, T = 3 second, M = 80 moves I = 45**

### Preparing
For competition you need provide only one executable file, which contains all your dependencies and you model weights. If you expect some __not specific__ package at host machine, please, contact me.
You agent will be runned on Ubuntu 16.04 (Xenial) machine with Tesla V100 GPU:
* Nvidia 396.44 + CUDA 9.0.176-1
* Python 3.5.2
* Tensorflow 1.12
* Pytorch 1.0.1
* Keras 2.2.4


#### How to make executable file
If you write your agent on python you may use package [pyinstaller](https://pyinstaller.readthedocs.io/).
Let's we have some small file **source_example.txt** and program **example.py**
```python3

# Some default packages
import numpy
import scipy

# Deep learning
import tensorflow
import torch

# Some specific import for Keras
import scipy._lib.messagestream
import keras

# Use outer file!
with open('destination_example.txt') as lines:
    print(lines.read())
```
So, you just need input 
```
# We add source_example.txt at result binary!
pyinstaller --add-data="source_example.txt:destination_example.txt" -F example.py
```

Flag **F** forces to create only one file.
Option **add-data** says that file **source_example.txt** need to be included in our executable as **destination_example.txt**.

#### Agent interface
Comming soon...
