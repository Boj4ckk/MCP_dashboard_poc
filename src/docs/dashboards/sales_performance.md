# Dashboard: Sales & Commercial Performance

## Objective
Monitor overall commercial performance, identify sales trends, top products, and channel distribution.

---

## Metrics & Visualizations

- **Revenue by period (day, month, year)**
  - Visualization: Line chart or Bar chart
  - Source: fact_sales, dim_date

- **Order volume, average basket value**
  - Visualization: KPI card, Bar chart
  - Source: fact_orders, fact_sales

- **Top products by revenue and volume**
  - Visualization: Horizontal bar chart, Table
  - Source: fact_sales, dim_product

- **Sales breakdown by channel**
  - Visualization: Pie chart or Stacked bar chart
  - Source: fact_sales, dim_channel

- **Conversion rate**
  - Visualization: KPI card, Gauge
  - Source: fact_orders

---

## Recommended Filters
- Period (day, week, month, year)
- Sales channel
- Product category
- Store

---

## Tables used
- fact_sales
- fact_orders
- dim_date
- dim_product
- dim_channel
- dim_store
