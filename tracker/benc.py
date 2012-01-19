from types import IntType, LongType, StringType, ListType, TupleType, DictType
from types import BooleanType
from types import UnicodeType
from cStringIO import StringIO

bencached_marker = []

class Bencached:
    def __init__(self, s):
        self.marker = bencached_marker
        self.bencoded = s

BencachedType = type(Bencached('')) # insufficient, but good as a filter

def encode_bencached(x,r):
    assert x.marker == bencached_marker
    r.append(x.bencoded)

def encode_int(x,r):
    r.extend(('i',str(x),'e'))

def encode_bool(x,r):
    encode_int(int(x),r)

def encode_string(x,r):    
    r.extend((str(len(x)),':',x))

def encode_unicode(x,r):
    encode_string(x.encode('UTF-8'),r)

def encode_list(x,r):
        r.append('l')
        for e in x:
            encode_func[type(e)](e, r)
        r.append('e')

def encode_dict(x,r):
    r.append('d')
    ilist = x.items()
    ilist.sort()
    for k,v in ilist:
        r.extend((str(len(k)),':',k))
        encode_func[type(v)](v, r)
    r.append('e')

encode_func = {}
encode_func[BencachedType] = encode_bencached
encode_func[IntType] = encode_int
encode_func[LongType] = encode_int
encode_func[StringType] = encode_string
encode_func[ListType] = encode_list
encode_func[TupleType] = encode_list
encode_func[DictType] = encode_dict
if BooleanType:
    encode_func[BooleanType] = encode_bool
if UnicodeType:
    encode_func[UnicodeType] = encode_unicode


class EncError(ValueError):
    def __str__(self):
        return "%s"%self.args

def bencode(x):
    r = []
    try:
        encode_func[type(x)](x, r)
    except:
        raise EncError("*** error *** could not encode type %s (value: %s)" % (type(x), x))
    return ''.join(r)