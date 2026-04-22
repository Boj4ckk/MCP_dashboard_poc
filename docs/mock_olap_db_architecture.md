# OLAP Data Warehouse Architecture (Retail Electronics Company)

## Context
This OLAP model is designed for a large retail company specializing in electronics and multimedia in France.

It follows a star schema optimized for analytics, BI dashboards, and LLM-driven tool routing.

---

# Core Design Principles

- Star schema (fact + dimensions)
- Pre-aggregated business metrics in fact tables
- Consistent surrogate keys (UUID or integer IDs)
- Time-centric analysis enabled via centralized date dimension
- Multiple fact tables for different business domains

---

# FACT TABLES (Business Metrics Layer)

## fact_sales
Primary sales performance table

Fields:
- sale_id (UUID)
- date_id (FK -> dim_date)
- product_id (FK -> dim_product)
- customer_id (FK -> dim_customer)
- store_id (FK -> dim_store)
- order_id (business reference)

Metrics:
- quantity
- revenue
- discount_amount
- cost_amount
- profit_amount

Dimensions:
- channel (online | in_store | marketplace)

Use cases:
- revenue analysis
- sales trends
- channel performance
- KPI dashboards

---

## fact_orders
Order lifecycle tracking (operational analytics)

Fields:
- order_id
- date_id
- customer_id
- store_id

Metrics:
- order_value
- item_count
- delivery_time_days
- order_status_flag (delivered, cancelled, returned)

Use cases:
- order flow analysis
- conversion funnel
- operational performance

---

## fact_inventory_snapshot
Inventory state over time (snapshot model)

Fields:
- snapshot_id
- date_id
- product_id
- warehouse_id

Metrics:
- stock_quantity
- reserved_quantity
- available_quantity
- stock_value

Use cases:
- stock levels
- out-of-stock detection
- supply chain monitoring

---

## fact_returns
Product returns and after-sales issues

Fields:
- return_id
- date_id
- product_id
- customer_id
- order_id

Metrics:
- return_quantity
- refund_amount
- return_rate_flag

Attributes:
- return_reason

Use cases:
- product quality analysis
- after-sales performance
- churn risk signals

---

## fact_support_tickets
Customer support and service tracking

Fields:
- ticket_id
- date_id
- customer_id
- store_id (optional)

Metrics:
- resolution_time_hours
- ticket_count
- escalation_flag

Attributes:
- issue_type
- status

Use cases:
- customer satisfaction
- operational efficiency
- product issue detection

---

# DIMENSION TABLES (Context Layer)

## dim_date
Central time dimension

Fields:
- date_id (PK)
- full_date
- day
- week
- month
- quarter
- year
- day_of_week
- is_weekend

Use cases:
- all time-based aggregations

---

## dim_product
Product catalog dimension

Fields:
- product_id (PK)
- product_name
- brand
- category
- subcategory
- price
- cost
- lifecycle_status (active, discontinued)

Use cases:
- product performance
- category analysis

---

## dim_customer
Customer profile dimension

Fields:
- customer_id (PK)
- first_name
- last_name
- email
- country
- city
- segment (new, returning, VIP)
- acquisition_channel
- registration_date

Use cases:
- segmentation
- LTV analysis
- churn analysis

---

## dim_store
Physical store dimension

Fields:
- store_id (PK)
- store_name
- city
- region
- country
- store_type (flagship, standard, outlet)
- opening_date

Use cases:
- geographic performance
- store comparison

---

## dim_warehouse
Logistics and inventory locations

Fields:
- warehouse_id (PK)
- warehouse_name
- city
- region
- country

Use cases:
- supply chain optimization
- stock distribution

---

## dim_channel
Sales channel dimension

Fields:
- channel_id (PK)
- channel_name (online, in_store, marketplace, partner)
- channel_type (digital, physical)

Use cases:
- omnichannel analysis

---

# RELATIONSHIPS (Star Schema Mapping)

fact_sales
- product_id -> dim_product
- customer_id -> dim_customer
- store_id -> dim_store
- date_id -> dim_date
- channel -> dim_channel

fact_orders
- customer_id -> dim_customer
- store_id -> dim_store
- date_id -> dim_date

fact_inventory_snapshot
- product_id -> dim_product
- warehouse_id -> dim_warehouse
- date_id -> dim_date

fact_returns
- product_id -> dim_product
- customer_id -> dim_customer
- date_id -> dim_date

fact_support_tickets
- customer_id -> dim_customer
- store_id -> dim_store (optional)
- date_id -> dim_date

---

# BUSINESS LOGIC NOTES

## Metric standardization
- revenue = sum(quantity * unit_price - discounts)
- profit = revenue - cost
- stock_value = stock_quantity * product_cost

## Time handling
- all facts are date_id based (no raw timestamps in analytics layer)

## Granularity rules
- fact_sales: one row per product per order
- fact_inventory_snapshot: one row per product per warehouse per day
- fact_support_tickets: one row per ticket

---

# LLM / DASHBOARD USAGE LAYER

This schema is optimized for LLM-driven dashboard routing:

## Mapping examples

- "sales performance" -> fact_sales + dim_date + dim_store
- "best products" -> fact_sales + dim_product
- "stock issues" -> fact_inventory_snapshot + dim_product
- "customer behavior" -> fact_sales + dim_customer
- "support issues" -> fact_support_tickets

---

# Summary

This OLAP model is:
- optimized for analytics (not transactions)
- stable for dashboard generation
- easy for LLM tool routing
- realistic for enterprise retail environments