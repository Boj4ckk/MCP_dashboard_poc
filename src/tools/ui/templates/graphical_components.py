
from prefab_ui.components.charts import BarChart, ChartSeries, PieChart, LineChart, AreaChart, RadarChart, RadialChart
from prefab_ui.components import Column, Heading
from prefab_ui import PrefabApp


class GraphicalComponents:

    @staticmethod
    def pie_chart(
        data: list[dict],
        data_key: str = "value",
        name_key: str = "name",
    ) -> PrefabApp:
        return PrefabApp(view=Column(children=[
            Heading("Pie Chart"),
            PieChart(data=data, data_key=data_key, name_key=name_key),
        ]))

    @staticmethod
    def bar_chart(
        data: list[dict],
        x_axis: str = "x",
        series_keys: list[str] = ["y"],
    ) -> PrefabApp:
        chart_series = [ChartSeries(data_key=key, label=key) for key in series_keys]
        return PrefabApp(view=Column(children=[
            Heading("Bar Chart"),
            BarChart(data=data, x_axis=x_axis, series=chart_series),
        ]))

    @staticmethod
    def line_chart(
        data: list[dict],
        x_axis: str = "x",
        series_keys: list[str] = ["y"],
    ) -> PrefabApp:
        chart_series = [ChartSeries(data_key=key, label=key) for key in series_keys]
        return PrefabApp(view=Column(children=[
            Heading("Line Chart"),
            LineChart(data=data, x_axis=x_axis, series=chart_series),
        ]))

    @staticmethod
    def area_chart(
        data: list[dict],
        x_axis: str = "x",
        series_keys: list[str] = ["y"],
    ) -> PrefabApp:
        chart_series = [ChartSeries(data_key=key, label=key) for key in series_keys]
        return PrefabApp(view=Column(children=[
            Heading("Area Chart"),
            AreaChart(data=data, x_axis=x_axis, series=chart_series),
        ]))

    @staticmethod
    def radar_chart(
        data: list[dict],
        axis_key: str = "x",
        series_keys: list[str] = ["y"],
    ) -> PrefabApp:
        chart_series = [ChartSeries(data_key=key, label=key) for key in series_keys]
        return PrefabApp(view=Column(children=[
            Heading("Radar Chart"),
            RadarChart(data=data, axis_key=axis_key, series=chart_series),
        ]))

    @staticmethod
    def radial_chart(
        data: list[dict],
        data_key: str = "value",
        name_key: str = "name",
    ) -> PrefabApp:
        return PrefabApp(view=Column(children=[
            Heading("Radial Chart"),
            RadialChart(data=data, data_key=data_key, name_key=name_key),
        ]))
