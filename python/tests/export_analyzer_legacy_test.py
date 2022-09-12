from contextlib import contextmanager
import os.path
import threading
import time

import saleae.automation

def test_legacy_export_analyzer(manager: saleae.automation.Manager, asset_path: str, tmp_path):
    path = os.path.join(asset_path, 'small_spi_capture.sal')

    
    with manager.load_capture(path) as cap:
        bitty = 8
        analyzer = cap.add_analyzer('SPI',label=f'SPI (bits={bitty})', settings={
            'MISO': 4,
            'Clock': 3,
            'Enable': 5,
            'Bits per Transfer': f'{bitty} Bits per Transfer{" (Standard)" if bitty == 8 else ""}'
        })

        for type in saleae.automation.RadixType:
            filepath = os.path.join(tmp_path, f'export_{type.name}.csv')
            print(f"Exporting to {filepath}")

            cap.legacy_export_analyzer(filepath=filepath, analyzer=analyzer, radix=type)