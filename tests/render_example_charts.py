import argparse
from pathlib import Path

import plotly.graph_objects as go

import flexoki_plotly


def _build_example_figure(template_name: str) -> go.Figure:
    x = ["Mon", "Tue", "Wed", "Thu", "Fri"]
    fig = go.Figure()
    for i, name in enumerate(["reads", "writes", "errors"]):
        fig.add_trace(go.Scatter(
            x=x, y=[3 + i, 5 + i, 4 + i, 6 + i, 5 + i], name=name, mode="lines+markers"))

    fig.update_layout(
        template=template_name,
        title=f"Flexoki {template_name.replace('flexoki_', '').title()} Example",
        xaxis_title="Day",
        yaxis_title="Value",
        height=600,
        width=900,
    )
    return fig


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Render example Plotly charts to PNG for visual review."
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(__file__).resolve(
        ).parents[1] / "docs" / "assets" / "images",
        help="Directory where PNG files will be written.",
    )
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)

    for template_name in ("flexoki_light", "flexoki_dark"):
        output = args.output_dir / f"{template_name}.png"
        fig = _build_example_figure(template_name)
        fig.write_image(output, scale=2)
        print(f"Wrote {output}")


if __name__ == "__main__":
    main()
