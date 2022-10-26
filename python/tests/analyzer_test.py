from contextlib import contextmanager
import os.path
import threading
import time

import saleae.automation

def test_add_analyzer(manager: saleae.automation.Manager, asset_path: str):
    path = os.path.join(asset_path, 'small_spi_capture.sal')
    
    with manager.load_capture(path) as cap:

        try:
            cap.add_analyzer('SPI', label='Invalid channel', settings={
                'MISO': 4,
                'Clock': 3,
                'Enable': 7,
                'Bits per Transfer': '8 Bits per Transfer (Standard)'        
            })
            assert(False)
        except saleae.automation.InvalidRequestError:
            pass

        for bitty in [1, 8, 16]:
            cap.add_analyzer('SPI',label=f'SPI (bits={bitty})', settings={
                'MISO': 4,
                'Clock': 3,
                'Enable': 5,
                'Bits per Transfer': f'{bitty} Bits per Transfer{" (Standard)" if bitty == 8 else ""}'
            })

        try:
            cap.add_analyzer('SPI', label='Invalid list choice', settings={
                'MISO': 4,
                'Clock': 3,
                'Enable': 5,
                'Bits per Transfer': '8 bits per Transfer (Standard)'        
            })
            assert(False)
        except saleae.automation.InvalidRequestError:
            pass


def test_bool_analyzer_setting(manager: saleae.automation.Manager, asset_path: str):
    path = os.path.join(asset_path, 'small_spi_capture.sal')

    with manager.load_capture(path) as cap:

        try:
            cap.add_analyzer('CAN', label='Invalid checkbox name', settings={
                'CAN': 4,
                'Bit Rate (Bits/s)': 5000,
                'Inverted': True
            })
            assert(False)
        except saleae.automation.InvalidRequestError:
            pass

        cap.add_analyzer('CAN', label='CAN Analyzer', settings={
            'CAN': 4,
            'Bit Rate (Bits/s)': 5000,
            'Inverted (CAN High)': True
        })

        cap.add_analyzer('SMBus', label='SMBus Analyzer', settings={
            'SMBDAT': 3,
            'SMBCLK': 4,
            'Calculate PEC on packets': True
        })



def test_remove_analyzer(manager: saleae.automation.Manager, asset_path: str):
    path = os.path.join(asset_path, 'small_spi_capture.sal')
    
    with manager.load_capture(path) as cap:
        for _ in range(4):
            analyzers = []
            for bitty in [1, 8, 16]:
                analyzer = cap.add_analyzer('SPI',label=f'SPI (bits={bitty})', settings={
                    'MISO': 4,
                    'Clock': 3,
                    'Enable': 5,
                    'Bits per Transfer': f'{bitty} Bits per Transfer{" (Standard)" if bitty == 8 else ""}'
                })
                if bitty == 8:
                    analyzers.append(analyzer)

            for analyzer in analyzers:
                cap.remove_analyzer(analyzer)


@contextmanager
def measure(name: str):
    before = time.time()
    yield
    dt = time.time() - before
    print(f"Took {dt} seconds to execute '{name}'")


def test_many_analyzers(manager: saleae.automation.Manager, asset_path: str):
    path = os.path.join(asset_path, 'small_spi_capture.sal')
    
    with manager.load_capture(path) as cap:
        for i in range(10):
            bitty = 8

            with measure(f'add analyzer {i}'):
                cap.add_analyzer('SPI',label=f'SPI ({i}) (bits={bitty})', settings={
                    'MISO': 4,
                    'Clock': 3,
                    'Enable': 5,
                    'Bits per Transfer': f'{bitty} Bits per Transfer{" (Standard)" if bitty == 8 else ""}'
                })


def test_parallel_analyzer(manager: saleae.automation.Manager, asset_path: str):
    path = os.path.join(asset_path, 'small_spi_capture.sal')
    
    with manager.load_capture(path) as cap:
        threads = []
        for i in range(20):
            bitty = 8

            def add(i):
                with measure(f'add analyzer {i}'):
                    cap.add_analyzer('SPI',label=f'SPI ({i}) (bits={bitty})', settings={
                        'MISO': 4,
                        'Clock': 3,
                        'Enable': 5,
                        'Bits per Transfer': f'{bitty} Bits per Transfer{" (Standard)" if bitty == 8 else ""}'
                    })
            threads.append(threading.Thread(target=add, args=(i,)))

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()
