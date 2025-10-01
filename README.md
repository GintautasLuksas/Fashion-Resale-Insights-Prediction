# Fashion Resale Insights & Prediction

A full-stack data project exploring **fashion resale trends**, **seller performance**, and **product insights** using **PostgreSQL**, **Power BI**, and a future extension into **Machine Learning**.

This repository covers the complete workflow:
1. Data ingestion & cleaning in Python.
2. Database structuring and querying in PostgreSQL.
3. Interactive analytics with Power BI.
4. Preparation for future feature engineering and ML modeling.

---

## Main Goals

### Task 1: PostgreSQL – Clean & Structure the Dataset
**Goal in PyCharm:**  
Prepare a clean dataset with only necessary columns, ready for queries.  

**Goal in PgAdmin:**  
Use SQL to explore:

1. **Sales Performance**  
    - Total sales  
    - Total items sold  
    - Average price  
    - Percentage of items sold  
    - Revenue by category  
    - Revenue by season  

2. **Seller Performance**  
    - Total earnings per seller  
    - Total items sold per seller  
    - Average earning per sold item  
    - Top seller countries  

3. **Product Trends**  
    - Best selling categories  
    - Top brands  
    - Color trends  
    - Material trends  
    - Gender performance  
    - Dependency on condition  
    - Season performance  

### Task 2: Power BI – Analytics Dashboard Prep
**Goal:** Visualize findings and derive additional insights.  
Each visual should clearly explain its **purpose** and how it was created.

### Task 3: Machine Learning – Feature Engineering & Modeling Prep
**Goal:** Prepare the dataset for future ML modeling.  
Includes encoding, filtering, and theoretical feature engineering for predicting price, sales success, or product desirability.

---

## Project Structure

```
data/                         # Data storage
├── raw/                      # Original Kaggle dataset
└── processed/                # Cleaned datasets for SQL/BI

Power BI Visuals/              # Power BI dashboard files

sql/
└── analysis_queries.sql       # SQL queries

src/
├── db/
│   └── insert.py              # Export processed data to PostgreSQL
├── data_processing.py         # Cleaning and preprocessing
└── main.py                    # Pipeline orchestrator

.env                           # Environment variables (login info)
.example                       # Example environment file
requirements.txt               # Python dependencies
README.md                      # Project overview (this file)
LICENSE                        # Project license
```

* Data file can be downloaded from Kaggle:*  
[https://www.kaggle.com/datasets/justinpakzad/vestiaire-fashion-dataset/data](https://www.kaggle.com/datasets/justinpakzad/vestiaire-fashion-dataset/data)


## Environment Setup
1. Create and activate a Python virtual environment.  
2. Install required packages from `requirements.txt`.  
pip install -r requirements.txt


3. Set database credentials in a `.env` file:

```env
DB_USER=your_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=fashion_resale
```
## How to Run

Process and clean the dataset:

python src/main.py

Insert processed data into PostgreSQL

Automatically handled in main.py using insert_dataframe_to_postgres().

Table created if it doesn’t exist (fashion_resale).

Optional: Open Power BI and connect to the PostgreSQL database for dashboard creation.

## Data Pipeline

1. **Load raw data**  
   - Large CSV loaded with `low_memory=False` to preserve data types.  

2. **Clean & transform**  
   - Drop unnecessary columns (product_id, product_description, seller_username, etc.)  
   - Keep essential columns for analysis: product_type, brand_name, product_category, product_gender_target, product_condition, price_usd, sold, seller_country, seller_products_sold, and others.   
   - Fill or handle missing values appropriately.  

3. **Save processed CSV**  
   - Saved for debugging or reuse in analysis and modeling.  

4. **Insert into PostgreSQL**  
   - `insert_dataframe_to_postgres()` handles connection via SQLAlchemy and inserts cleaned data into the `fashion_resale` table.  

---

## Analysis Goals (PostgreSQL & Power BI)

**Sales Performance**
- Total sales and revenue  
- Total items sold  
- Average price  
- Revenue by category and season  

**Seller Performance**
- Total earnings and items sold per seller  
- Average earning per sold item  
- Top seller countries  

**Product Trends**
- Best selling categories and brands  
- Top colors and materials  
- Gender-based trends  
- Impact of product condition and season  

*All SQL queries are in `sql/analysis_queries.sql`.*

---

## Power BI Dashboard

- Visualizations for sales, seller, and product trends.  
- Cards, column charts, and slicers for interactive insights.  
- Metrics like total revenue, average price, percentage sold, and top sellers are included.  

---

## Machine Learning Preparation

**Feature Engineering (Theoretical approach)**
- Encode categorical columns (one-hot, label encoding)  
- Filter low-frequency categories  
- Drop irrelevant or redundant columns  
- Prepare target variables for predicting price, sales success, or product desirability  

**Modeling - for future**
- Sale success prediction using Random Forest Classifier (prototype)  
- Dataset ready for experimentation and further modeling  

---

## Notes
- Keep `.env` secure; do not commit credentials.  
- Raw SQL queries for detailed insights are available in `sql/analysis_queries.sql`.  
- The processed dataset can be reused for ML experiments or additional dashboards.  
