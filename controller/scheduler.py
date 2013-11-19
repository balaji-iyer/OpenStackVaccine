"""
    Scheduler class.
    Schedules fault injections at specific time and frequency.
"""
from datetime import datetime
from datetime import date
from datetime import timedelta
from menace import Menace
from pytz import timezone
import os
import sys

SUNDAY = 6
SATURDAY = 5
class Scheduler:
    def __init__(self, conf):
        self.frequency = conf["frequency"]
        self.start_time = conf["start_time"] or 9;
        self.end_time = conf["end_time"] or 16
        self.timezone = timezone(conf["timezone"]) or os.environ['TZ']
        self.last_scheduled = None
        self.shall_run = True

    def start(self, osv):
        while(self.shall_run):
            if self.shall_schedule():
                self.schedule(osv)


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
                print "Menace selection returned None. Check clients.json"
                sys.exit(-1)

            process = None
            if menace == Menace.KILL_PROCESS:
                process = osv.selector.select_process(Menace.KILL_PROCESS)

            instance = osv.selector.select_instance()

            if client.can_apply_menace(menace):
                client.create_menace(menace, instance, process)



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
            return False;

        hour = time.hour

        if hour < self.start_time or hour > self.end_time:
            return False

        if self.last_scheduled != None:

            # office hours of the day / how many times to run = interval in hours * 3600
            schedule_in_secs = (self.end_time - self.start_time) / self.frequency * 60 * 60
            if self.last_scheduled + timedelta(seconds=schedule_in_secs) < time:
                return False
        return True
from OSV import OpenStackVaccine
