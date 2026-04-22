# Dashboard MCP — Project Spec for Claude Code

## What this project is

A FastMCP server that exposes LLM-callable tools returning interactive dashboards built with Prefab UI. The LLM orchestration layer uses LangGraph. The rendering layer is hybrid: pre-built Prefab templates for known use cases, generative UI fallback for edge cases.

---

## Stack

| Layer | Library |
|---|---|
| MCP server | `fastmcp[apps]` |
| UI components | `prefab-ui` (pinned to specific version in prod) |
| LLM orchestration | `langgraph` |
| LLM API | `anthropic` |
| Data access | `sqlalchemy` |
| Settings | `pydantic-settings` |
| Python | 3.11+ |

---

## Project structure

```
my_dashboard_mcp/
│
├── server.py                        # FastMCP entry point — registers all tools
├── config.py                        # Pydantic BaseSettings (env vars)
│
├── tools/                           # MCP tool definitions — what the LLM calls
│   ├── data/
│   │   ├── sales.py                 # query_sales(filters, group_by, metrics)
│   │   ├── products.py              # get_products(filters)
│   │   └── categories.py           # get_category_benchmark(filters)
│   └── render/
│       └── dashboard.py            # render_dashboard(user_prompt) → ToolResult
│
├── graph/                           # LangGraph pipeline
│   ├── dashboard_graph.py          # compiled graph + DashboardState TypedDict
│   └── nodes/
│       ├── parse_intent.py         # Node 1: LLM extracts intent JSON from prompt
│       ├── plan_queries.py         # Node 2: deterministic query planning (no LLM)
│       ├── fetch_data.py           # Node 3: deterministic data fetching (no LLM)
│       ├── select_template.py      # Node 4: LLM selects template + params JSON
│       └── validate_ui.py          # Node 5: validates Prefab execution, retry logic
│
├── ui/
│   ├── templates/                  # Pre-built Prefab templates (fast path, ~95%)
│   │   ├── comparison.py           # product vs benchmark
│   │   ├── trend.py                # time series evolution
│   │   ├── breakdown.py            # category breakdown
│   │   └── kpi.py                  # key metrics display
│   └── generative.py               # fallback: LLM generates Prefab code + sandbox exec
│
├── services/
│   ├── llm_service.py              # Single point of contact with Anthropic API
│   ├── sales_service.py            # Sales business logic + query building
│   └── product_service.py          # Product business logic
│
└── data/
    ├── db.py                        # SQLAlchemy engine + session
    └── external_api.py             # Third-party API clients
```

---

## Data flow — full pipeline

```
User prompt (natural language)
        │
        ▼
Tool: render_dashboard(user_prompt)          [tools/render/dashboard.py]
        │
        └── graph.invoke({"user_prompt": ...})
                │
                ▼
        Node 1: parse_intent                 [graph/nodes/parse_intent.py]
                └── llm_service.extract_intent(prompt)
                    → {entities, period, viz_type, metrics}  ← JSON
                │
                ▼
        Node 2: plan_queries                 [graph/nodes/plan_queries.py]
                └── deterministic logic — NO LLM
                    reads intent → builds list of query dicts
                │
                ▼
        Node 3: fetch_data                   [graph/nodes/fetch_data.py]
                └── deterministic — NO LLM
                    sales_service.query() → db.execute() → raw_data
                │
                ▼
        Node 4: select_template              [graph/nodes/select_template.py]
                └── llm_service.select_template(intent, raw_data)
                    → {template: "comparison", params: {...}}  ← JSON only
                │
                ▼
        UI rendering
                ├── template in TEMPLATES dict?
                │   YES → ui/templates/comparison.py(params)   fast, reliable
                │   NO  → ui/generative.py fallback            slow, flexible
                │
                ▼
        Node 5: validate_ui                  [graph/nodes/validate_ui.py]
                └── try sandbox.execute(view)
                    ok   → END
                    fail → retry Node 4 (max 2 retries)
                │
                ▼
        ToolResult(
            content="..."               ← LLM reads this (text summary)
            structured_content=PrefabApp(view)  ← User sees this (interactive UI)
        )
```

---

## Layer responsibilities — strict rules

### tools/
- Thin layer. Orchestrates, does not compute.
- Calls `graph.invoke()` and wraps result in `ToolResult`.
- Never imports from `data/` directly.
- Docstrings are critical — the LLM uses them to decide which tool to call.

### graph/nodes/
- Each node has exactly one responsibility.
- `parse_intent` and `select_template` → call `llm_service` only.
- `plan_queries` and `fetch_data` → zero LLM calls, pure Python logic.
- `validate_ui` → zero LLM calls, try/except + retry signal.

### ui/templates/
- Pure Prefab builders. Receive typed data, return a Prefab component.
- Never call services, never call LLM.
- Reusable across multiple tools.

### ui/generative.py
- Fallback only. Called when `viz_type` not in `TEMPLATES`.
- Calls `llm_service.generate_prefab()` → gets Python code string.
- Executes with `exec()` in a sandboxed `allowed_globals` dict.
- Never expose `__builtins__`, `os`, `subprocess`, or `requests` in sandbox.

