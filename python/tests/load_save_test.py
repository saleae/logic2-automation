import os.path

import saleae.automation

def test_load_empty_file(manager: saleae.automation.Manager, asset_path: str, tmp_path):
    path = os.path.join(asset_path, 'empty.sal')

    try:
        with manager.load_capture(path) as cap:
            # We should fail to load the captrue - the file doesn't exist yet
            assert(False)
    except saleae.automation.SaleaeError:
        pass


def test_save_and_load(manager: saleae.automation.Manager, asset_path: str, tmp_path):
    path = os.path.join(asset_path, 'cap1.sal')

    save_path = os.path.join(tmp_path, 'new_capture.sal')

    try:
        with manager.load_capture(save_path) as cap:
            # We should fail to load the captrue - the file doesn't exist yet
            assert(False)
    except saleae.automation.SaleaeError:
        pass

    with manager.load_capture(path) as cap:
        print(cap.capture_id)
        cap.save_capture(save_path)

    with manager.load_capture(save_path) as cap:
        pass


def test_load_small(manager: saleae.automation.Manager, asset_path: str):
    path = os.path.join(asset_path, 'cap1.sal')

    with manager.load_capture(path) as cap:
        pass


def test_load_stress(manager: saleae.automation.Manager, asset_path: str, tmp_path):
    path = os.path.join(asset_path, 'cap1.sal')
    export_path = os.path.join(tmp_path, 'export')

    with manager.load_capture(path) as cap:
        cap.export_raw_data_binary(directory=export_path)
        with manager.load_capture(path) as cap2:
            cap2.export_raw_data_binary(directory=export_path)
            bitty = 8
            analyzer = cap2.add_analyzer('SPI', label=f'SPI (bits={bitty})', settings={
                'MISO': 0,
                'Clock': 1,
                'Bits per Transfer': f'{bitty} Bits per Transfer{" (Standard)" if bitty == 8 else ""}'
            })
            export_filepath = os.path.join(tmp_path, 'data_table.csv')

            cap2.export_data_table(filepath=export_filepath, analyzers=[])
            cap2.save_capture(os.path.join(tmp_path, 'my_cap2.sal'))
