import saleae.automation


def test_get_devices(manager: saleae.automation.Manager):
    all_devices = manager.get_devices()
    num_simulation_devices = len([d for d in all_devices if d.is_simulation])
    assert num_simulation_devices == 0, 'Simulation devices should not be present if not explicitly requested'


def test_get_devices_simulation(manager: saleae.automation.Manager):
    all_devices = manager.get_devices(include_simulation_devices=True)
    num_simulation_devices = len([d for d in all_devices if d.is_simulation])
    assert num_simulation_devices == 3, 'Simulation devices should be present if explicitly requested'
