"""Data template classes for discovery used to generate additional data for setup."""
from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass, field
import logging
from typing import Any

from zwave_js_server.const import CommandClass
from zwave_js_server.const.command_class.meter import (
    CURRENT_METER_TYPES,
    ENERGY_TOTAL_INCREASING_METER_TYPES,
    POWER_FACTOR_METER_TYPES,
    POWER_METER_TYPES,
    UNIT_AMPERE as METER_UNIT_AMPERE,
    UNIT_CUBIC_FEET,
    UNIT_CUBIC_METER as METER_UNIT_CUBIC_METER,
    UNIT_KILOWATT_HOUR,
    UNIT_US_GALLON,
    UNIT_VOLT as METER_UNIT_VOLT,
    UNIT_WATT as METER_UNIT_WATT,
    VOLTAGE_METER_TYPES,
    ElectricScale,
    MeterScaleType,
)
from zwave_js_server.const.command_class.multilevel_sensor import (
    CO2_SENSORS,
    CO_SENSORS,
    CURRENT_SENSORS,
    ENERGY_MEASUREMENT_SENSORS,
    HUMIDITY_SENSORS,
    ILLUMINANCE_SENSORS,
    POWER_SENSORS,
    PRESSURE_SENSORS,
    SIGNAL_STRENGTH_SENSORS,
    TEMPERATURE_SENSORS,
    UNIT_AMPERE as SENSOR_UNIT_AMPERE,
    UNIT_BTU_H,
    UNIT_CELSIUS,
    UNIT_CENTIMETER,
    UNIT_CUBIC_FEET_PER_MINUTE,
    UNIT_CUBIC_METER as SENSOR_UNIT_CUBIC_METER,
    UNIT_CUBIC_METER_PER_HOUR,
    UNIT_DECIBEL,
    UNIT_DEGREES,
    UNIT_DENSITY,
    UNIT_FAHRENHEIT,
    UNIT_FEET,
    UNIT_GALLONS,
    UNIT_HERTZ,
    UNIT_INCHES_OF_MERCURY,
    UNIT_INCHES_PER_HOUR,
    UNIT_KILOGRAM,
    UNIT_KILOHERTZ,
    UNIT_LITER,
    UNIT_LUX,
    UNIT_M_S,
    UNIT_METER,
    UNIT_MICROGRAM_PER_CUBIC_METER,
    UNIT_MILLIAMPERE,
    UNIT_MILLIMETER_HOUR,
    UNIT_MILLIVOLT,
    UNIT_MPH,
    UNIT_PARTS_MILLION,
    UNIT_PERCENTAGE_VALUE,
    UNIT_POUND_PER_SQUARE_INCH,
    UNIT_POUNDS,
    UNIT_POWER_LEVEL,
    UNIT_RSSI,
    UNIT_SECOND,
    UNIT_SYSTOLIC,
    UNIT_VOLT as SENSOR_UNIT_VOLT,
    UNIT_WATT as SENSOR_UNIT_WATT,
    UNIT_WATT_PER_SQUARE_METER,
    VOLTAGE_SENSORS,
    MultilevelSensorScaleType,
    MultilevelSensorType,
)
from zwave_js_server.model.node import Node as ZwaveNode
from zwave_js_server.model.value import (
    ConfigurationValue as ZwaveConfigurationValue,
    Value as ZwaveValue,
    get_value_id,
)
from zwave_js_server.util.command_class.meter import get_meter_scale_type
from zwave_js_server.util.command_class.multilevel_sensor import (
    get_multilevel_sensor_scale_type,
    get_multilevel_sensor_type,
)

