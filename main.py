from pathlib import Path
from math import cos, sin, pi

from newsflash import App, Page
from newsflash.widgets import LineChart, Button, Select
from newsflash.widgets.widgets import Widget


class DemoBar(LineChart):
    id: str = "line-chart"
    title: str = "sine wave"

    amplitude: int = 2
    line_type: str = "sine"

    def set_title(self) -> None:
        self.title = f"{self.line_type} wave"

    def get_y_value(self, x: float) -> float:
        if self.line_type == "sine":
            return sin(x)*self.amplitude
        elif self.line_type == "cosine":
            return cos(x)*self.amplitude
        else:
            raise ValueError(f"Unknown line type: {self.line_type}")

    def on_load(self) -> list[Widget]:
        self.set_title()

        x_values = [i / 100 for i in range(1000)]
        y_values = [self.get_y_value(x) for x in x_values]

        x_labels = {
            0: "0",
            pi: "π",
            2*pi: "2π",
            3*pi: "3π",
        }
        self.set_values(
            xs=x_values, 
            ys=y_values, 
            x_labels=x_labels
        )
        return [self]
    

class SineButton(Button):
    id: str = "sine-button"
    label: str = "show sine wave"

    def on_click(self) -> list[Widget]:
        return []
    

class AmplitudeSelect(Select):
    id: str = "amplitude-select"
    options: list[str] = ["2", "5", "10", "500", "10000"]

    def on_select(self, demo_bar_chart: DemoBar) -> list[Widget]:
        assert self.selected is not None
        demo_bar_chart.amplitude = int(self.selected)
        demo_bar_chart.on_load()
        return [demo_bar_chart]


class LineTypeSelect(Select):
    id: str = "line-type-select"
    options: list[str] = ["sine", "cosine"]

    def on_select(self, demo_bar_chart: DemoBar) -> list[Widget]:
        assert self.selected is not None
        demo_bar_chart.line_type = self.selected
        demo_bar_chart.on_load()
        return [demo_bar_chart]


home_page = Page(
    id="/",
    path="/",
    title="newsflash docs",
    template=("templates", "home.html"),
    children=[
        DemoBar(),
        SineButton(),
        AmplitudeSelect(),
        LineTypeSelect(),
    ],
)

app = App(
    pages=[home_page],
    template_folders=[
        ("templates", Path.cwd() / "templates")
    ],
)
