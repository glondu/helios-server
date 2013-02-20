from helios.datatypes import DictObject
from helios.datatypes.legacy import LegacyObject

class Signature(DictObject, LegacyObject):
    FIELDS = ['challenge', 'response']

    STRUCTURED_FIELDS = {
        'challenge': 'core/BigInteger',
        'response': 'core/BigInteger'
    }

class Certificate(DictObject, LegacyObject):
    FIELDS = ['signature_key', 'encryption_key', 'signature']

    STRUCTURED_FIELDS = {
        'signature_key': 'core/BigInteger',
        'encryption_key': 'core/BigInteger',
        'signature': 'heliosc/Signature'
    }

class Coefficient(DictObject, LegacyObject):
    FIELDS = [ 'coefficient', 'signature' ]

    STRUCTURED_FIELDS = {
        'coefficient': 'core/BigInteger',
        'signature': 'heliosc/Signature'
    }

class Point(DictObject, LegacyObject):
    FIELDS = [ 'alpha', 'beta', 'signature' ]

    STRUCTURED_FIELDS = {
        'alpha': 'core/BigInteger',
        'signature': 'heliosc/Signature'
    }
