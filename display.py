from datetime import datetime
from rich.table import Table
from rich import box
from rich.text import Text
from config import (
    TEMP_NORMAL_MAX,
    TEMP_WARM_MAX,
    TEMP_HOT_MAX,
)


def get_temperature_status(temp):
    '''Return the status and color for a given temperature.'''

    if temp < TEMP_NORMAL_MAX:
        return "NORMAL", "green"

    if temp < TEMP_WARM_MAX:
        return "WARM", "yellow"

    if temp < TEMP_HOT_MAX:
        return "HOT", "dark_orange"

    return "CRITICAL", "bold red"


def format_temperature(temp):
    '''Return a formatted temperature string with an appropriate color.'''

    status, color = get_temperature_status(temp)

    temperature = Text()
    temperature.append(f"{temp:.1f}°C", style=f"bold {color}")

    return temperature


def format_status(temp):
    '''Return a colored temperature status indicator.'''

    status, color = get_temperature_status(temp)

    result = Text()
    result.append("● ", style=color)
    result.append(status, style=f"bold {color}")

    return result


def create_device_table(dev_temps):
    '''Create a table containing device temperatures and statuses.'''

    table = Table(
        box=box.ROUNDED,
        border_style="bright_black",
        expand=False,
        padding=(0, 2),
    )

    table.add_column(
        "DEVICE",
        justify="left",
        style="bold white",
        no_wrap=True,
    )

    table.add_column(
        "TEMPERATURE",
        justify="right",
        no_wrap=True,
    )

    table.add_column(
        "STATUS",
        justify="left",
        no_wrap=True,
    )

    for device, temp in dev_temps.items():
        dev_name = device.replace(" ", "_").replace("/dev/", "")

        table.add_row(
            dev_name,
            format_temperature(temp),
            format_status(temp),
        )

    return table


def create_summary(dev_temps):
    '''Create a summary table containing average and maximum temperature.'''

    if not dev_temps:
        return Table()

    temperatures = list(dev_temps.values())

    average_temp = sum(temperatures) / len(temperatures)
    maximum_temp = max(temperatures)

    max_device = next(
        device
        for device, temp in dev_temps.items()
        if temp == maximum_temp
    )

    max_device = max_device.replace(" ", "_").replace("/dev/", "")

    table = Table(
        box=box.SIMPLE,
        show_header=False,
        padding=(0, 2),
        expand=False,
    )

    table.add_column(style="dim")
    table.add_column(justify="right")

    table.add_row(
        "Average",
        format_temperature(average_temp),
    )

    table.add_row(
        "Maximum",
        format_temperature(maximum_temp),
    )

    table.add_row(
        "Max device",
        Text(max_device, style="bold white"),
    )

    return table


def render(dev_temps):
    '''Return the complete temperature display as a Rich Group.'''

    if not dev_temps:
        return Text("No temperature data available.", style="yellow")

    current_time = datetime.now().strftime("%H:%M:%S")

    header = Text()
    header.append("DEVICE TEMPERATURE\n", style="bold cyan")
    header.append(
        f"Last update: {current_time}",
        style="dim",
    )
    
    device_table = create_device_table(dev_temps)

    summary = create_summary(dev_temps)

    from rich.console import Group

    return Group(
        header,
        "",
        device_table,
        "",
        summary,
    )
