import time
from typing import Literal
import pytest
import os.path

from saleae import automation

def test_export(manager: automation.Manager, asset_path: str, tmp_path):
    path = os.path.join(asset_path, 'cap1.sal')

    save_path = os.path.join(tmp_path, 'new_capture.sal')

    try:
        with manager.load_capture(save_path) as cap:
            # We should fail to load the captrue
            assert(False)
    except:
        pass
    
    with manager.load_capture(path) as cap:
        cap.save_capture(save_path)

    with manager.load_capture(save_path) as cap:
        pass
    
