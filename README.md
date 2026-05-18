# 📊 Vendor Performance Analysis

End-to-end data analytics project analyzing vendor profitability, inventory turnover, and discount effectiveness using **SQL Server**, **Python**, and **Power BI**.

---

## 📁 Data Source

6 CSV files with **15.6M+ records**:
- `sales` (12.8M rows) – transaction data
- `purchases` (2.4M rows) – purchase orders
- `begin_inventory` / `end_inventory` – inventory snapshots
- `purchase_prices` – product pricing
- `vendor_invoice` – freight costs

---

## 🔧 What I Did

### 1. Data Ingestion
- Used **Python (pandas + SQLAlchemy)** to load all CSVs into SQL Server
- Handled data types and connection using ODBC

### 2. Data Cleaning & Merging (SQL)
- Created **CTEs** to aggregate purchases, sales, and freight data
- Built a master table `vendor_sales_summary` joining all sources on `VendorNumber` and `Brand`
- Calculated derived metrics:
  - `GrossProfit` = Sales - Purchases - Freight
  - `ProfitMargin` = (GrossProfit / Sales) × 100
  - `StockTurnover` = SalesQuantity / PurchaseQuantity

### 3. Exploratory Data Analysis (Python)
- Generated summary statistics and distribution plots
- Detected outliers using boxplots
- Created **correlation heatmap** (found 0.40 correlation between stock turnover and profit margin)
- Filtered out inconsistent records (negative profit, zero sales)

### 4. Statistical Testing
- Performed **two-sample t-test** comparing top vs low-performing vendors
- Calculated **95% confidence intervals** for profit margins
- Result: Significant difference (p < 0.05) – low-sales vendors have higher margins (40-42% vs 30-31%)

### 5. Business Analysis
- **Pareto analysis** – Top 10 vendors contribute 65.69% of purchases
- **Bulk purchasing impact** – Large orders reduce unit cost by 72%
- **Unsold inventory** – $2.71M capital locked in slow-moving stock
- **Promotional targets** – Identified brands with low sales but high margins

### 6. Power BI Dashboard
- Connected to SQL Server, built interactive visuals:
  - KPI cards, Pareto chart, scatter plot, confidence interval comparison
  - Slicers for vendor, brand, and category filtering

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| SQL Server | Database, aggregation, joins |
| Python (pandas, numpy, scipy, seaborn) | EDA, statistics, visualization |
| Power BI | Dashboard |
| Git LFS | Large file storage |

---

## 📁 Repo Structure
- notebooks/ # Jupyter notebooks (ingestion, EDA, analysis)
- reports/ # PDF report + Gamma presentation
- dashboard/ # Power BI .pbix file
- data/ # CSV files (compressed)
- Plots/ # Visualizations
