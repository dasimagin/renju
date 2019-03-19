import abc
import numpy
import subprocess

class Agent(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def move(game):
        '''Return next move'''
        raise exception.NotImplementedError

    @abc.abstractmethod
    def name():
        '''return name of agent'''
        raise exception.NotImplementedError

class HumanAgent(Agent):
    def __init__(self, name='Human'):
        self._name = name

    def name(self):
        return self._name

    def move(self, game):
        return input()

class BackendAgent(Agent):
    def __init__(self, cmd, name, **kvargs):
        self._name = name
        self._backend = subprocess.Popen(
            cmd.split(),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            **kvargs
        )

    def name(self):
        return self._name

    def send_game_to_backend(self, game):
        data = game.dumps()
        self._backend.stdin.write(data.encode() + b'\n')
        self._backend.stdin.flush()

    def wait_for_backend_move(self):
        data = self._backend.stdout.readline().rstrip()
        return data.decode()

    def move(self, game):
        self.send_game_to_backend(game)
        return self.wait_for_backend_move()
