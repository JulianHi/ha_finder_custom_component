"""custom_components/sensor/finder_measurement.py"""
import logging
from homeassistant.helpers.entity import Entity

_LOGGER = logging.getLogger(__name__)

def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the Finder Measurement sensor."""
    sensor_entity_id = config.get('sensor')
    if sensor_entity_id:
        add_entities([FinderMeasurementSensor(sensor_entity_id)])

class FinderMeasurementSensor(Entity):
    """Representation of a Finder Measurement sensor."""

    def __init__(self, sensor_entity_id):
        """Initialize the sensor."""
        self._state = None
        self._unit_of_measurement = "V"
        self._sensor_entity_id = sensor_entity_id

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"Finder Measurement Sensor ({self._sensor_entity_id})"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return self._unit_of_measurement

    def update(self):
        """Update the sensor state."""
        try:
            # Get the state of the specified sensor
            sensor_state = self.hass.states.get(self._sensor_entity_id).state

            # Your custom interpretation logic using the sensor_state
            self._state = interpret_measurement(sensor_state)
        except Exception as e:
            _LOGGER.error("Error updating sensor: %s", str(e))
            self._state = None

def interpret_measurement(sensor_state):
    """Custom function to interpret the measurement."""
    try:
        hex_value = sensor_state  # Assuming the sensor state is in hexadecimal format
        decade_exponent = (int(hex_value, 16) >> 24) - 1
        signed_measurement = int(hex_value, 16) & 0xFFFFFF
        interpreted_value = (signed_measurement * 10**decade_exponent)
        #return round(interpreted_value, 2)
        _LOGGER.info("Finder T5 function executed with result: %s", result)
        return sensor_state
    except Exception as e:
        _LOGGER.error("Error interpreting measurement: %s", str(e))
        return None
