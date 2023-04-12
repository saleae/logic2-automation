try:
    from saleae.grpc import saleae_pb2, saleae_pb2_grpc
except Exception as exc:
    import sys
    sys.stderr.write('''There was an error that occurred while importing grpc/pb modules.
This can be caused by pb files that were generated using an incompatible version of protobuf.
You can regenerate these files by reinstalling logic2-automation:

     pip install logic2-automation --force-reinstall

 ''')
    raise exc from None

from .manager import *
from .capture import *
from .errors import *