from homeassistant.const import (
    CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
    CONCENTRATION_PARTS_PER_MILLION,
    DEGREE,
    ELECTRIC_CURRENT_AMPERE,
    ELECTRIC_CURRENT_MILLIAMPERE,
    ELECTRIC_POTENTIAL_MILLIVOLT,
    ELECTRIC_POTENTIAL_VOLT,
    ENERGY_KILO_WATT_HOUR,
    FREQUENCY_HERTZ,
    FREQUENCY_KILOHERTZ,
    IRRADIATION_WATTS_PER_SQUARE_METER,
    LENGTH_CENTIMETERS,
    LENGTH_FEET,
    LENGTH_METERS,
    LIGHT_LUX,
    MASS_KILOGRAMS,
    MASS_POUNDS,
    PERCENTAGE,
    POWER_BTU_PER_HOUR,
    POWER_WATT,
    PRECIPITATION_INCHES_PER_HOUR,
    PRECIPITATION_MILLIMETERS_PER_HOUR,
    PRESSURE_INHG,
    PRESSURE_MMHG,
    PRESSURE_PSI,
    SIGNAL_STRENGTH_DECIBELS,
    SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
    SPEED_METERS_PER_SECOND,
    SPEED_MILES_PER_HOUR,
    TEMP_CELSIUS,
    TEMP_FAHRENHEIT,
    TIME_SECONDS,
    VOLUME_CUBIC_FEET,
    VOLUME_CUBIC_METERS,
    VOLUME_FLOW_RATE_CUBIC_FEET_PER_MINUTE,
    VOLUME_FLOW_RATE_CUBIC_METERS_PER_HOUR,
    VOLUME_GALLONS,
    VOLUME_LITERS,
)

from .const import (
    ENTITY_DESC_KEY_BATTERY,
    ENTITY_DESC_KEY_CO,
    ENTITY_DESC_KEY_CO2,
    ENTITY_DESC_KEY_CURRENT,
    ENTITY_DESC_KEY_ENERGY_MEASUREMENT,
    ENTITY_DESC_KEY_ENERGY_TOTAL_INCREASING,
    ENTITY_DESC_KEY_HUMIDITY,
    ENTITY_DESC_KEY_ILLUMINANCE,
    ENTITY_DESC_KEY_MEASUREMENT,
    ENTITY_DESC_KEY_POWER,
    ENTITY_DESC_KEY_POWER_FACTOR,
    ENTITY_DESC_KEY_PRESSURE,
    ENTITY_DESC_KEY_SIGNAL_STRENGTH,
    ENTITY_DESC_KEY_TARGET_TEMPERATURE,
    ENTITY_DESC_KEY_TEMPERATURE,
    ENTITY_DESC_KEY_TOTAL_INCREASING,
    ENTITY_DESC_KEY_VOLTAGE,
)
from .helpers import ZwaveValueID

METER_DEVICE_CLASS_MAP: dict[str, set[MeterScaleType]] = {
    ENTITY_DESC_KEY_CURRENT: CURRENT_METER_TYPES,
    ENTITY_DESC_KEY_VOLTAGE: VOLTAGE_METER_TYPES,
    ENTITY_DESC_KEY_ENERGY_TOTAL_INCREASING: ENERGY_TOTAL_INCREASING_METER_TYPES,
    ENTITY_DESC_KEY_POWER: POWER_METER_TYPES,
    ENTITY_DESC_KEY_POWER_FACTOR: POWER_FACTOR_METER_TYPES,
}

MULTILEVEL_SENSOR_DEVICE_CLASS_MAP: dict[str, set[MultilevelSensorType]] = {
    ENTITY_DESC_KEY_CO: CO_SENSORS,
    ENTITY_DESC_KEY_CO2: CO2_SENSORS,
    ENTITY_DESC_KEY_CURRENT: CURRENT_SENSORS,
    ENTITY_DESC_KEY_ENERGY_MEASUREMENT: ENERGY_MEASUREMENT_SENSORS,
    ENTITY_DESC_KEY_HUMIDITY: HUMIDITY_SENSORS,
    ENTITY_DESC_KEY_ILLUMINANCE: ILLUMINANCE_SENSORS,
    ENTITY_DESC_KEY_POWER: POWER_SENSORS,
    ENTITY_DESC_KEY_PRESSURE: PRESSURE_SENSORS,
    ENTITY_DESC_KEY_SIGNAL_STRENGTH: SIGNAL_STRENGTH_SENSORS,
    ENTITY_DESC_KEY_TEMPERATURE: TEMPERATURE_SENSORS,
    ENTITY_DESC_KEY_VOLTAGE: VOLTAGE_SENSORS,
}

