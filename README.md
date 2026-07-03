# Employee Performance Prediction Website

A simple web app (built with Streamlit) that predicts an employee's
performance rating based on their profile, and shows graphs/insights
from the underlying dataset. No database required — everything runs
from CSV + a saved ML model file.

## Project Files

| File                  | Purpose                                                              |
|-----------------------|-----------------------------------------------------------------------|
| `generate_data.py`    | Creates a synthetic employee dataset (`employee_data.csv`)            |
| `train_model.py`      | Trains a Random Forest model and saves it as `model.pkl`              |
| `app.py`              | The Streamlit website (prediction form + graphs)                      |
| `employee_data.csv`   | The dataset used for training and for the insights graphs             |
| `model.pkl`           | The trained ML model                                                   |
| `label_encoders.pkl`  | Encoders used to convert text fields (Department, etc.) to numbers    |
| `feature_columns.pkl` | The exact order of columns the model expects                          |
| `requirements.txt`    | Python packages needed to run the project                             |

## How to Run

1. **Install dependencies** (only needs to be done once):
   ```bash
   pip install -r requirements.txt
   ```

2. **(Optional) Regenerate the dataset and retrain the model**
   If you want to use your own dataset instead of the synthetic one,
   replace `employee_data.csv` with your own file (keep the same
   column names), then run:
   ```bash
   python train_model.py
   ```
   This will create fresh `model.pkl`, `label_encoders.pkl`, and
   `feature_columns.pkl` files.

   To regenerate the included synthetic dataset:
   ```bash
   python generate_data.py
   python train_model.py
   ```

3. **Run the website**:
   ```bash
   streamlit run app.py
   ```
   This opens a browser window (usually at `http://localhost:8501`)
   with the prediction form and graphs.

## How It Works

- **Dataset**: `employee_data.csv` contains employee records with
  fields like Age, Department, Job Role, Monthly Income, Years at
  Company, Overtime, Job Satisfaction, Work-Life Balance, etc., along
  with a `PerformanceRating` (1 = Low, 2 = Good, 3 = Excellent,
  4 = Outstanding).

- **Model**: A `RandomForestClassifier` from scikit-learn is trained
  on this data to predict `PerformanceRating` from the other columns.

- **Website (app.py)**:
  - The **sidebar** lets the user enter an employee's details.
  - Clicking **Predict Performance** runs the saved model on those
    inputs and shows the predicted rating along with a confidence
    chart.
  - The **Dataset Insights** section shows:
    - Distribution of performance ratings across all employees
    - Feature importance (which factors matter most to the model)
    - A correlation heatmap of numeric features
    - Average performance rating by department

## Using a Real Dataset (Optional Improvement)

If you'd like to use a real dataset for your final year project (e.g.
the "IBM HR Analytics Employee Attrition & Performance" dataset from
Kaggle), download it, rename/clean the columns to match the ones
listed above (or update `train_model.py` and `app.py` accordingly),
then re-run `train_model.py`.

## Notes for Your Project Report / Viva

- The current dataset is **synthetically generated** (see
  `generate_data.py`) so the project can run fully offline. You can
  mention this in your report and optionally swap in a real dataset
  for stronger results.
- The model achieves roughly **55-60% accuracy** on a 4-class problem
  (random guessing would be 25%), which is reasonable for a synthetic
  dataset with added noise — a real dataset will likely perform
  better and give you a stronger demo.
- No database is used — `employee_data.csv` and the `.pkl` files act
  as simple persistent storage, which keeps the project lightweight
  and easy to run/demo.
