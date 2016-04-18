'''This module implements Picture Transfer Protocol (ISO 15740:2013(E))

It is transport agnostic and requires a transport layer to provide the missing
methods in the class :py:class`PTPDevice`.

Convenience structures are provided to pack messages. These are native-endian
and may need to be adapted to transport-endianness:

    SessionID()  # returns native endian constructor
    SessionID(le=True)  # returns little endian constructor
    SessionID(be=True)  # returns big endian constructor
'''
from construct import (
    Container, Struct, Enum, UNInt8, UNInt16, UNInt32, Array, BitField, ULInt8,
    ULInt16, ULInt32, UBInt8, UBInt16, UBInt32, Pass, PascalString, Debugger
    )
from contextlib import contextmanager

# Module specific
# _______________
__all__ = (
    'PTPError', 'PTPUnimplemented', 'SessionID', 'TransactionID',
    'OperationCode', 'ResponseCode', 'EventCode', 'Event', 'Response',
    'Operation', 'PTPDevice',
    )

__author__ = 'Luis Mario Domenzain'


# Exceptions
# ----------
class PTPError(Exception):
    '''PTP implementation exceptions.'''
    pass


class PTPUnimplemented(PTPError):
    '''Exception to indicate missing implementation.'''
    pass


# Helper functions
# ----------------
def switch_endian(le, be, l, b, n):
    '''Return little, native or big endian.'''
    if (be != le):
        return l if le else b
    elif le:
        raise PTPError('Cannot be both little and big endian...')
    else:
        return n


# Base PTP protocol transaction elements
# --------------------------------------

# Apparently nobody uses the SessionID field. Even though it is specified in
# ISO15740:2013(E), no device respects it and the session number is implicit.
def SessionID(_le_=False, _be_=False):
    '''Return desired endianness for SessionID'''
    subcon = switch_endian(_le_, _be_, ULInt32, UBInt32, UNInt32)
    return subcon('SessionID')


def TransactionID(_le_=False, _be_=False):
    '''Return desired endianness for TransactionID'''
    subcon = switch_endian(_le_, _be_, ULInt32, UBInt32, UNInt32)
    return subcon('TransactionID')


def Parameter(_le_=False, _be_=False):
    '''Return desired endianness for Parameter'''
    return switch_endian(
        _le_,
        _be_,
        BitField('Parameter', 32, swapped=True),
        BitField('Parameter', 32, swapped=False),
        BitField('Parameter', 32)
    )


def OperationCode(_le_=False, _be_=False, **vendor_operations):
    '''Return desired endianness for known OperationCode'''
    subcon = switch_endian(_le_, _be_, ULInt16, UBInt16, UNInt16)
    return Enum(
        subcon('OperationCode'),
        _default_=Pass,
        Undefined=0x1000,
        GetDeviceInfo=0x1001,
        OpenSession=0x1002,
        CloseSession=0x1003,
        GetStorageIDs=0x1004,
        GetStorageInfo=0x1005,
        GetNumObjects=0x1006,
        GetObjectHandles=0x1007,
        GetObjectInfo=0x1008,
        GetObject=0x1009,
        GetThumb=0x100A,
        DeleteObject=0x100B,
        SendObjectInfo=0x100C,
        SendObject=0x100D,
        InitiateCapture=0x100E,
        FormatStore=0x100F,
        ResetDevice=0x1010,
        SelfTest=0x1011,
        SetObjectProtection=0x1012,
        PowerDown=0x1013,
        GetDevicePropDesc=0x1014,
        GetDevicePropValue=0x1015,
        SetDevicePropValue=0x1016,
        ResetDevicePropValue=0x1017,
        TerminateOpenCapture=0x1018,
        MoveObject=0x1019,
        CopyObject=0x101A,
        GetPartialObject=0x101B,
        InitiateOpenCapture=0x101C,
        StartEnumHandles=0x101D,
        EnumHandles=0x101E,
        StopEnumHandles=0x101F,
        GetVendorExtensionMapss=0x1020,
        GetVendorDeviceInfo=0x1021,
        GetResizedImageObject=0x1022,
        GetFilesystemManifest=0x1023,
        GetStreamInfo=0x1024,
        GetStream=0x1025,
        **vendor_operations
        )


