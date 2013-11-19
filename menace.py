"""
    Abstract menace class.
    Serves as base class for all menace types.
    Define interface for menaces which client can call.
"""
class Menace:
    KILL_PROCESS = "kill-process"
    KILL_INSTANCE = "kill-instance"
    FLOOD_NETWORK = "flood-network"
    FAIL_NETWORK = "fail-network"
    CRASH_NETWORK = "crash-network"
    FAIL_DNS = "fail-dns"
    FAIL_VOLUME = "fail-volume"
    CRASH_IO = "crash-io"
    CRASH_CPU = "crash-cpu"


    def can_apply(self, client):
        """
            Decides whether or not this type of menace is applicable to client
        """
        raise NotImplementedError;

    def apply(self, client):
        """
            Applies the menace to the client. Implemented by the derived class.
        """
        raise NotImplementedError;
