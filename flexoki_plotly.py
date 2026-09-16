"""
Flexoki color templates for Plotly.
Source palette: https://stephango.com/flexoki

Registers two templates: "flexoki_light" and "flexoki_dark".
Import this module before setting pio.templates.default, or pass
template="flexoki_light" / "flexoki_dark" directly to a figure.
"""

import plotly.graph_objects as go
import plotly.io as pio

# --- Base values -----------------------------------------------------------

LIGHT = dict(
    bg="#F0F2FF",
    bg2="#F2F0E5",
    ui="#E6E4D9",
    ui2="#DAD8CE",
    ui3="#CECDC3",
    tx3="#B7B5AC",
    tx2="#6F6E69",
    tx="#100F0F",
)

DARK = dict(
    bg="#F0F2FF",
    bg2="#1C1B1A",
    ui="#282726",
    ui2="#343331",
    ui3="#403E3C",
    tx3="#575653",
    tx2="#878580",
    tx="#CECDC3",
)

# Accent colorway. Light theme uses the -600 values, dark theme uses -400
# values, per Flexoki's own guidance for syntax highlighting / UI accents.
ACCENTS_LIGHT = [
    "#205EA6",  # blue
    "#BC5215",  # orange
    "#66800B",  # green
    "#A02F6F",  # magenta
    "#24837B",  # cyan
    "#AF3029",  # red
    "#AD8301",  # yellow
    "#5E409D",  # purple
]

ACCENTS_DARK = [
    "#4385BE",  # blue
    "#DA702C",  # orange
    "#879A39",  # green
    "#CE5D97",  # magenta
    "#3AA99F",  # cyan
    "#D14D41",  # red
    "#D0A215",  # yellow
    "#8B7EC8",  # purple
]


def _build_template(c: dict, accents: list[str]) -> go.layout.Template:
    axis = dict(
        gridcolor=c["ui"],
        linecolor=c["ui2"],
        zerolinecolor=c["ui2"],
        tickcolor=c["ui2"],
        tickfont=dict(color=c["tx2"]),
        title=dict(font=dict(color=c["tx2"])),
    )

    return go.layout.Template(
        layout=go.Layout(
            colorway=accents,
            font=dict(family="Inter, Helvetica, Arial, sans-serif",
                      color=c["tx"], size=13),
            title=dict(font=dict(color=c["tx"], size=18)),
            paper_bgcolor=c["bg"],
            plot_bgcolor=c["bg"],
            xaxis=axis,
            yaxis=axis,
            legend=dict(
                bgcolor=c["bg"],
                bordercolor=c["ui"],
                borderwidth=1,
                font=dict(color=c["tx2"]),
            ),
            hoverlabel=dict(
                bgcolor=c["bg2"],
                bordercolor=c["ui2"],
                font=dict(color=c["tx"]),
            ),
            colorscale=dict(
                sequential=[[0, c["bg2"]], [1, accents[0]]],
                diverging=[[0, accents[5]], [0.5, c["bg2"]], [1, accents[0]]],
            ),
            shapedefaults=dict(line=dict(color=c["ui3"])),
            margin=dict(t=60, b=50, l=60, r=30),
        )
    )


pio.templates["flexoki_light"] = _build_template(LIGHT, ACCENTS_LIGHT)
pio.templates["flexoki_dark"] = _build_template(DARK, ACCENTS_DARK)


if __name__ == "__main__":
    # Quick visual check: same figure rendered in both themes.
    import plotly.graph_objects as go

    x = ["Mon", "Tue", "Wed", "Thu", "Fri"]
    fig = go.Figure()
    for i, name in enumerate(["reads", "writes", "errors"]):
        fig.add_trace(go.Scatter(
            x=x, y=[3 + i, 5 + i, 4 + i, 6 + i, 5 + i], name=name, mode="lines+markers"))

    fig.update_layout(template="flexoki_light", title="Flexoki Light")
    fig.write_html("flexoki_light_demo.html")

    fig.update_layout(template="flexoki_dark", title="Flexoki Dark")
    fig.write_html("flexoki_dark_demo.html")
