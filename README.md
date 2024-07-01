# Weather Data Pipeline

This project provides a pipeline for storing and querying historical and recent weather data. Follow the steps below to set up and use the project.

## Prerequisites

- Python 3.8.10
- MySQL database

## Installation

1. Clone the repository to your local machine.

   ```sh
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Create a virtual environment (optional but recommended).

   ```sh
   python3.8 -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required Python packages.

   ```sh
   pip install -r requirements.txt
   ```

## Database Setup

1. Install and configure a MySQL database on your local machine.

2. Update the database connection properties in `DBConnection.properties`.

   ```properties
   [mysql]
   host = <your-host>
   database = <your-database>
   user = <your-username>
   password = <your-password>
   ```

3. Run the database script to create the necessary tables.

   ```sh
   mysql -u <your-username> -p <your-database> < createDB.sql
   ```

4. Run common queries from `commonQueries.sql`.

   ```sh
   mysql -u <your-username> -p <your-database> < commonQueries.sql
   ```

## Usage

### Historical Weather Data Dump

Use the `historical_dump.py` script to fetch and store historical weather data.

1. Open `historical_dump.py` and change the API key on line number 7 to your API key.

   ```python
   API_KEY = 'your_api_key'
   ```

2. Run the script.

   ```sh
   python historical_dump.py
   ```

### Yesterday's Weather Data Dump

Use the `yesterdays_dump.py` script to fetch and store yesterday's weather data.

1. Open `yesterdays_dump.py` and change the API key on line number 7 to your API key.

   ```python
   API_KEY = 'your_api_key'
   ```

2. Run the script.

   ```sh
   python yesterdays_dump.py
   ```

## Contributing

Feel free to fork the repository and make improvements. Pull requests are welcome.

## License

This project is licensed under the MIT License.

---

By following the steps above, you should be able to set up and use the weather data pipeline effectively. If you encounter any issues, please open an issue on the repository or contact the maintainers.
