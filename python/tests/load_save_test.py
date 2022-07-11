import os.path

from saleae import automation

def test_load_empty_file(manager: automation.Manager, asset_path: str, tmp_path):
    path = os.path.join(asset_path, 'empty.sal')

    try:
        with manager.load_capture(path) as cap:
            # We should fail to load the captrue - the file doesn't exist yet
            assert(False)
    except automation.SaleaeError:
        pass

    
def test_save_and_load(manager: automation.Manager, asset_path: str, tmp_path):
    path = os.path.join(asset_path, 'cap1.sal')

    save_path = os.path.join(tmp_path, 'new_capture.sal')

    try:
        with manager.load_capture(save_path) as cap:
            # We should fail to load the captrue - the file doesn't exist yet
            assert(False)
    except automation.SaleaeError:
        pass

    with manager.load_capture(path) as cap:
        print(cap.capture_id)
        cap.save_capture(save_path)

    #with manager.load_capture(save_path) as cap:
        #pass

def test_load(manager: automation.Manager, asset_path: str):
    path = os.path.join(asset_path, 'cap1.sal')

    with manager.load_capture(path) as cap:
        pass