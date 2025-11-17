import oracledb

# Assuming your wallet files are in './wallet'
config_dir = "/home/teliason/src/ref01/env/dev/Wallet_testatp01"
username = "ADMIN"
password = "Welcome1_234_MM"
service_name = "testatp01_tp" # e.g., from tnsnames.ora
wallet_password = "welcome1"
wallet_location = "/home/teliason/src/ref01/env/dev/Wallet_testatp01"


try:
    connection = oracledb.connect(
        user=username,
        password=password,
        dsn=service_name,
        config_dir=config_dir,
        wallet_password=wallet_password,
        wallet_location=wallet_location
    )
    print("Connection successful!")
    # Perform database operations here

    try: 
        sql_query = "drop user sh01 cascade;"
        connection.cursor().execute(sql_query)
    except oracledb.Error as e:
        print(f"Error:  {e}")
    
    try: 
        connection.cursor().execute("create user sh01 identified by WElcome_123#;")
        connection.cursor().execute("GRANT CREATE SESSION, RESOURCE TO sh01;")
        connection.cursor().execute("GRANT UNLIMITED TABLESPACE TO sh01;")
        connection.cursor().execute("BEGIN ORDS_ADMIN.ENABLE_SCHEMA(p_enabled => TRUE, p_schema => UPPER('sh01'), p_url_mapping_type => 'BASE_PATH', p_url_mapping_pattern => LOWER('sh01'), p_auto_rest_auth => TRUE); END;")
        connection.cursor().execute("CREATE TABLE sh01.customers AS SELECT * FROM sh.customers;")
        connection.cursor().execute("CREATE TABLE sh01.countries AS SELECT * FROM sh.countries;")
        connection.cursor().execute("CREATE TABLE sh01.sales AS SELECT * FROM sh.sales;")
        connection.cursor().execute("ALTER TABLE SH01.CUSTOMERS ADD CONSTRAINT CUSTOMERS_PK PRIMARY KEY (CUST_ID);")
        connection.cursor().execute("ALTER TABLE SH01.SALES ADD CONSTRAINT SALES_PK PRIMARY KEY (PROD_ID, CUST_ID, TIME_ID, CHANNEL_ID, PROMO_ID);")
        connection.cursor().execute("ALTER TABLE SH01.SALES ADD CONSTRAINT SALES_CUSTOMER_FK FOREIGN KEY (CUST_ID) REFERENCES SH01.CUSTOMERS(CUST_ID);")
        connection.cursor().execute("CREATE TABLE SH01.PAYMENTS (   Payment_ID NUMBER PRIMARY KEY,   Customer_ID NUMBER,   Sale_ID NUMBER,   Payment_Amount NUMBER NOT NULL,   Payment_Date DATE NOT NULL,   Payment_Method VARCHAR2(50),   VISA VARCHAR2(16),   AMEX VARCHAR2(15),   DISCOVER VARCHAR2(16),   MC VARCHAR2(16), BANKING_ACCOUNT VARCHAR2(17),   ROUTING_NUMBER VARCHAR2(9),   FOREIGN KEY (Customer_ID) REFERENCES SH01.CUSTOMERS(CUST_ID));")
    except oracledb.Error as e:
        print(f"Error:  {e}")

    connection.close()
    print(f"connection closed")
except oracledb.Error as e:
    print(f"Error connecting to database: {e}")

print(f"complete")