METER_UNIT_MAP: dict[str, set[MeterScaleType]] = {
    ELECTRIC_CURRENT_AMPERE: METER_UNIT_AMPERE,
    VOLUME_CUBIC_FEET: UNIT_CUBIC_FEET,
    VOLUME_CUBIC_METERS: METER_UNIT_CUBIC_METER,
    VOLUME_GALLONS: UNIT_US_GALLON,
    ENERGY_KILO_WATT_HOUR: UNIT_KILOWATT_HOUR,
    ELECTRIC_POTENTIAL_VOLT: METER_UNIT_VOLT,
    POWER_WATT: METER_UNIT_WATT,
}

MULTILEVEL_SENSOR_UNIT_MAP: dict[str, set[MultilevelSensorScaleType]] = {
    ELECTRIC_CURRENT_AMPERE: SENSOR_UNIT_AMPERE,
    POWER_BTU_PER_HOUR: UNIT_BTU_H,
    TEMP_CELSIUS: UNIT_CELSIUS,
    LENGTH_CENTIMETERS: UNIT_CENTIMETER,
    VOLUME_FLOW_RATE_CUBIC_FEET_PER_MINUTE: UNIT_CUBIC_FEET_PER_MINUTE,
    VOLUME_CUBIC_METERS: SENSOR_UNIT_CUBIC_METER,
    VOLUME_FLOW_RATE_CUBIC_METERS_PER_HOUR: UNIT_CUBIC_METER_PER_HOUR,
    SIGNAL_STRENGTH_DECIBELS: UNIT_DECIBEL,
    DEGREE: UNIT_DEGREES,
    CONCENTRATION_MICROGRAMS_PER_CUBIC_METER: {
        *UNIT_DENSITY,
        *UNIT_MICROGRAM_PER_CUBIC_METER,
    },
    TEMP_FAHRENHEIT: UNIT_FAHRENHEIT,
    LENGTH_FEET: UNIT_FEET,
    VOLUME_GALLONS: UNIT_GALLONS,
    FREQUENCY_HERTZ: UNIT_HERTZ,
    PRESSURE_INHG: UNIT_INCHES_OF_MERCURY,
    PRECIPITATION_INCHES_PER_HOUR: UNIT_INCHES_PER_HOUR,
    MASS_KILOGRAMS: UNIT_KILOGRAM,
    FREQUENCY_KILOHERTZ: UNIT_KILOHERTZ,
    VOLUME_LITERS: UNIT_LITER,
    LIGHT_LUX: UNIT_LUX,
    LENGTH_METERS: UNIT_METER,
    ELECTRIC_CURRENT_MILLIAMPERE: UNIT_MILLIAMPERE,
    PRECIPITATION_MILLIMETERS_PER_HOUR: UNIT_MILLIMETER_HOUR,
    ELECTRIC_POTENTIAL_MILLIVOLT: UNIT_MILLIVOLT,
    SPEED_MILES_PER_HOUR: UNIT_MPH,
    SPEED_METERS_PER_SECOND: UNIT_M_S,
    CONCENTRATION_PARTS_PER_MILLION: UNIT_PARTS_MILLION,
    PERCENTAGE: {*UNIT_PERCENTAGE_VALUE, *UNIT_RSSI},
    MASS_POUNDS: UNIT_POUNDS,
    PRESSURE_PSI: UNIT_POUND_PER_SQUARE_INCH,
    SIGNAL_STRENGTH_DECIBELS_MILLIWATT: UNIT_POWER_LEVEL,
    TIME_SECONDS: UNIT_SECOND,
    PRESSURE_MMHG: UNIT_SYSTOLIC,
    ELECTRIC_POTENTIAL_VOLT: SENSOR_UNIT_VOLT,
    POWER_WATT: SENSOR_UNIT_WATT,
    IRRADIATION_WATTS_PER_SQUARE_METER: UNIT_WATT_PER_SQUARE_METER,
}

