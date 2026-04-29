from typing import Optional, List, Dict, Any
from fastmcp import FastMCP
from src.tools.ui.templates.graphical_components import GraphicalComponents

charts_mcp = FastMCP("Charts")


@charts_mcp.tool(description="Generate a chart from data")
def generate_chart(
    data: List[Dict[str, Any]],
    chart_type: str,
    x_axis: Optional[str] = None,
    series_keys: Optional[List[str]] = None,
    data_key: Optional[str] = None,
    name_key: Optional[str] = None,
):
    """
    Génère un graphique à partir de données structurées.

    Args:
        data: Liste de dictionnaires contenant les données
        chart_type: Type de graphique ('bar', 'line', 'pie', 'area', 'radar', 'radial')
        x_axis: Colonne pour l'axe X — requis pour bar, line, area
        series_keys: Colonnes numériques à visualiser — requis pour bar, line, area, radar
        data_key: Colonne numérique — requis pour pie et radial
        name_key: Colonne label — requis pour pie et radial

    Returns:
        PrefabApp: Composant UI avec le graphique
    """

    if not data:
        return {"error": "Données vides"}

    if chart_type == "pie":
        if not data_key or not name_key:
            return {"error": "Pie chart nécessite data_key et name_key"}
        app = GraphicalComponents.pie_chart(data=data, data_key=data_key, name_key=name_key)

    elif chart_type == "radial":
        if not data_key or not name_key:
            return {"error": "Radial chart nécessite data_key et name_key"}
        app = GraphicalComponents.radial_chart(data=data, data_key=data_key, name_key=name_key)

    elif chart_type == "radar":
        app = GraphicalComponents.radar_chart(
            data=data,
            axis_key=x_axis or "x",
            series_keys=series_keys or ["y"]
        )

    else:
        chart_map = {
            "bar": GraphicalComponents.bar_chart,
            "line": GraphicalComponents.line_chart,
            "area": GraphicalComponents.area_chart,
        }

        if chart_type not in chart_map:
            return {"error": f"Type non supporté: {chart_type}. Disponibles: bar, line, area, pie, radar, radial"}

        app = chart_map[chart_type](
            data=data,
            x_axis=x_axis or "x",
            series_keys=series_keys or ["y"]
        )

    return app.html()