def ResponseCode(_le_=False, _be_=False, **vendor_responses):
    '''Return desired endianness for known ResponseCode'''
    subcon = switch_endian(_le_, _be_, ULInt16, UBInt16, UNInt16)
    return Enum(
        subcon('ResponseCode'),
        _default_=Pass,
        Undefined=0x2000,
        OK=0x2001,
        GeneralError=0x2002,
        SessionNotOpen=0x2003,
        InvalidTransactionID=0x2004,
        OperationNotSupported=0x2005,
        ParameterNotSupported=0x2006,
        IncompleteTransfer=0x2007,
        InvalidStorageId=0x2008,
        InvalidObjectHandle=0x2009,
        DevicePropNotSupported=0x200A,
        InvalidObjectFormatCode=0x200B,
        StoreFull=0x200C,
        ObjectWriteProtected=0x200D,
        StoreReadOnly=0x200E,
        AccessDenied=0x200F,
        NoThumbnailPresent=0x2010,
        SelfTestFailed=0x2011,
        PartialDeletion=0x2012,
        StoreNotAvailable=0x2013,
        SpecificationByFormatUnsupported=0x2014,
        NoValidObjectInfo=0x2015,
        InvalidCodeFormat=0x2016,
        UnknownVendorCode=0x2017,
        CaptureAlreadyTerminated=0x2018,
        DeviceBusy=0x2019,
        InvalidParentObject=0x201A,
        InvalidDevicePropFormat=0x201B,
        InvalidDevicePropValue=0x201C,
        InvalidParameter=0x201D,
        SessionAlreadyOpened=0x201E,
        TransactionCanceled=0x201F,
        SpecificationOfDestinationUnsupported=0x2020,
        InvalidEnumHandle=0x2021,
        NoStreamEnabled=0x2022,
        InvalidDataset=0x2023,
        **vendor_responses
        )


def EventCode(_le_=False, _be_=False, **vendor_events):
    '''Return desired endianness for known EventCode'''
    subcon = switch_endian(_le_, _be_, ULInt16, UBInt16, UNInt16)
    return Enum(
        subcon('EventCode'),
        _default_=Pass,
        Undefined=0x4000,
        CancelTransaction=0x4001,
        ObjectAdded=0x4002,
        ObjectRemoved=0x4003,
        StoreAdded=0x4004,
        StoreRemoved=0x4005,
        DevicePropChanged=0x4006,
        ObjectInfoChanged=0x4007,
        DeviceInfoChanged=0x4008,
        RequestObjectTransfer=0x4009,
        StoreFull=0x400A,
        DeviceReset=0x400B,
        StorageInfoChanged=0x400C,
        CaptureComplete=0x400D,
        UnreportedStatus=0x400E,
        **vendor_events
        )


def Event(_le_=False, _be_=False):
    return Struct(
        'Event',
        EventCode(_le_=_le_, _be_=_be_),
        SessionID(_le_=_le_, _be_=_be_),
        TransactionID(_le_=_le_, _be_=_be_),
        Array(3, Parameter(_le_=_le_, _be_=_be_)),
    )


def Response(_le_=False, _be_=False):
    return Struct(
        'Response',
        ResponseCode(_le_=_le_, _be_=_be_),
        SessionID(_le_=_le_, _be_=_be_),
        TransactionID(_le_=_le_, _be_=_be_),
        Array(5, Parameter(_le_=_le_, _be_=_be_)),
    )


def Operation(_le_=False, _be_=False):
    return Struct(
        'Operation',
        OperationCode(_le_=_le_, _be_=_be_),
        SessionID(_le_=_le_, _be_=_be_),
        TransactionID(_le_=_le_, _be_=_be_),
        Array(5, Parameter(_le_=_le_, _be_=_be_)),
    )