_LOGGER = logging.getLogger(__name__)


@dataclass
class BaseDiscoverySchemaDataTemplate:
    """Base class for discovery schema data templates."""

    static_data: Any | None = None

    def resolve_data(self, value: ZwaveValue) -> Any:
        """
        Resolve helper class data for a discovered value.

        Can optionally be implemented by subclasses if input data needs to be
        transformed once discovered Value is available.
        """
        return {}

    def values_to_watch(self, resolved_data: Any) -> Iterable[ZwaveValue]:
        """
        Return list of all ZwaveValues resolved by helper that should be watched.

        Should be implemented by subclasses only if there are values to watch.
        """
        return []

    def value_ids_to_watch(self, resolved_data: Any) -> set[str]:
        """
        Return list of all Value IDs resolved by helper that should be watched.

        Not to be overwritten by subclasses.
        """
        return {val.value_id for val in self.values_to_watch(resolved_data) if val}

    @staticmethod
    def _get_value_from_id(
        node: ZwaveNode, value_id_obj: ZwaveValueID
    ) -> ZwaveValue | None:
        """Get a ZwaveValue from a node using a ZwaveValueDict."""
        value_id = get_value_id(
            node,
            value_id_obj.command_class,
            value_id_obj.property_,
            endpoint=value_id_obj.endpoint,
            property_key=value_id_obj.property_key,
        )
        return node.values.get(value_id)


@dataclass
class DynamicCurrentTempClimateDataTemplate(BaseDiscoverySchemaDataTemplate):
    """Data template class for Z-Wave JS Climate entities with dynamic current temps."""

    lookup_table: dict[str | int, ZwaveValueID] = field(default_factory=dict)
    dependent_value: ZwaveValueID | None = None

    def resolve_data(self, value: ZwaveValue) -> dict[str, Any]:
        """Resolve helper class data for a discovered value."""
        if not self.lookup_table or not self.dependent_value:
            raise ValueError("Invalid discovery data template")
        data: dict[str, Any] = {
            "lookup_table": {},
            "dependent_value": self._get_value_from_id(
                value.node, self.dependent_value
            ),
        }
        for key, value_id in self.lookup_table.items():
            data["lookup_table"][key] = self._get_value_from_id(value.node, value_id)

        return data

    def values_to_watch(self, resolved_data: dict[str, Any]) -> Iterable[ZwaveValue]:
        """Return list of all ZwaveValues resolved by helper that should be watched."""
        return [
            *resolved_data["lookup_table"].values(),
            resolved_data["dependent_value"],
        ]

    @staticmethod
    def current_temperature_value(resolved_data: dict[str, Any]) -> ZwaveValue | None:
        """Get current temperature ZwaveValue from resolved data."""
        lookup_table: dict[str | int, ZwaveValue | None] = resolved_data["lookup_table"]
        dependent_value: ZwaveValue | None = resolved_data["dependent_value"]

        if dependent_value and dependent_value.value is not None:
            lookup_key = dependent_value.metadata.states[
                str(dependent_value.value)
            ].split("-")[0]
            return lookup_table.get(lookup_key)

        return None


@dataclass
class NumericSensorDataTemplateData:
    """Class to represent returned data from NumericSensorDataTemplate."""

    entity_description_key: str | None = None
    unit_of_measurement: str | None = None


