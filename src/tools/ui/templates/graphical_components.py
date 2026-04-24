
from prefab_ui.components.charts import  BarChart, ChartSeries,PieChart, LineChart, AreaChart, RadarChart, RadialChart
from prefab_ui.components import Column, Heading
from prefab_ui import PrefabApp


class GraphicalComponents:
    
    @staticmethod
    def pie_chart(
        data = dict[str,int]
    ) -> PrefabApp:
        series = [ChartSeries(name=key, value=value) for key, value in data.items()]
        pie_chart = PieChart(series=series)
        return PrefabApp(
            Column(
                Heading("Pie Chart"),
                pie_chart
            )
        )
    
    @staticmethod
    def bar_chart(
        data = list[dict[str, int]],
        x_axis: str = "x",
        series_keys: list[str] = ["y"]
    ) -> PrefabApp:
        
        chart_series = [ChartSeries(data_key=key, label=key) for key in series_keys]
        return PrefabApp(
            Column(
                Heading("Bar Chart"),
                BarChart(data=data, x_axis=x_axis, series=chart_series)
            )
        )
    
    @staticmethod
    def line_chart(
        data = list[dict[str, int]],
        x_axis: str = "x",
        series_keys: list[str] = ["y"]
    ) -> PrefabApp:

        chart_series = [ChartSeries(data_key=key, label=key) for key in series_keys]
        return PrefabApp(
            Column(
                Heading("Line Chart"),
                LineChart(data=data, x_axis=x_axis, series=chart_series)
            )
        )
    @staticmethod
    def area_chart(
        data = list[dict[str, int]],
        x_axis: str = "x",
        series_keys: list[str] = ["y"]
    ) -> PrefabApp:

        chart_series = [ChartSeries(data_key=key, label=key) for key in series_keys]
        return PrefabApp(
            Column(
                Heading("Area Chart"),
                AreaChart(data=data, x_axis=x_axis, series=chart_series)
            )
        )
    @staticmethod
    def radar_chart(
        data = list[dict[str, int]],
        x_axis: str = "x",
        series_keys: list[str] = ["y"]
    ) -> PrefabApp:

        chart_series = [ChartSeries(data_key=key, label=key) for key in series_keys]
        return PrefabApp(
            Column(
                Heading("Radar Chart"),
                RadarChart(data=data, x_axis=x_axis, series=chart_series)
            )
        )
    
    @staticmethod
    def radial_chart(
        data = list[dict[str, int]],
        x_axis: str = "x",
        series_keys: list[str] = ["y"]
    ) -> PrefabApp:

        chart_series = [ChartSeries(data_key=key, label=key) for key in series_keys]
        return PrefabApp(
            Column(
                Heading("Radial Chart"),
                RadialChart(data=data, x_axis=x_axis, series=chart_series)
            )
        )
    
        