from pathlib import Path
from math import cos, sin, pi

from newsflash import App, Page
from newsflash.widgets import LineChart, Select
from newsflash.widgets.widgets import Widget


class DemoBar(LineChart):
    id: str = "line-chart"
    title: str = "sine wave"

    def set_title(self, line_type: str) -> None:
        self.title = f"{line_type} wave"

    def get_y_value(self, line_type: str, x: float, amplitude: int) -> float:
        if line_type == "sine":
            return sin(x) * amplitude
        elif line_type == "cosine":
            return cos(x) * amplitude
        else:
            raise ValueError(f"Unknown line type: {line_type}")

    def on_load(
        self,
        line_type_select: "LineTypeSelect",
        amplitude_select: "AmplitudeSelect",
        num_periods_select: "NumPeriodsSelect",
    ) -> list[Widget]:
        assert line_type_select.selected is not None
        assert amplitude_select.selected is not None
        assert num_periods_select.selected is not None

        num_periods_selected = int(num_periods_select.selected)

        self.set_title(line_type=line_type_select.selected)

        x_values = [
            i / 100 for i in range(int((num_periods_selected * 2 + 0.2) * pi * 100))
        ]

        y_values = [
            self.get_y_value(
                line_type=line_type_select.selected,
                x=x,
                amplitude=int(amplitude_select.selected),
            )
            for x in x_values
        ]

        x_labels = {
            **{
                i * pi: f"{i}π"
                for i in range(
                    0, num_periods_selected * 2 + 1, num_periods_selected // 2
                )
            },
        }
        self.set_values(xs=x_values, ys=y_values, x_labels=x_labels)
        return [self]


class AmplitudeSelect(Select):
    id: str = "amplitude-select"
    options: list[str] = ["2", "5", "10", "400", "10000"]

    def on_select(
        self,
        demo_bar_chart: DemoBar,
        line_type_select: "LineTypeSelect",
        num_periods_select: "NumPeriodsSelect",
    ) -> list[Widget]:
        demo_bar_chart.on_load(
            line_type_select=line_type_select,
            amplitude_select=self,
            num_periods_select=num_periods_select,
        )
        return [demo_bar_chart]


class NumPeriodsSelect(Select):
    id: str = "num-periods-select"
    options: list[str] = ["2", "3", "6", "9", "25"]

    def on_select(
        self,
        demo_bar_chart: DemoBar,
        line_type_select: "LineTypeSelect",
        amplitude_select: AmplitudeSelect,
    ) -> list[Widget]:
        demo_bar_chart.on_load(
            line_type_select=line_type_select,
            amplitude_select=amplitude_select,
            num_periods_select=self,
        )
        return [demo_bar_chart]


class LineTypeSelect(Select):
    id: str = "line-type-select"
    options: list[str] = ["sine", "cosine"]

    def on_select(
        self,
        demo_bar_chart: DemoBar,
        amplitude_select: "AmplitudeSelect",
        num_periods_select: "NumPeriodsSelect",
    ) -> list[Widget]:
        demo_bar_chart.on_load(
            line_type_select=self,
            amplitude_select=amplitude_select,
            num_periods_select=num_periods_select,
        )
        return [demo_bar_chart]


home_page = Page(
    id="/",
    path="/",
    title="newsflash docs",
    template=("templates", "home.html"),
    children=[
        DemoBar(),
        AmplitudeSelect(),
        LineTypeSelect(),
        NumPeriodsSelect(),
    ],
)

app = App(
    pages=[home_page],
    template_folders=[("templates", Path.cwd() / "templates")],
)