class NumericSensorDataTemplate(BaseDiscoverySchemaDataTemplate):
    """Data template class for Z-Wave Sensor entities."""

    @staticmethod
    def find_key_from_matching_set(
        enum_value: MultilevelSensorType | MultilevelSensorScaleType | MeterScaleType,
        set_map: dict[
            str, set[MultilevelSensorType | MultilevelSensorScaleType | MeterScaleType]
        ],
    ) -> str | None:
        """Find a key in a set map that matches a given enum value."""
        for key, value_set in set_map.items():
            for value_in_set in value_set:
                # Since these are IntEnums and the different classes reuse the same
                # values, we need to match the class as well
                if (
                    value_in_set.__class__ == enum_value.__class__
                    and value_in_set == enum_value
                ):
                    return key
        return None

    def resolve_data(self, value: ZwaveValue) -> NumericSensorDataTemplateData:
        """Resolve helper class data for a discovered value."""

        if value.command_class == CommandClass.BATTERY:
            return NumericSensorDataTemplateData(ENTITY_DESC_KEY_BATTERY, PERCENTAGE)

        if value.command_class == CommandClass.METER:
            scale_type = get_meter_scale_type(value)
            unit = self.find_key_from_matching_set(scale_type, METER_UNIT_MAP)
            # We do this because even though these are energy scales, they don't meet
            # the unit requirements for the energy device class.
            if scale_type in (
                ElectricScale.PULSE_COUNT,
                ElectricScale.KILOVOLT_AMPERE_HOUR,
                ElectricScale.KILOVOLT_AMPERE_REACTIVE_HOUR,
            ):
                return NumericSensorDataTemplateData(
                    ENTITY_DESC_KEY_TOTAL_INCREASING, unit
                )
            # We do this because even though these are power scales, they don't meet
            # the unit requirements for the power device class.
            if scale_type == ElectricScale.KILOVOLT_AMPERE_REACTIVE:
                return NumericSensorDataTemplateData(ENTITY_DESC_KEY_MEASUREMENT, unit)

            return NumericSensorDataTemplateData(
                self.find_key_from_matching_set(scale_type, METER_DEVICE_CLASS_MAP),
                unit,
            )

        if value.command_class == CommandClass.SENSOR_MULTILEVEL:
            sensor_type = get_multilevel_sensor_type(value)
            scale_type = get_multilevel_sensor_scale_type(value)
            unit = self.find_key_from_matching_set(
                scale_type, MULTILEVEL_SENSOR_UNIT_MAP
            )
            if sensor_type == MultilevelSensorType.TARGET_TEMPERATURE:
                return NumericSensorDataTemplateData(
                    ENTITY_DESC_KEY_TARGET_TEMPERATURE, unit
                )
            key = self.find_key_from_matching_set(
                sensor_type, MULTILEVEL_SENSOR_DEVICE_CLASS_MAP
            )
            if key:
                return NumericSensorDataTemplateData(key, unit)

        return NumericSensorDataTemplateData()


@dataclass
class TiltValueMix:
    """Mixin data class for the tilt_value."""

    tilt_value_id: ZwaveValueID


@dataclass
class CoverTiltDataTemplate(BaseDiscoverySchemaDataTemplate, TiltValueMix):
    """Tilt data template class for Z-Wave Cover entities."""

    def resolve_data(self, value: ZwaveValue) -> dict[str, ZwaveValue | None]:
        """Resolve helper class data for a discovered value."""
        return {"tilt_value": self._get_value_from_id(value.node, self.tilt_value_id)}

    def values_to_watch(self, resolved_data: dict[str, Any]) -> Iterable[ZwaveValue]:
        """Return list of all ZwaveValues resolved by helper that should be watched."""
        return [resolved_data["tilt_value"]]

    @staticmethod
    def current_tilt_value(
        resolved_data: dict[str, ZwaveValue | None]
    ) -> ZwaveValue | None:
        """Get current tilt ZwaveValue from resolved data."""
        return resolved_data["tilt_value"]


@dataclass
class FanValueMapping:
    """Data class to represent how a fan's values map to features."""

    presets: dict[int, str] = field(default_factory=dict)
    speeds: list[tuple[int, int]] = field(default_factory=list)

    def __post_init__(self) -> None:
        """
        Validate inputs.

        These inputs are hardcoded in `discovery.py`, so these checks should
        only fail due to developer error.
        """
        assert len(self.speeds) > 0, "At least one speed must be specified"
        for speed_range in self.speeds:
            (low, high) = speed_range
            assert high >= low, "Speed range values must be ordered"


