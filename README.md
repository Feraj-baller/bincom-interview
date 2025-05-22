## ⚙️ Requirements

* Python 3.x
* `psycopg2` (for PostgreSQL integration)

Install `psycopg2` using pip:
```bash
pip install psycopg2
```

---

##  How to Run

1.  Ensure Python 3 and `psycopg2` are installed.
2.  **Database Setup (Optional but Recommended for full functionality):**
    * Have a PostgreSQL server running.
    * Update database connection details (`dbname`, `user`, `password`, `host`) in the `save_to_postgresql` function within the script.
3.  Execute from your terminal:
    ```bash
    python your_script_name.py
    ```
    (Replace `your_script_name.py` with the actual file name.)

---

##  Core Functionalities

* **Color Data Processing**: Extracts and cleans a predefined list of weekly shirt colors.
* **Statistical Color Analysis**:
    * Calculates the most worn color (mode).
    * Determines custom "mean" and "median" colors based on frequency and alphabetical sorting.
    * Computes the variance of color frequencies.
    * Calculates the probability of picking a "RED" shirt.
* **Database Interaction**: Saves color names and their frequencies to a PostgreSQL table (`color_frequencies`).
* **Algorithmic Utilities**:
    * Recursive binary search on a list of numbers.
    * Generation of a random 4-digit binary number and its conversion to decimal.
    * Summation of the first 50 Fibonacci numbers.

---

##  Important Notes

* The script's definitions for "mean color" and "median color" are specific interpretations for categorical data and may differ from standard statistical approaches.
* The "color variance" refers to the variance of the *counts* (frequencies) of each color.
* The database saving feature (`save_to_postgresql`) is initially commented out in the `main()` function. Uncomment it and configure your database credentials if you wish to use it.

---
```
