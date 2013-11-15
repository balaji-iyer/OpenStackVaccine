"""
    Scheduler class.
    Schedules fault injections at specific time and frequency.
"""
import os
from datetime import datetime
from datetime import timedelta
from OSV import OpenStackVaccine
from menace.menace import Menace

SUNDAY = 6
SATURDAY = 5
class Scheduler:
    def __init__(self, frequency, start_time, end_time, timezone):
        self.frequency = frequency
        self.start_time = start_time or 9;
        self.end_time = end_time or 16
        self.timezone = timezone or os.environ['TZ']
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
            menace = osv.selector.select_menace(client)
            if menace != None:
                return False

            process = None
            if menace == Menace.KILL_PROCESS:
                process = osv.selector.select_process(client, Menace.KILL_PROCESS)

            instance = osv.selector.select_instance(client, menace, process)

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

        day = datetime.weekday()

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
