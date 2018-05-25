## Competition

### Rules
1. Each player plays N games for white and black with each opponent.
2. For the victory is awarded 3 points, a draw costs 1 point.
3. In case of an error in the execution time, the player is counted a defeat.
4. Agent has no more that T seconds per one move.
5. The game can't last more than M moves.
6. Initialization time I.

**N = 5 games, T = 15 second, M = 80 moves I = 30**

### Preparing
For competition you need provide only one executable file, which contains all your dependencies and you model weights.
You agent will be runned on Ubuntu 14.04 machine.

#### How to make executable file
If you write your agent on python you may use package [pyinstaller](https://pyinstaller.readthedocs.io/).
Let's we have some small file **source_example.txt** and program **example.py**
```python3
import numpy
import scipy
import tensorflow

# For fucking keras wankers
import scipy._lib.messagestream
import keras


with open('destination_example.txt') as lines:
    print(lines.read())
```
So, you just need input
```
pyinstaller --add-data="source_example.txt:destination_example.txt" -F example.py
```
Flag **F** forces to create only one file.
Option **add-data** says that file **source_example.txt** need to be included in our executable as **destination_example.txt**.

#### Agent interface
Comming soon...