### services/llm_service.py
- **Only file that imports `anthropic`.**
- All Anthropic API calls go through here.
- Three methods:
  - `extract_intent(prompt: str) -> dict`
  - `select_template(intent: dict, data: list[dict]) -> dict`
  - `generate_prefab(intent: dict, data: list[dict]) -> str`

### services/*_service.py
- Business logic only. No Prefab imports. No LLM imports.
- Callable from tests without any UI or LLM context.

### data/
- SQLAlchemy only. Returns raw dicts or dataclasses.
- No business logic here.

---

## LangGraph state

```python
# graph/dashboard_graph.py

class DashboardState(TypedDict):
    user_prompt: str           # input
    intent: dict               # set by parse_intent
    data_queries: list         # set by plan_queries
    raw_data: list[dict]       # set by fetch_data
    template_selection: dict   # set by select_template
    prefab_view: Any           # set by UI rendering step
    error: str | None          # set by validate_ui on failure
    retry_count: int           # incremented on retry
```

Graph edges:
```
parse_intent → plan_queries → fetch_data → select_template → validate_ui
                                                    ↑               │
                                                    └───(on fail)───┘
                                                    (max 2 retries)
```

---

## LLM output contracts

### extract_intent output
```json
{
  "entities": ["machine_laver_x"],
  "period": { "year": 2026, "granularity": "monthly" },
  "viz_type": "comparison",
  "metrics": ["revenue", "units_sold"]
}
```

`viz_type` must be one of: `"comparison"` | `"trend"` | `"breakdown"` | `"kpi"`

### select_template output
```json
{
  "template": "comparison",
  "params": {
    "metric": "revenue",
    "title": "Machine à laver X vs marché 2026",
    "period_key": "month"
  }
}
```

Both LLM calls must return **JSON only** — no markdown, no explanation. Enforce this in system prompts.

---

## UI templates registry

```python
# ui/templates/__init__.py

from .comparison import comparison_template
from .trend import trend_template
from .breakdown import breakdown_template
from .kpi import kpi_template

TEMPLATES = {
    "comparison": comparison_template,
    "trend": trend_template,
    "breakdown": breakdown_template,
    "kpi": kpi_template,
}
```

Adding a new template = add file in `ui/templates/` + register in `TEMPLATES`. No other files change.

---

## Generative UI sandbox — allowed globals only

```python
# ui/generative.py

ALLOWED_GLOBALS = {
    # Layout
    "Column": Column, "Row": Row, "Grid": Grid,
    # Typography
    "Heading": Heading, "Text": Text, "Muted": Muted,
    # Data display
    "Badge": Badge, "Card": Card, "CardContent": CardContent, "Metric": Metric,
    # Charts
    "BarChart": BarChart, "LineChart": LineChart, "ChartSeries": ChartSeries,
    # Tables
    "DataTable": DataTable, "TableColumn": TableColumn,
}
# No __builtins__, no os, no requests, no subprocess
```

---

## Key architectural principles

1. **LLM decides, Python executes.** LLM outputs are always JSON (intent, params). Never execute LLM free text directly except in the sandboxed generative fallback.

2. **Templates first, generative as fallback.** `TEMPLATES` dict is the fast path. Generative UI is only reached when `viz_type` not in `TEMPLATES`.

3. **`llm_service.py` is the single LLM boundary.** Change model or provider → touch one file.

4. **Deterministic nodes have zero LLM calls.** `plan_queries`, `fetch_data`, `validate_ui` are fully testable without mocking any LLM.

5. **Services are UI-agnostic.** `sales_service.py` has no Prefab imports. It can be used in a REST API, a CLI, or a test with zero changes.

6. **Tool docstrings are API contracts.** The LLM reads them to decide which tool to call. Keep them precise, include arg types and return shape.

---

## Implementation order

Build in this sequence — each step is independently testable:

```
Step 1 — data/db.py + services/sales_service.py
         → unit test with real or mock DB

Step 2 — services/llm_service.py
         → test extract_intent and select_template with real prompts

Step 3 — graph/nodes/ one by one
         → test each node with a hardcoded state dict

Step 4 — graph/dashboard_graph.py
         → integration test: prompt in, state out

Step 5 — ui/templates/ one template at a time
         → fastmcp dev apps to preview locally

Step 6 — ui/generative.py
         → test with edge case prompts that don't match any template

Step 7 — tools/ + server.py
         → end-to-end test with Claude as the caller
```

---

## Environment variables

```bash
ANTHROPIC_API_KEY=sk-...
DATABASE_URL=postgresql://user:pass@localhost:5432/dashboard
LLM_MODEL=claude-opus-4-5
MAX_RETRIES=2
```

Loaded via `config.py` using `pydantic-settings`. Never hardcode these values.

---

## Commands

```bash
# Install
pip install "fastmcp[apps]" langgraph anthropic sqlalchemy pydantic-settings

# Preview UI locally
fastmcp dev apps server.py

# Run server
python server.py
```