# PTP Datasets for specific operations
# ------------------------------------


def PropertyCode(_le_=False, _be_=False, **vendor_properties):
    '''Return desired endianness for known OperationCode'''
    subcon = switch_endian(_le_, _be_, ULInt16, UBInt16, UNInt16)
    return Enum(
        subcon('PropertyCode'),
        _default_=Pass,
        Undefined=0x5000,
        BatteryLevel=0x5001,
        FunctionalMode=0x5002,
        ImageSize=0x5003,
        CompressionSetting=0x5004,
        WhiteBalance=0x5005,
        RGBGain=0x5006,
        FNumber=0x5007,
        FocalLength=0x5008,
        FocusDistance=0x5009,
        FocusMode=0x500A,
        ExposureMeteringMode=0x500B,
        FlashMode=0x500C,
        ExposureTime=0x500D,
        ExposureProgramMode=0x500E,
        ExposureIndex=0x500F,
        ExposureBiasCompensation=0x5010,
        DateTime=0x5011,
        CaptureDelay=0x5012,
        StillCaptureMode=0x5013,
        Contrast=0x5014,
        Sharpness=0x5015,
        DigitalZoom=0x5016,
        EffectMode=0x5017,
        BurstNumber=0x5018,
        BurstInterval=0x5019,
        TimelapseNumber=0x501A,
        TimelapseInterval=0x501B,
        FocusMeteringMode=0x501C,
        UploadURL=0x501D,
        Artist=0x501E,
        CopyrightInfo=0x501F,
        **vendor_properties
    )


def PTPString(name, _le_=False, _be_=False):
    '''Returns a PTP String constructor'''
    return PascalString(
        name,
        length_field=switch_endian(
            _le_, _be_, ULInt8, UBInt8, UNInt8
        )('length'),
        encoding='utf16'
    )


def PTPArray(name, element, _le_=False, _be_=False):
    Length = switch_endian(_le_, _be_, ULInt32, UBInt32, UNInt32)
    return Struct(
        name,
        Length('length'),
        Array(lambda ctx: ctx.length, element),
    )


def ObjectFormatCode(_le_=False, _be_=False, **vendor_object_formats):
    '''Return desired endianness for known ObjectFormatCode'''
    subcon = switch_endian(_le_, _be_, ULInt16, UBInt16, UNInt16)
    return Enum(
        subcon('ObjectFormatCode'),
        # Ancilliary
        Undefined=0x3000,
        Association=0x3001,
        Script=0x3002,
        Executable=0x3003,
        Text=0x3004,
        HTML=0x3005,
        DPOF=0x3006,
        AIFF=0x3007,
        WAV=0x3008,
        MP3=0x3009,
        AVI=0x300A,
        MPEG=0x300B,
        ASF=0x300C,
        QT=0x300D,
        # Images
        EXIF_JPEG=0x3801,
        TIFF_EP=0x3802,
        FlashPix=0x3803,
        BMP=0x3804,
        CIFF=0x3805,
        GIF=0x3807,
        JFIF=0x3808,
        PCD=0x3809,
        PICT=0x380A,
        PNG=0x380B,
        TIFF=0x380D,
        TIFF_IT=0x380E,
        JP2=0x380F,
        JPX=0x3810,
        DNG=0x3811,
        _default_=Pass,
        **vendor_object_formats
    )


def DeviceInfo(_le_=False, _be_=False):
    return Struct(
        'DeviceInfo',
        ULInt16('StandardVersion'),
        ULInt32('VendorExtensionID'),
        ULInt16('VendorExtensionVersion'),
        PTPString('VendorExtensionDesc'),
        ULInt16('FunctionalMode'),
        PTPArray(
            'OperationSupported',
            OperationCode(_le_=_le_, _be_=_be_)
        ),
        PTPArray(
            'EventsSupported',
            EventCode(_le_=_le_, _be_=_be_)
        ),
        PTPArray(
            'DevicePropertiesSupported',
            PropertyCode(_le_=_le_, _be_=_be_)
        ),
        PTPArray(
            'CaptureFormats',
            ObjectFormatCode(_le_=_le_, _be_=_be_)
        ),
        PTPString('Manufacturer'),
        PTPString('Model'),
        PTPString('DeviceVersion'),
        PTPString('SerialNumber'),
    )


