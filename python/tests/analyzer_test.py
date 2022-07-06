from contextlib import contextmanager
import os.path
import time

from saleae import automation

def test_add_analyzer(manager: automation.Manager, asset_path: str):
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
        except automation.InvalidRequest:
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
        except automation.InvalidRequest:
            pass


def test_remove_analyzer(manager: automation.Manager, asset_path: str):
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



def test_many_analyzers(manager: automation.Manager, asset_path: str):
    path = os.path.join(asset_path, 'small_spi_capture.sal')
    
    cap = manager.load_capture(path)
    for i in range(100):
        bitty = 8

        with measure(f'add analyzer {i}'):
            cap.add_analyzer('SPI',label=f'SPI ({i}) (bits={bitty})', settings={
                'MISO': 4,
                'Clock': 3,
                'Enable': 5,
                'Bits per Transfer': f'{bitty} Bits per Transfer{" (Standard)" if bitty == 8 else ""}'
            })
