import abc
import numpy
import subprocess
import util

class Agent(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def policy(game):
        '''Return probabilty matrix of possible actions'''

    @abc.abstractmethod
    def name():
        '''return name of agent'''

class HumanAgent(Agent):
    def __init__(self, name='Human'):
        self._name = name

    def name(self):
        return self._name

    def policy(self, game):
        move = input()
        pos = util.to_pos(move)

        probs = numpy.zeros(game.shape)
        probs[pos] = 1.0

        return probs

class BackendAgent(Agent):
    def __init__(self, backend, name='BackendAgent'):
        self._name = name
        self._backend = subprocess.Popen(
            backend.split(),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE
        )

    def name(self):
        return self._name

    def send_game_to_backend(self, game):
        data = game.dumps().encode()
        self._backend.stdin.write(data + b'\n')
        self._backend.stdin.flush()

    def wait_for_backend_move(self):
        data = self._backend.stdout.readline().rstrip()
        return data.decode()

    def policy(self, game):
        self.send_game_to_backend(game)
        pos = util.to_pos(self.wait_for_backend_move())

        probs = numpy.zeros(game.shape)
        probs[pos] = 1.0

        return probs
