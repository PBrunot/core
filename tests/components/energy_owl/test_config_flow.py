"""Test the cm160 config flow."""

from unittest.mock import AsyncMock, patch

from homeassistant import config_entries
from homeassistant.components.energy_owl.config_flow import CannotConnect
from homeassistant.components.energy_owl.const import DOMAIN
from homeassistant.const import CONF_PORT
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResultType


async def test_form(hass: HomeAssistant, mock_setup_entry: AsyncMock) -> None:
    """Test we get the form."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] == FlowResultType.FORM
    assert result["errors"] == {}

    with patch(
        "homeassistant.components.energy_owl.config_flow.EnergyOwlHub.connect",
        return_value=True,
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                CONF_PORT: "test",
            },
        )
        await hass.async_block_till_done()

    assert result["type"] == FlowResultType.CREATE_ENTRY
    assert result["title"] == "Energy OWL - CM160"
    assert result["data"] == {CONF_PORT: "test"}
    assert len(mock_setup_entry.mock_calls) == 1


async def test_form_cannot_connect(
    hass: HomeAssistant, mock_setup_entry: AsyncMock
) -> None:
    """Test we handle cannot connect error."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch(
        "homeassistant.components.energy_owl.config_flow.EnergyOwlHub.connect",
        side_effect=CannotConnect,
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                CONF_PORT: "/dev/fake",
            },
        )

    assert result["type"] == FlowResultType.FORM
    assert result["errors"] == {"base": "cannot_connect"}

    # Make sure the config flow tests finish with either an
    # FlowResultType.CREATE_ENTRY or FlowResultType.ABORT so
    # we can show the config flow is able to recover from an error.

    with patch(
        "homeassistant.components.energy_owl.config_flow.EnergyOwlHub.connect",
        return_value=True,
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                CONF_PORT: "test",
            },
        )
        await hass.async_block_till_done()

    assert result["type"] == FlowResultType.CREATE_ENTRY
    assert result["title"] == "Energy OWL - CM160"
    assert result["data"] == {
        CONF_PORT: "test",
    }
    assert len(mock_setup_entry.mock_calls) == 1
