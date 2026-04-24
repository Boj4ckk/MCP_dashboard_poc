# Dashboard: Returns & After-Sales Service

## Objective
Analyze product returns, reasons, and after-sales service efficiency to improve product quality and customer satisfaction.

---

## Metrics & Visualizations

- **Return rate by product, category, channel**
  - Visualization: Bar chart, KPI card
  - Source: fact_returns, dim_product, dim_channel

- **Return reasons**
  - Visualization: Pie chart, Table
  - Source: fact_returns

- **Average return processing time**
  - Visualization: KPI card, Line chart
  - Source: fact_returns

---

## Recommended Filters
- Period (day, week, month, year)
- Product category
- Sales channel

---

## Tables used
- fact_returns
- dim_product
- dim_channel
