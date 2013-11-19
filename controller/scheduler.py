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
    def __init__(self, conf):
        self.frequency = conf["frequency"]
        self.start_time = conf["start_time"] or 9;
        self.end_time = conf["end_time"] or 16
        self.timezone = timezone(conf["timezone"]) or os.environ['TZ']
        self.last_scheduled = None
        self.shall_run = True

    def start(self, osv):
        import pdb;pdb.set_trace()
        while(self.shall_run):
            if self.shall_schedule():
                self.schedule(osv)
            time.sleep(60)


    def schedule(self, osv):
        """ Scheduler Routine.

            Gets random client
            On this random client, select a random menace.
            Select Process if necessary, and select a random instances
            which satisfies the given constraints.

            If can apply menace, create menace.
        """
        client = osv.registrar.get_client()

        if client != None:
            menace = osv.selector.select_menace()
            if menace == None:
                logging.error("Menace selection returned None. Check clients.json")
                sys.exit(-1)

            process = None
            if menace == Menace.KILL_PROCESS:
                process = osv.selector.select_process(Menace.KILL_PROCESS)

            instance = osv.selector.select_instance()

            if client.can_apply_menace(menace):
                client.create_menace(menace, instance, process)
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

        if day == SUNDAY or day == SATURDAY:
            logging.info("%s today. Take some rest" % "SUNDAY" if day - SATURDAY else "SATURDAY")
            return False;

        hour = time.hour

        if hour < self.start_time or hour > self.end_time:
            logging.info("Post Office Hours. Go home. Get some life.")
            return False

        if self.last_scheduled != None:

            # office hours of the day / how many times to run = interval in hours * 3600
            schedule_in_secs = float((self.end_time - self.start_time)) / self.frequency * 60 * 60
            if self.last_scheduled + timedelta(seconds=schedule_in_secs) > time:
                logging.info("Next Run in %s"
                        % (self.last_scheduled + timedelta(seconds=schedule_in_secs) - time))
                return False
        return True