class PTPDevice(object):
    '''Implement bare PTP Device. Vendor specific devices should extend it.'''

    def _set_endian(self, little=False, big=False):
        self._DeviceInfo = DeviceInfo(_le_=little, _be_=big)
        self._SessionID = SessionID(_le_=little, _be_=big)
        self._TransactionID = TransactionID(_le_=little, _be_=big)
        self._Parameter = Parameter(_le_=little, _be_=big)
        self._OperationCode = OperationCode(_le_=little, _be_=big)
        self._ResponseCode = ResponseCode(_le_=little, _be_=big)
        self._EventCode = EventCode(_le_=little, _be_=big)
        self._Event = Event(_le_=little, _be_=big)
        self._Response = Response(_le_=little, _be_=big)
        self._Operation = Operation(_le_=little, _be_=big)
        self._PropertyCode = PropertyCode(_le_=little, _be_=big)
        self._ObjectFormatCode = ObjectFormatCode(_le_=little, _be_=big)

    __session = 0
    __transaction_id = 0

    @property
    def __transaction(self):
        '''Give magical property for the latest TransactionID'''
        current_id = self.__transaction_id
        self.__transaction_id += 1
        if self.__transaction_id > 0xFFFFFFFE:
            self.__transaction_id = 1
        return current_id

    @__transaction.setter
    def __transaction(self, value):
        '''Manage reset of TransactionID'''
        if value != 0:
            raise PTPError(
                'Current TransactionID should not be set. Only reset.'
            )
        else:
            self.__transaction_id = 0

    def __init__(self):
        raise PTPUnimplemented(
            'Please implement PTP device setup for this transport.'
        )

    def send(self, ptp_container, payload):
        '''Operation with dataphase from initiator to responder'''
        raise PTPUnimplemented(
            'Please implement a PTP dataphase send for this transport.'
        )

    def recv(self, ptp_container):
        '''Operation with dataphase from responder to initiator'''
        raise PTPUnimplemented(
            'Please implement PTP dataphase receive for this transport.'
        )

    def mesg(self, ptp_container):
        '''Operation with no dataphase'''
        raise PTPUnimplemented(
            'Please implement PTP no-dataphase command for this transport.'
        )

    def event(self, wait=False):
        raise PTPUnimplemented(
            'Please implement a PTP event for this transport.'
        )

    @property
    def session_id(self):
        '''Expose internat SessionID'''
        return self.__session

    @session_id.setter
    def session_id(self, value):
        '''Ignore external modifications to SessionID'''
        pass

    @contextmanager
    def session(self):
        '''Manage session with context manager.

        Once transport specifig interfaces are defined, this allows easier,
        more nuclear sessions:

            ptp = PTPUSB()
            with ptp.session():
                ptp.get_device_info()
        '''
        try:
            self.open_session()
            yield
        finally:
            self.close_session()

    def open_session(self):
        self.__session += 1
        self.__transaction = 0
        ptp = Container(
            OperationCode='OpenSession',
            # Only the OpenSession operation is allowed to have a 0
            # SessionID, because no session is open yet.
            SessionID=0,
            TransactionID=self.__transaction,
            Parameter=[self.__session, 0, 0, 0, 0]
        )
        response = self.mesg(ptp)
        return response

    def close_session(self):
        ptp = Container(
            OperationCode='CloseSession',
            SessionID=self.__session,
            TransactionID=self.__transaction,
            Parameter=[0, 0, 0, 0, 0]
        )
        response = self.mesg(ptp)
        return response
