# MyShop Project
This is an online shop, that sells TVs and refrigirators.
It is built to run in **Python 3.6** using the **Aiohttp** framework. Checked with Ubuntu Linux 16.04 LTS.
It uses PostgreSQL database (checked with PostgreSQL 9.5.12).


# Setup
1. Create virtual enviroment and activate it:
  ```
  python -m venv <env_name>
  source <env_name>/bin/activate
  ```
2. Clone the repository:
  ```
  git clone https://github.com/Juliya555/myshop.git
  ```
3. Install all requirements:
  ```
  pip install -r requirements.txt
  ```
4. Create your database and user for PostgresSQL (assumimg that Ubuntu Linux 16.04 is used):
  ```
  sudo adduser <somename>
  sudo -u postgres createuser --interactive
  sudo -u postgres createdb <somename>
  sudo -u postgres psql
  ```
5. In psql write the following queries:
  ```
  ALTER ROLE <somename> WITH PASSWORD '<db_password>';
  GRANT ALL PRIVILEGES ON DATABASE <somename> TO <somename>;
  \q
  ```
6. Fill the config file with your data **(config/prod.yaml)**.
7. Run the script **init_db.py** and then use **data.sql** file to load structure and data to launch the project:
  ```
  python init_db.py
  sudo -u <somename> psql <somename> < data.sql
  ```

# Run
1. Change directory to myshop and run the server:
  ```
  cd myshop/
  python main.py
  ```
2. Open http://localhost:8080 in your web browser to see the online shop.
