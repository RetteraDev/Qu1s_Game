from multiprocessing import Process, Queue
from sockets_listen import Socket
from Qu1s import Qu1s


if __name__ == '__main__':

    game = Process(target = Qu1s().run)
    game.start()