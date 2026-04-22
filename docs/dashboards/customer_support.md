# Dashboard: Customer Support

## Objective
Track customer support activity, resolution efficiency, and identify recurring issues to enhance service quality.

---

## Metrics & Visualizations

- **Support tickets volume over time**
  - Visualization: Line chart, Bar chart
  - Source: fact_support_tickets, dim_date

- **Average resolution time**
  - Visualization: KPI card, Line chart
  - Source: fact_support_tickets

- **Tickets breakdown by issue type/category**
  - Visualization: Pie chart, Bar chart
  - Source: fact_support_tickets

- **First contact resolution rate**
  - Visualization: KPI card, Gauge
  - Source: fact_support_tickets

---

## Recommended Filters
- Period (day, week, month, year)
- Issue type
- Store

---

## Tables used
- fact_support_tickets
- dim_date
- dim_store