@dataclass
class FanValueMappingDataTemplate:
    """Mixin to define `get_fan_value_mapping`."""

    def get_fan_value_mapping(
        self, resolved_data: dict[str, Any]
    ) -> FanValueMapping | None:
        """Get the value mappings for this device."""
        raise NotImplementedError


@dataclass
class ConfigurableFanValueMappingValueMix:
    """Mixin data class for defining fan properties that change based on a device configuration option."""

    configuration_option: ZwaveValueID
    configuration_value_to_fan_value_mapping: dict[int, FanValueMapping]


@dataclass
class ConfigurableFanValueMappingDataTemplate(
    BaseDiscoverySchemaDataTemplate,
    FanValueMappingDataTemplate,
    ConfigurableFanValueMappingValueMix,
):
    """
    Gets fan speeds based on a configuration value.

    Example:
      ZWaveDiscoverySchema(
          platform="fan",
          hint="has_fan_value_mapping",
          ...
          data_template=ConfigurableFanValueMappingDataTemplate(
            configuration_option=ZwaveValueID(
                property_=5, command_class=CommandClass.CONFIGURATION, endpoint=0
            ),
            configuration_value_to_fan_value_mapping={
                0: FanValueMapping(speeds=[(1,33), (34,66), (67,99)]),
                1: FanValueMapping(speeds=[(1,24), (25,49), (50,74), (75,99)]),
            },
          ),

    `configuration_option` is a reference to the setting that determines which
    value mapping to use (e.g., 3 speeds or 4 speeds).

    `configuration_value_to_fan_value_mapping` maps the values from
    `configuration_option` to the value mapping object.
    """

    def resolve_data(self, value: ZwaveValue) -> dict[str, ZwaveConfigurationValue]:
        """Resolve helper class data for a discovered value."""
        zwave_value: ZwaveValue = self._get_value_from_id(
            value.node, self.configuration_option
        )
        return {"configuration_value": zwave_value}

    def values_to_watch(self, resolved_data: dict[str, Any]) -> Iterable[ZwaveValue]:
        """Return list of all ZwaveValues that should be watched."""
        return [
            resolved_data["configuration_value"],
        ]

    def get_fan_value_mapping(
        self, resolved_data: dict[str, ZwaveConfigurationValue]
    ) -> FanValueMapping | None:
        """Get current fan properties from resolved data."""
        zwave_value: ZwaveValue = resolved_data["configuration_value"]

        if zwave_value is None:
            _LOGGER.warning("Unable to read device configuration value")
            return None

        if zwave_value.value is None:
            _LOGGER.warning("Fan configuration value is missing")
            return None

        fan_value_mapping = self.configuration_value_to_fan_value_mapping.get(
            zwave_value.value
        )
        if fan_value_mapping is None:
            _LOGGER.warning("Unrecognized fan configuration value")
            return None

        return fan_value_mapping


@dataclass
class FixedFanValueMappingValueMix:
    """Mixin data class for defining supported fan speeds."""

    fan_value_mapping: FanValueMapping


@dataclass
class FixedFanValueMappingDataTemplate(
    BaseDiscoverySchemaDataTemplate,
    FanValueMappingDataTemplate,
    FixedFanValueMappingValueMix,
):
    """
    Specifies a fixed set of properties for a fan.

    Example:
      ZWaveDiscoverySchema(
          platform="fan",
          hint="has_fan_value_mapping",
          ...
          data_template=FixedFanValueMappingDataTemplate(
              config=FanValueMapping(
                speeds=[(1, 32), (33, 65), (66, 99)]
              )
          ),
      ),
    """

    def get_fan_value_mapping(
        self, resolved_data: dict[str, ZwaveConfigurationValue]
    ) -> FanValueMapping:
        """Get the fan properties for this device."""
        return self.fan_value_mapping
