"""
Minimal usage example for flexoki_plotly.

Run from the repo root:
    python examples/demo.py
"""

import sys
from pathlib import Path

# Allow running this example without installing the package.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import plotly.graph_objects as go
import flexoki_plotly  # noqa: F401  (registers the templates on import)

x = ["Mon", "Tue", "Wed", "Thu", "Fri"]
fig = go.Figure()
for i, name in enumerate(["reads", "writes", "errors"]):
    fig.add_trace(go.Scatter(x=x, y=[3 + i, 5 + i, 4 + i, 6 + i, 5 + i], name=name, mode="lines+markers"))

fig.update_layout(template="flexoki_light", title="Flexoki Light")
fig.write_html("flexoki_light_demo.html")
print("Wrote flexoki_light_demo.html")

fig.update_layout(template="flexoki_dark", title="Flexoki Dark")
fig.write_html("flexoki_dark_demo.html")
print("Wrote flexoki_dark_demo.html")
