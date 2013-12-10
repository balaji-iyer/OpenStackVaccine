class Notifier:
    """ Base abstract class for different notifiers like EmailNotifier or TextNotifier.
    """

    def __init__(self, client, notified_conf, owner):
        self.client = client
        self.owner_name = owner["name"]
        self.owner_email = owner["email"]
        self.owner_phone = owner["phone"]

    def notify(self, menace, menace_info, applied_at, applied_duration):
        self._do_notify(menace.get_name(),
                menace_info.get("Instance", None),
                menace_info.get("Process", None),
                menace_info.get("Volume", None), 
                applied_at,
                applied_duration)
         
    def _do_notify(self, menace_name, instance_name, process_name, volume_name, applied_at, applied_duration):
        raise NotImplementedError
