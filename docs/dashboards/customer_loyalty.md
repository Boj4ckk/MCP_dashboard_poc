# Dashboard: Customer & Loyalty

## Objective
Monitor customer base evolution, segment customers, and analyze lifetime value to drive retention strategies.

---

## Metrics & Visualizations

- **Active customers, new customers**
  - Visualization: KPI card, Line chart
  - Source: dim_customer, fact_orders

- **Customer lifetime value (LTV)**
  - Visualization: KPI card, Bar chart
  - Source: fact_sales, dim_customer

- **Customer segmentation (by region, channel, product category)**
  - Visualization: Pie chart, Map, Table
  - Source: dim_customer, dim_channel, dim_product

---

## Recommended Filters
- Period (day, week, month, year)
- Customer segment
- Region
- Channel

---

## Tables used
- dim_customer
- fact_orders
- fact_sales
- dim_channel
- dim_product
