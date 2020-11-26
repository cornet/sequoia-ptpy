from contextlib import contextmanager
from construct import Container, Struct, Range, Computed, Enum, Array, PrefixedArray, Pass, ExprAdapter
from ..ptp import PTPError
import logging
logger = logging.getLogger(__name__)

__all__ = ('FujiX100',)

class FujiX100Error(PTPError):
    pass

class FujiX100(object):
    '''This class implements FujiX100's PTP operations.'''
    def __init__(self, *args, **kwargs):
        logger.debug('Init FujiX100')
        super(FujiX100, self).__init__(*args, **kwargs)

    @contextmanager
    def session(self):
        with super(FujiX100, self).session():
            yield

    def get_config_info(self):
        '''Returns the configuration object info

        Perform GetObject request with the handle set to 0.
        The PTP spec says that requesting this is undefined but Fuji appear
        to be using it as a way of getting the config backup.

        This should be called before getting the object or you will get an authorisation error.
        '''
        ptp = Container(
            OperationCode='GetObjectInfo',
            SessionID=self._session,
            TransactionID=self._transaction,
            Parameter=[0]
        )
        response = self.recv(ptp)
        return response

    def get_config_backup(self):
        '''Returns the configuration backup as binary string.

        Perform GetObject request with the handle set to 0.
        The PTP spec says that requesting this is undefined but Fuji appear
        to be using it as a way of getting the config backup.
        '''
        ptp = Container(
            OperationCode='GetObject',
            SessionID=self._session,
            TransactionID=self._transaction,
            Parameter=[0]
        )
        return self.recv(ptp)
