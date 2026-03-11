import dash
import requests
from dash import ALL, Input, Output, State, ctx, dcc, html

from src.config import API_BASE_URL

app = dash.Dash(__name__)

app.layout = html.Div(
    style={"display": "flex", "height": "100vh", "flexDirection": "column"},
    children=[
        # Stores
        dcc.Store(id="selected-id"),
        dcc.Store(id="selected-type"),
        dcc.Store(id="mode"),
        dcc.Store(id="list-refresh", data=0),
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
                    style={
                        "width": "260px",
                        "display": "flex",
                        "flexDirection": "column",
                        "padding": "8px",
                        "borderLeft": "1px solid #ccc",
                    },
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
            style={
                "height": "220px",
                "padding": "8px",
                "borderTop": "1px solid #ccc",
                "display": "flex",
                "gap": "8px",
            },
            children=[
                html.Div(
                    style={"flex": "1", "display": "flex", "flexDirection": "column", "gap": "4px"},
                    children=[
                        dcc.Input(id="input-name", type="text", placeholder="Name", style={"width": "100%"}),
                        dcc.Textarea(
                            id="input-description",
                            placeholder="Description",
                            style={"width": "100%", "resize": "none"},
                        ),
                        dcc.Input(
                            id="input-tags",
                            type="text",
                            placeholder="Tags (comma-separated)",
                            style={"width": "100%"},
                        ),
                        html.Div(id="variable-form", style={"display": "none"}),
                    ],
                ),
                html.Div(
                    style={
                        "display": "flex",
                        "flexDirection": "column",
                        "justifyContent": "flex-end",
                        "gap": "4px",
                    },
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


# --- Helpers ---


def _prompt_list_items(q: str | None) -> list:
    """Fetch prompts from API and return a list of sidebar button components."""
    params = {"q": q} if q else {}
    resp = requests.get(f"{API_BASE_URL}/prompts", params=params)
    return [
        html.Button(
            item["name"],
            id={"type": "prompt-item", "index": item["id"]},
            style={"display": "block", "width": "100%", "textAlign": "left"},
            n_clicks=0,
        )
        for item in resp.json()
    ]


# --- Callbacks ---


app.clientside_callback(
    "function(value) { return value || ''; }",
    Output("preview", "children"),
    Input("editor", "value"),
)


@app.callback(
    Output("list-area", "children"),
    Input("search-input", "value"),
    Input("sidebar-toggle", "value"),
    Input("list-refresh", "data"),
)
def update_list(q: str | None, toggle: str, _refresh: int) -> list:
    """Populate the sidebar list with prompts matching the search query."""
    if toggle != "prompts":
        return []
    return _prompt_list_items(q)


@app.callback(
    Output("editor", "value"),
    Output("input-name", "value"),
    Output("input-description", "value"),
    Output("input-tags", "value"),
    Output("selected-id", "data"),
    Output("selected-type", "data"),
    Input({"type": "prompt-item", "index": ALL}, "n_clicks"),
    State({"type": "prompt-item", "index": ALL}, "id"),
    prevent_initial_call=True,
)
def load_prompt(n_clicks_list: list, ids: list) -> tuple:
    """Load a prompt into the editor when clicked in the sidebar."""
    if not any(n_clicks_list):
        raise dash.exceptions.PreventUpdate
    triggered = ctx.triggered_id
    if triggered is None:
        raise dash.exceptions.PreventUpdate
    prompt_id = triggered["index"]
    resp = requests.get(f"{API_BASE_URL}/prompts/{prompt_id}")
    prompt = resp.json()
    tags = ", ".join(prompt.get("tags") or [])
    return (
        prompt["content"],
        prompt["name"],
        prompt.get("description") or "",
        tags,
        prompt["id"],
        "prompt",
    )


@app.callback(
    Output("editor", "value", allow_duplicate=True),
    Output("input-name", "value", allow_duplicate=True),
    Output("input-description", "value", allow_duplicate=True),
    Output("input-tags", "value", allow_duplicate=True),
    Output("selected-id", "data", allow_duplicate=True),
    Output("selected-type", "data", allow_duplicate=True),
    Output("mode", "data"),
    Input("btn-new-prompt", "n_clicks"),
    prevent_initial_call=True,
)
def new_prompt(n_clicks: int) -> tuple:
    """Clear the editor and set mode=new when New Prompt is clicked."""
    return "", "", "", "", None, "prompt", "new"


@app.callback(
    Output("selected-id", "data", allow_duplicate=True),
    Output("mode", "data", allow_duplicate=True),
    Output("list-refresh", "data"),
    Input("btn-save", "n_clicks"),
    State("mode", "data"),
    State("selected-id", "data"),
    State("selected-type", "data"),
    State("editor", "value"),
    State("input-name", "value"),
    State("input-description", "value"),
    State("input-tags", "value"),
    State("list-refresh", "data"),
    prevent_initial_call=True,
)
def save_prompt(
    n_clicks: int,
    mode: str | None,
    selected_id: str | None,
    selected_type: str | None,
    content: str | None,
    name: str | None,
    description: str | None,
    tags_str: str | None,
    refresh: int,
) -> tuple:
    """Create or update a prompt when Save is clicked."""
    if selected_type != "prompt":
        raise dash.exceptions.PreventUpdate
    tags = [t.strip() for t in (tags_str or "").split(",") if t.strip()]
    payload = {
        "name": name or "",
        "content": content or "",
        "description": description or "",
        "tags": tags,
    }
    if mode == "new":
        resp = requests.post(f"{API_BASE_URL}/prompts", json=payload)
        new_id = resp.json()["id"]
    else:
        requests.put(f"{API_BASE_URL}/prompts/{selected_id}", json=payload)
        new_id = selected_id
    return new_id, "edit", (refresh or 0) + 1


@app.callback(
    Output("editor", "value", allow_duplicate=True),
    Output("input-name", "value", allow_duplicate=True),
    Output("input-description", "value", allow_duplicate=True),
    Output("input-tags", "value", allow_duplicate=True),
    Output("selected-id", "data", allow_duplicate=True),
    Output("selected-type", "data", allow_duplicate=True),
    Output("list-refresh", "data", allow_duplicate=True),
    Input("btn-delete", "n_clicks"),
    State("selected-id", "data"),
    State("selected-type", "data"),
    State("list-refresh", "data"),
    prevent_initial_call=True,
)
def delete_prompt(
    n_clicks: int,
    selected_id: str | None,
    selected_type: str | None,
    refresh: int,
) -> tuple:
    """Delete the current prompt and clear the editor."""
    if selected_type != "prompt" or not selected_id:
        raise dash.exceptions.PreventUpdate
    requests.delete(f"{API_BASE_URL}/prompts/{selected_id}")
    return "", "", "", "", None, None, (refresh or 0) + 1


if __name__ == "__main__":
    app.run(debug=True)
