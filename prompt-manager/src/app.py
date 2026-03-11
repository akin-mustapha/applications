import dash
from dash import dcc, html

from src.config import API_BASE_URL  # noqa: F401

app = dash.Dash(__name__)

app.layout = html.Div(
    style={"display": "flex", "height": "100vh", "flexDirection": "column"},
    children=[
        # Stores
        dcc.Store(id="selected-id"),
        dcc.Store(id="selected-type"),
        dcc.Store(id="mode"),
        # Download
        dcc.Download(id="download"),
        # Main area: center + sidebar
        html.Div(
            style={"display": "flex", "flex": "1", "overflow": "hidden"},
            children=[
                # Center pane: editor + preview
                html.Div(
                    style={"display": "flex", "flex": "1", "overflow": "hidden"},
                    children=[
                        dcc.Textarea(
                            id="editor",
                            style={"flex": "1", "resize": "none", "fontFamily": "monospace"},
                            placeholder="Write your prompt in Markdown...",
                        ),
                        dcc.Markdown(
                            id="preview",
                            style={"flex": "1", "overflowY": "auto", "padding": "8px"},
                        ),
                    ],
                ),
                # Right sidebar
                html.Div(
                    style={"width": "260px", "display": "flex", "flexDirection": "column", "padding": "8px", "borderLeft": "1px solid #ccc"},
                    children=[
                        dcc.Input(
                            id="search-input",
                            type="text",
                            placeholder="Search...",
                            debounce=True,
                            style={"width": "100%", "marginBottom": "8px"},
                        ),
                        dcc.RadioItems(
                            id="sidebar-toggle",
                            options=[
                                {"label": "Prompts", "value": "prompts"},
                                {"label": "Templates", "value": "templates"},
                            ],
                            value="prompts",
                            inline=True,
                            style={"marginBottom": "8px"},
                        ),
                        html.Div(id="list-area", style={"flex": "1", "overflowY": "auto"}),
                        html.Button("New Prompt", id="btn-new-prompt", style={"marginTop": "8px"}),
                        html.Button("New Template", id="btn-new-template", style={"marginTop": "4px"}),
                    ],
                ),
            ],
        ),
        # Bottom pane
        html.Div(
            style={"height": "220px", "padding": "8px", "borderTop": "1px solid #ccc", "display": "flex", "gap": "8px"},
            children=[
                html.Div(
                    style={"flex": "1", "display": "flex", "flexDirection": "column", "gap": "4px"},
                    children=[
                        dcc.Input(id="input-name", type="text", placeholder="Name", style={"width": "100%"}),
                        dcc.Textarea(id="input-description", placeholder="Description", style={"width": "100%", "resize": "none"}),
                        dcc.Input(id="input-tags", type="text", placeholder="Tags (comma-separated)", style={"width": "100%"}),
                        html.Div(id="variable-form", style={"display": "none"}),
                    ],
                ),
                html.Div(
                    style={"display": "flex", "flexDirection": "column", "justifyContent": "flex-end", "gap": "4px"},
                    children=[
                        dcc.RadioItems(
                            id="export-format",
                            options=[
                                {"label": "md", "value": "md"},
                                {"label": "yaml", "value": "yaml"},
                                {"label": "json", "value": "json"},
                            ],
                            value="md",
                            inline=True,
                        ),
                        html.Button("Export", id="btn-export"),
                        html.Button("Save", id="btn-save"),
                        html.Button("Delete", id="btn-delete"),
                    ],
                ),
            ],
        ),
    ],
)

if __name__ == "__main__":
    app.run(debug=True)
