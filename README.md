# Weather ETL Pipeline

## Project Overview
This project involves building an Extract, Transform, Load (ETL) pipeline to fetch weather data from public APIs, cleanse and transform the data, and load it into a database for daily updates. The goal is to practice and enhance skills in:

- Data extraction from APIs
- Data cleaning and transformation
- Pipeline scheduling and automation
- Working with databases

## Features
- **Data Extraction:** Fetch weather data using a public API.
- **Data Transformation:** Cleanse and structure the data for analysis.
- **Data Loading:** Store the processed data in a database.
- **Automation:** Schedule the pipeline to update data daily.

## Prerequisites
Ensure the following tools and libraries are installed:

- Python 3.x
- Virtual environment tool (`venv`)
- Libraries: `requests`, `pandas`, `numpy`, `python-dotenv`
- A database system (e.g., PostgreSQL, MySQL, SQLite)

## Setup Instructions

### Step 1: Clone the Repository
Clone this project to your local machine:
```bash
git clone https://github.com/imaddde867/Weather_Pipeline.git
cd Weather_ETL_Pipeline
```

### Step 2: Create and Activate a Virtual Environment
```bash
python3 -m venv env
source env/bin/activate  # On macOS/Linux
env\Scripts\activate   # On Windows
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables
1. Create a `.env` file in the root directory.
2. Add your API key and any other configuration variables:
   ```env
   API_KEY=your_api_key_here
   DB_CONNECTION_STRING=your_database_connection_string_here
   ```

## Pipeline Workflow

### 1. **Data Extraction**
   - Fetch raw weather data using the API key.
   - Parse the data to JSON format.

### 2. **Data Transformation**
   - Cleanse missing or inconsistent data.
   - Convert units if necessary (e.g., temperature from Kelvin to Celsius).
   - Restructure the data into a tabular format using Pandas.

### 3. **Data Loading**
   - Connect to the database using the connection string.
   - Insert or update records as needed.

### 4. **Automation**
   - Schedule the pipeline to run daily using tools like `cron` (Linux/macOS) or Task Scheduler (Windows).

## Usage
Run the pipeline script manually for testing:
```bash
python main.py
```

For automation, configure a scheduler to execute the script daily.

## Project Structure
```
Weather_ETL_Pipeline/
|-- env/                 # Virtual environment directory
|-- data/                # Optional: Store raw and processed data locally
|-- scripts/             # Pipeline scripts
|   |-- extract.py       # Data extraction logic
|   |-- transform.py     # Data cleaning and transformation
|   |-- load.py          # Database operations
|-- main.py              # Entry point for the pipeline
|-- .env                 # Environment variables
|-- requirements.txt     # Python dependencies
|-- README.md            # Project documentation
```
## Database Structure

![alt text](https://github.com/imaddde867/Weather_Pipeline/blob/main/Database_Preview.png)

## Technologies Used
- **Languages:** Python
- **Libraries:** Requests, Pandas, NumPy
- **Database:** PostgreSQL (or any preferred database system)
- **Automation Tools:** Cron, Task Scheduler

## Future Enhancements
- Add error handling and logging.
- Support multiple weather APIs for redundancy.
- Visualize the stored data using a dashboard (e.g., Tableau, Matplotlib).

## Acknowledgments
Special thanks to the developers and maintainers of the public weather API used in this project.
