import logging


logging.addLevelName("VDEBUG", 5)


class EuterpeLogger(logging.Logger):
    __slots__ = ()

    def vdebug(self, *args, **kargs):
        self.log(5, *args, **kargs)


logging.setLoggerClass(EuterpeLogger)
logging.basicConfig()

euterpe = logging.getLogger("euterpe")
server = euterpe.getChild("server")
config = euterpe.getChild("config")
