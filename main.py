from typing import Annotated
from pathlib import Path
from math import cos, sin, pi

from newsflash import App, Page
from newsflash.widgets import LineChart, Select
from newsflash.widgets.widgets import Widget
from newsflash.svg.element import TemplateParam


class DemoBar(LineChart):
    id: Annotated[str, TemplateParam()] = "line-chart"
    title: Annotated[str, TemplateParam()] = "sine wave"

    def set_title(self, line_type: str) -> None:
        self.title = f"{line_type} wave"

    def get_y_values(
        self, line_type: str, x_values: list[float], amplitude: int
    ) -> list[float]:
        if line_type == "sine":
            return [sin(x) * amplitude for x in x_values]
        elif line_type == "cosine":
            return [cos(x) * amplitude for x in x_values]
        else:
            raise ValueError(f"Unknown line type: {line_type}")

    def on_load(
        self,
        line_type_select: "LineTypeSelect",
        amplitude_select: "AmplitudeSelect",
        num_periods_select: "NumPeriodsSelect",
    ) -> list[Widget]:
        line_type = line_type_select.selected
        amplitude = amplitude_select.selected
        num_periods = num_periods_select.selected

        assert line_type is not None
        assert amplitude is not None
        assert num_periods is not None

        num_periods = int(num_periods)
        amplitude = int(amplitude)

        self.set_title(line_type=line_type)

        x_values = [i / 15 for i in range(int((num_periods * 2 + 0.2) * pi * 15))]

        y_values = self.get_y_values(
            line_type=line_type,
            x_values=x_values,
            amplitude=amplitude,
        )

        x_labels = {
            i * pi: f"{i}π" for i in range(0, num_periods * 2 + 1, num_periods // 2)
        }
        self.set_values(xs=x_values, ys=y_values, x_labels=x_labels)
        return [self]


class AmplitudeSelect(Select):
    id: Annotated[str, TemplateParam()] = "amplitude-select"
    options: Annotated[list[str], TemplateParam()] = ["2", "5", "10", "400", "10000"]

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
    id: Annotated[str, TemplateParam()] = "num-periods-select"
    options: Annotated[list[str], TemplateParam()] = ["2", "3", "7", "11", "25"]

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
    id: Annotated[str, TemplateParam()] = "line-type-select"
    options: Annotated[list[str], TemplateParam()] = ["sine", "cosine"]

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


class HomePage(Page):
    id: str = "/"
    path: str = "/"
    title: str = "newsflash docs"
    template: tuple[str, str] = ("templates", "home.html")

    def compose(self) -> list[Widget]:
        return [
            DemoBar(),
            AmplitudeSelect(),
            LineTypeSelect(),
            NumPeriodsSelect(),
        ]


app = App(
    pages=[HomePage()],
    template_folders=[("templates", Path.cwd() / "templates")],
)
