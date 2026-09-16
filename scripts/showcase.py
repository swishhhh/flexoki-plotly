"""
Show common Plotly chart types with the Flexoki theme.

Run from the repository root:
    python scripts/showcase.py --output docs/showcase
"""

import argparse
import json
import sys
from pathlib import Path

import plotly.graph_objects as go
from plotly.utils import PlotlyJSONEncoder

# Allow running this example without installing the package.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import flexoki_plotly  # noqa: F401  (registers the templates)


def build_showcase() -> dict[str, go.Figure]:
    """Build one independent figure for each common chart type."""
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
    revenue = [42, 48, 45, 58, 64, 72]
    costs = [31, 35, 34, 39, 43, 46]
    figures = {
        "line": go.Figure(go.Scatter(x=months, y=revenue, mode="lines+markers", name="Revenue")),
        "bar": go.Figure(
            [
                go.Bar(x=months, y=revenue, name="Revenue"),
                go.Bar(x=months, y=costs, name="Costs"),
            ]
        ),
        "area": go.Figure(go.Scatter(x=months, y=revenue, fill="tozeroy", mode="lines", name="Revenue")),
        "scatter": go.Figure(
            go.Scatter(
                x=[8, 10, 11, 13, 14, 17, 18, 21],
                y=[18, 15, 17, 12, 14, 10, 13, 8],
                mode="markers",
                marker=dict(size=10),
                name="Observations",
            )
        ),
        "histogram": go.Figure(go.Histogram(x=[12, 14, 15, 15, 16, 17, 18, 18, 19, 21, 22], name="Values")),
        "box": go.Figure(go.Box(y=[31, 35, 34, 39, 43, 46, 52, 57], name="Costs", boxmean=True)),
        "pie": go.Figure(go.Pie(labels=["Product", "Services", "Other"], values=[55, 30, 15], name="Mix")),
        "heatmap": go.Figure(
            go.Heatmap(
                z=[[3, 5, 4, 6], [4, 6, 5, 7], [2, 4, 3, 5]],
                x=["Q1", "Q2", "Q3", "Q4"],
                y=["North", "Central", "South"],
                name="Activity",
            )
        ),
    }

    for chart_name, figure in figures.items():
        figure.update_layout(
            height=500, showlegend=chart_name in {"bar", "pie"})
        figure.update_xaxes(showgrid=False)
        figure.update_yaxes(showgrid=True)
    return figures


def render_chart(chart_name: str, figure: go.Figure) -> str:
    themes = {}
    for theme in ("flexoki_light", "flexoki_dark"):
        themed_figure = go.Figure(figure)
        themed_figure.update_layout(
            template=theme,
            title=f"Flexoki {theme.removeprefix('flexoki_').title()} - {chart_name.title()} Chart",
        )
        themes[theme.removeprefix("flexoki_")] = themed_figure.to_plotly_json()[
            "layout"]

    chart_data = json.dumps(figure.to_plotly_json()[
                            "data"], cls=PlotlyJSONEncoder)
    theme_json = json.dumps(themes, cls=PlotlyJSONEncoder)
    chart_id = f"flexoki_{chart_name}"
    return f"""<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Flexoki {chart_name.title()} Chart</title>
    <style>html, body {{ margin: 0; overflow: hidden; }} #chart {{ width: 100%; }}</style>
</head>
<body>
    <div id="{chart_id}" style="height:500px; width:100%;"></div>
    <script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>
    <script>
        const chartData = {chart_data};
        const themes = {theme_json};
        const chart = document.getElementById("{chart_id}");
        const systemTheme = window.matchMedia("(prefers-color-scheme: dark)");
        let activeTheme = systemTheme.matches ? "dark" : "light";

        function setTheme(theme) {{
            activeTheme = theme === "dark" ? "dark" : "light";
            Plotly.react(chart, chartData, themes[activeTheme], {{responsive: true}});
        }}

        window.addEventListener("message", (event) => {{
            if (event.source === window.parent && event.data?.type === "flexoki-theme") {{
                setTheme(event.data.theme);
            }}
        }});

        systemTheme.addEventListener("change", (event) => {{
            if (window.parent === window) setTheme(event.matches ? "dark" : "light");
        }});

        setTheme(activeTheme);
    </script>
</body>
</html>
"""


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("."),
                        help="Directory for the HTML files")
    args = parser.parse_args()

    args.output.mkdir(parents=True, exist_ok=True)
    for old_output in args.output.glob("flexoki_*_*.html"):
        old_output.unlink()
    for chart_name, figure in build_showcase().items():
        html_output = args.output / f"{chart_name}.html"
        html_output.write_text(render_chart(
            chart_name, figure), encoding="utf-8")
        print(f"Wrote {html_output}")


if __name__ == "__main__":
    main()
