"""Test Xiaomi binary sensors."""

from unittest.mock import patch

from homeassistant.components.bluetooth import BluetoothChange
from homeassistant.components.xiaomi_ble.const import DOMAIN
from homeassistant.const import ATTR_FRIENDLY_NAME

from . import make_advertisement

from tests.common import MockConfigEntry


async def test_smoke_sensor(hass):
    """Test setting up a smoke sensor."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        unique_id="54:EF:44:E3:9C:BC",
        data={"bindkey": "5b51a7c91cde6707c9ef18dfda143a58"},
    )
    entry.add_to_hass(hass)

    saved_callback = None

    def _async_register_callback(_hass, _callback, _matcher, _mode):
        nonlocal saved_callback
        saved_callback = _callback
        return lambda: None

    with patch(
        "homeassistant.components.bluetooth.update_coordinator.async_register_callback",
        _async_register_callback,
    ):
        assert await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

    assert len(hass.states.async_all()) == 0
    saved_callback(
        make_advertisement(
            "54:EF:44:E3:9C:BC",
            b"XY\x97\tf\xbc\x9c\xe3D\xefT\x01" b"\x08\x12\x05\x00\x00\x00q^\xbe\x90",
        ),
        BluetoothChange.ADVERTISEMENT,
    )
    await hass.async_block_till_done()
    assert len(hass.states.async_all()) == 1

    smoke_sensor = hass.states.get("binary_sensor.thermometer_e39cbc_smoke")
    smoke_sensor_attribtes = smoke_sensor.attributes
    assert smoke_sensor.state == "on"
    assert smoke_sensor_attribtes[ATTR_FRIENDLY_NAME] == "Thermometer E39CBC Smoke"

    assert await hass.config_entries.async_unload(entry.entry_id)
    await hass.async_block_till_done()


async def test_moisture(hass):
    """Make sure that formldehyde sensors are correctly mapped."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        unique_id="C4:7C:8D:6A:3E:7A",
    )
    entry.add_to_hass(hass)

    saved_callback = None

    def _async_register_callback(_hass, _callback, _matcher, _mode):
        nonlocal saved_callback
        saved_callback = _callback
        return lambda: None

    with patch(
        "homeassistant.components.bluetooth.update_coordinator.async_register_callback",
        _async_register_callback,
    ):
        assert await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

    assert len(hass.states.async_all()) == 0

    # WARNING: This test data is synthetic, rather than captured from a real device
    # obj type is 0x1014, payload len is 0x2 and payload is 0xf400
    saved_callback(
        make_advertisement(
            "C4:7C:8D:6A:3E:7A", b"q \x5d\x01iz>j\x8d|\xc4\r\x14\x10\x02\xf4\x00"
        ),
        BluetoothChange.ADVERTISEMENT,
    )

    await hass.async_block_till_done()
    assert len(hass.states.async_all()) == 1

    sensor = hass.states.get("binary_sensor.smart_flower_pot_6a3e7a_moisture")
    sensor_attr = sensor.attributes
    assert sensor.state == "on"
    assert sensor_attr[ATTR_FRIENDLY_NAME] == "Smart Flower Pot 6A3E7A Moisture"

    assert await hass.config_entries.async_unload(entry.entry_id)
    await hass.async_block_till_done()
