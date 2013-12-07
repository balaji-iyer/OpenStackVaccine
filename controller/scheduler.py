from datetime import datetime
from datetime import date
from datetime import timedelta
from menace import Menace
from pytz import timezone
import logging
import os
import sys
import time

SUNDAY = 6
SATURDAY = 5
class Scheduler:
    """ Scheduler class.
        Schedules fault injections at specific time and frequency.
    """
    def __init__(self, debug=False):
        self.frequency = 10
        self.start_time = 9;
        self.duration = 10
        self.applied_duration = 60
        self.timezone = os.environ.get('TZ', None) or timezone("US/Eastern")
        self.last_scheduled = None
        self.shall_run = True
        self.debug = debug

    def start(self, osv, conf):
        if "frequency" in conf:
            self.frequency = conf["frequency"]
        if "start_time" in conf:
            self.start_time = conf["start_time"]
        if "duration" in conf:
            self.duration = conf["duration"]
        if "timezone" in conf:
            self.timezone = timezone(conf["timezone"])
        if "applied_duration" in conf:
            self.timezone = conf["applied_duration"]

        while(self.shall_run):
            if self.shall_schedule():
                self.schedule(osv)
            time.sleep(20)


    def schedule(self, osv):
        """ Scheduler Routine.

            Gets random client
            On this random client, select a random menace.
            Select Process if necessary, and select a random instances
            which satisfies the given constraints.

            If can apply menace, create menace.
        """
        client = osv.registrar.get_client()
        selector = osv.selector
        info = {}
        if client != None:
            menace = selector.select_menace(osv)
            if menace == None:
                logging.error("Menace selection returned None. Check clients.json")
                sys.exit(-1)

            process = None
            if menace.needs_process():
                process = selector.select_process(osv)
                if process != None:
                    info["Process"] = process
                    menace.set_process(process)

            instance = selector.select_instance(osv)
            if instance != None:
                info["Instance"] = "%s(%s)" % (instance.get_name(), instance.get_id())
                menace.set_instance(instance)

                volume = None
                if menace.needs_volume():
                    volume = selector.select_volume(osv, instance)
                    if volume != None:
                        info["Volume"] = "%s(%s)" % (volume.get_device(), volume.get_id())
                        menace.set_volume(volume)

            if menace.can_apply():
                applied = menace.apply()

                if applied:
                    logging.info("Menace %s applied: %s"
                            % (menace.get_name(),
                                " ".join(["%s: %s" %(key, pair) for key, pair in info.iteritems()])))

                    # Undo Menace after applied_duration
                    time.sleep(self.applied_duration)
                    applied = menace.undo()

                    if applied:
                        logging.info("Undid Menace %s : %s"
                                % (menace.get_name(),
                                    " ".join(["%s: %s" %(key, pair) for key, pair in info.iteritems()])))

                self.last_scheduled = datetime.now(tz=self.timezone)

    def stop(self):
        """ Set shall_run to False.
            This breaks scheduler loop.
            To start again call start.  """
        self.shall_run = False

    def get_frequency(self):
        return self.frequency

    def shall_schedule(self):
        """ Checks the schedule.
            See if its weekday,
            See if office hours,
            See if recently applied
        """

        time = datetime.now(tz=self.timezone)

        day = date.today().weekday()

        if not self.debug and (day == SUNDAY or day == SATURDAY):
            logging.info("%s today. Take some rest" % ("SUNDAY" if (day - SATURDAY) else "SATURDAY"))
            return False;

        hour = time.hour

        if not self.debug and ( hour < self.start_time or hour > self.start_time + self.duration):
            logging.info("Post Office Hours. Go home. Get some life.")
            return False

        if self.last_scheduled != None:

            # office hours of the day / how many times to run = interval in hours * 3600
            schedule_in_secs = float((self.duration)) / self.frequency * 60 * 60
            if self.last_scheduled + timedelta(seconds=schedule_in_secs) > time:
                logging.info("Next Run in %s"
                        % (self.last_scheduled + timedelta(seconds=schedule_in_secs) - time))
                return False
        return True
