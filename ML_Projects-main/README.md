# ML Project Portfolio

This repository contains two major project folders showcasing a variety of data analytics and development skills:

- **1. Data Analytics Project**
- **2. SDP (Social Development Project)**

---

## 📊 1. Data Analytics Projects

This folder includes two SQL projects and a Power BI dashboard analyzing medical data.

### 📁 SQL Tasks

#### 🔹 Task 1: Department Salary Analysis
**Objective:**  
Analyze salaries within departments using HR.EMPLOYEES and HR.DEPARTMENTS tables.

**Key Outputs:**
- Average, max, and min salaries per department
- Names of employees with max/min salaries (using `CASE` + `OVER PARTITION`)
- Cost increase if all employees earned the max salary
- Percentage cost increase

**Techniques Used:**
- SQL Aggregation (`AVG`, `MAX`, `MIN`)
- Window functions
- Conditional logic with `CASE`
- Derived metrics (`cost_increase`, `cost_increase_percent`)

#### 🔹 Task 2: Job Distribution & Salary Pattern
**Objective:**  
Explore job-wise salary trends and job distribution across departments.

**Key Outputs:**
- Salary ranges per job (`min`, `max`, `avg`)
- Employee details (name, job, salary, department)
- Flag `low_job_distribution`: YES if job appears in only one department

**Techniques Used:**
- SQL Window Functions with `OVER (PARTITION BY)`
- Joins across HR.EMPLOYEES, HR.JOBS, and HR.DEPARTMENTS
- Derived flags with conditional `CASE` logic

---

### 📊 Power BI Report: Diabetes Dataset

**Objective:**  
Use Power BI to visually explore patterns between medical metrics and diabetes diagnoses.

**Visuals Created:**
- **Pie Chart:** Diabetes vs Non-Diabetes distribution (~65% vs ~35%)
- **Bar Chart:** Average glucose level by diabetes outcome
- **Clustered Column Chart:** Glucose levels by age group and outcome

**Data Cleaning Steps:**
- Replaced invalid 0 values with `NULL`
- Imputed missing values using column means
- Cleaned columns inline for clarity and consistency

**Tools Used:**
- Power BI Desktop
- Data transformation (Power Query)
- DAX for calculated measures

---

## 🤖 2. SDP (Social Development Project) – Jailbreak Classifier

This notebook implements a basic **toxic prompt filtering system** for NLP use cases.

### 🔹 Components

- **Prompt Dataset:** JSONL file of prompts to evaluate
- **Keyword Filter:** Loaded from `banned_keywords_from_realtoxicity.txt`
- **Toxicity Classifier:** Hugging Face `transformers` pipeline (optional fallback)
- **Final Labeling:** Marked prompts as harmful or safe

### 🧠 Core Logic

```python
df["is_harmful"] = df["prompt_text"].apply(
    lambda text: any(k in text.lower() for k in harmful_keywords)
)
