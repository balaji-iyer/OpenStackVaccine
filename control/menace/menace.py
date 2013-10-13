"""
    Abstract menace class.
    Serves as base class for all menace types.
    Define interface for menaces which client can call.
"""
class Menace:

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
