# Dashboard: Stock & Logistics

## Objective
Monitor inventory levels, detect out-of-stock situations, and optimize supply chain operations.

---

## Metrics & Visualizations

- **Stock level by product, warehouse, store**
  - Visualization: Heatmap, Table, Bar chart
  - Source: fact_inventory_snapshot, dim_product, dim_warehouse, dim_store

- **Out-of-stock rate**
  - Visualization: KPI card, Bar chart
  - Source: fact_inventory_snapshot

- **Stock turnover rate**
  - Visualization: Line chart, KPI card
  - Source: fact_inventory_snapshot, fact_sales

- **Overstock/Out-of-stock alerts**
  - Visualization: Alert list (Table), Visual indicator (Icon/Conditional formatting)
  - Source: fact_inventory_snapshot

---

## Recommended Filters
- Period (day, week, month, year)
- Product category
- Warehouse
- Store

---

## Tables used
- fact_inventory_snapshot
- fact_sales
- dim_product
- dim_warehouse
- dim_store
