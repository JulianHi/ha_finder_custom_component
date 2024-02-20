"""GitHub sensor platform."""
import logging
import voluptuous as vol
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import CONF_NAME, CONF_UNIT_OF_MEASUREMENT, CONF_ENTITY_ID
from homeassistant.helpers.entity import Entity
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)

DOMAIN = "finder_measurement"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_NAME, default="Finder Measurement Sensor"): cv.string,
    vol.Optional(CONF_UNIT_OF_MEASUREMENT, default="V"): cv.string,
    vol.Required(CONF_ENTITY_ID): cv.entity_id,
})

def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the Finder Measurement sensor."""
    name = config.get(CONF_NAME)
    unit_of_measurement = config.get(CONF_UNIT_OF_MEASUREMENT)
    entity_id = config.get(CONF_ENTITY_ID)

    sensor = FinderMeasurementSensor(name, unit_of_measurement, entity_id)
    add_entities([sensor])

    def state_changed_listener(event):
        """Handle state changes for the source entity."""
        new_state = event.data.get("new_state")
        if new_state is not None and new_state.entity_id == entity_id:
            sensor.schedule_update_ha_state()

    # Listen for state changes on the specified entity
    hass.bus.listen("state_changed", state_changed_listener)

class FinderMeasurementSensor(Entity):
    """Representation of a Finder Measurement sensor."""

    def __init__(self, name, unit_of_measurement, entity_id):
        """Initialize the sensor."""
        self._state = None
        self._unit_of_measurement = unit_of_measurement
        self._name = name
        self._entity_id = entity_id

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

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
            # Read the value from the specified entity ID
            source_entity_state = self.hass.states.get(self._entity_id)

            if source_entity_state is not None:
                # Use the state of the specified entity for interpretation
                source_entity_value = source_entity_state.state
                self._state = interpret_measurement(source_entity_value)
            else:
                _LOGGER.warning("Entity not found: %s", self._entity_id)
                self._state = None
        except Exception as e:
            _LOGGER.error("Error updating sensor: %s", str(e))
            self._state = None

def interpret_measurement(value):
    """Custom function to interpret the measurement."""
    try:
        # Replace this with your custom interpretation logic
        interpreted_value = float(value)  # Placeholder logic, assuming the value is numeric
        return round(interpreted_value, 2)
    except ValueError as ve:
        _LOGGER.error("Error interpreting measurement: %s", str(ve))
        return None