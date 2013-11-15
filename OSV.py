from controller.registrar import Registrar
from controller.selector import Selector
from controller.scheduler import Scheduler
from recorder.recorder import Recorder

class OpenStackVaccine:
    def __init__(self, args):
        self.registrar = Registrar()
        self.selector = Selector()
        self.scheduler = Scheduler(args.frequency,
                                    args.start_time,
                                    args.end_time,
                                    args.timezone)
        self.recorder = Recorder()


if __name__ == "__main__":
    pass
