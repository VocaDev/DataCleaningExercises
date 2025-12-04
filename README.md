# 📊 Cafe Sales Data Cleaning & Analysis

A complete, end-to-end data cleaning & analysis workflow using **Python**, **Pandas**, **NumPy**, **Matplotlib**, and **Seaborn**.

---

## 🚀 Overview

This project demonstrates how to clean, validate, analyze, and visualize a **dirty real-world café sales dataset**.  
It shows the full process of turning raw, inconsistent, error-filled data into meaningful insights and visualizations.

---

## 🎯 Purpose of This Project

The goal of this project is to:

- Practice **real-world data cleaning** techniques
- Fix and validate corrupted or inconsistent data
- Perform meaningful **Exploratory Data Analysis (EDA)**
- Produce clear, visually appealing **data visualizations**
- Demonstrate a professional data workflow suitable for portfolios and GitHub projects
- Help others learn how to clean and analyze datasets effectively

This project is ideal for Data Analysis students, beginners in Python, or anyone improving their analytical pipeline.

---

## 🧰 Libraries Used

This project uses the following Python libraries:

- **Pandas** — data manipulation & cleaning
- **NumPy** — numerical operations
- **Matplotlib** — fundamental plotting
- **Seaborn** — advanced visualization styling
- **Python 3.x** — programming language used to build the entire project

To install them, see the _How to Run_ section below.

---

## 🧹 Data Cleaning Steps

The raw dataset contained many real-world issues such as missing values, incorrect entries, inconsistent formatting, and invalid numbers.  
Below are the exact cleaning steps implemented:

### ✔ Replace invalid values

- Convert `"ERROR"` and `"UNKNOWN"` into `NaN`
- Remove empty strings or replace them with meaningful categories

### ✔ Fix data types

- Convert numerical columns from string → integer/float
- Convert `Transaction Date` from string → `datetime`

### ✔ Validate numerical relationships

- Check if `Total Spent = Quantity × Price Per Unit`
- Recalculate totals where incorrect

### ✔ Standardize categories

- Clean and unify Payment Methods
- Normalize item names and location fields

### ✔ Handle missing data

- Drop rows with too many empty fields
- Fill reasonable missing values using median/mode

### ✔ Export cleaned dataset

- Save final, cleaned version to:  
  **`clean_cafe_sales.csv`**

---

## 📈 Exploratory Data Analysis (EDA)

After cleaning, various analyses were performed, including:

- Most sold café items
- Sales distribution by payment method
- Sales by location
- Daily and monthly trends
- Statistical summaries (mean, median, std, variance)

---

## 📊 Visualizations Included

This project generates multiple graphs to better understand the dataset:

- 📦 **Bar Charts** – top-selling items
- 📈 **Line Charts** – sales trends over time
- 🥧 **Pie Charts** – payment method usage
- 📊 **Histograms** – distribution of quantity & spending
- 📉 **Boxplots** – price comparisons
- 🔥 **Heatmaps** – correlation between numerical fields

All charts are created with Matplotlib and Seaborn.

---

## 📁 File Structure

├── dirty_cafe_sales.csv # Raw dataset

├── clean_cafe_sales.csv # Cleaned dataset (auto-generated)

├── analysis.py # Main script for cleaning, EDA & visualization

└── README.md # Project documentation

---

## 🧪 How to Run This Project

### 1️⃣ Install required libraries

Run this command in your terminal:

pip install pandas numpy matplotlib seaborn

### 2️⃣ Run the main Python script

python analysis.py

3️⃣ Output

After running:

A cleaned CSV file will be generated
All visualizations will be saved in the project folder
Terminal will display summaries and analysis results
You can modify or extend the analysis freely.

### 🤝 Contribution

Feel free to contribute, improve, or suggest changes via pull requests or issues.

### 📬 How to Reach Me

You can contact me for feedback, collaboration, or questions:

- Email: gentainvoca@gmail.com

- LinkedIn: https://www.linkedin.com/in/gentian-voca-578943322/
