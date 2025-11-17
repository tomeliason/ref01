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
        connection.cursor().execute("CREATE SEQUENCE SH01.PAYMENT_ID_SEQ START WITH 1 INCREMENT BY 1;")

        sql_generate="DECLARE  v_payment_method VARCHAR2(50); v_payment_date DATE; v_visa VARCHAR2(16); v_amex VARCHAR2(15); v_discover VARCHAR2(16);    v_mc VARCHAR2(16); v_banking_account VARCHAR2(17);    v_routing_number VARCHAR2(9); "

        sql_generate=sql_generate+" FUNCTION generate_random_number(p_length IN NUMBER) RETURN VARCHAR2 IS BEGIN   RETURN LPAD(FLOOR(DBMS_RANDOM.VALUE(0, POWER(10, p_length))), p_length, '0');   END; "

        sql_generate=sql_generate+" BEGIN  FOR sale IN (SELECT PROD_ID, CUST_ID, TIME_ID, AMOUNT_SOLD FROM SH01.SALES ) "
#        sql_generate=sql_generate+" BEGIN  FOR sale IN (SELECT PROD_ID, CUST_ID, TIME_ID, AMOUNT_SOLD FROM SH01.SALES WHERE CUST_ID in (103, 131, 147, 156)) "

        sql_generate=sql_generate+" LOOP CASE FLOOR(DBMS_RANDOM.VALUE(0, 5)) WHEN 0 THEN v_payment_method := 'VISA'; WHEN 1 THEN v_payment_method := 'AMEX'; WHEN 2 THEN v_payment_method := 'DISCOVER'; WHEN 3 THEN v_payment_method := 'MC'; WHEN 4 THEN v_payment_method := 'BANK'; END CASE; "

        sql_generate=sql_generate+" v_visa := CASE WHEN v_payment_method = 'VISA' THEN generate_random_number(16) ELSE NULL END; "
        sql_generate=sql_generate+" v_amex := CASE WHEN v_payment_method = 'AMEX' THEN generate_random_number(15) ELSE NULL END; "
        sql_generate=sql_generate+" v_discover := CASE WHEN v_payment_method = 'DISCOVER' THEN generate_random_number(16) ELSE NULL END; "
        sql_generate=sql_generate+" v_mc := CASE WHEN v_payment_method = 'MC' THEN generate_random_number(16) ELSE NULL END; "
        sql_generate=sql_generate+" v_banking_account := CASE WHEN v_payment_method = 'BANK' THEN generate_random_number(17) ELSE NULL END; "
        sql_generate=sql_generate+" v_routing_number := CASE WHEN v_payment_method = 'BANK' THEN generate_random_number(9) ELSE NULL END; "

        sql_generate=sql_generate+" v_payment_date := sale.TIME_ID + DBMS_RANDOM.VALUE(1, 5); "

        sql_generate=sql_generate+" INSERT INTO SH01.PAYMENTS ( Payment_ID, Customer_ID, Sale_ID, Payment_Amount, Payment_Date, Payment_Method, VISA, AMEX, DISCOVER, MC, BANKING_ACCOUNT, ROUTING_NUMBER ) VALUES ( SH01.PAYMENT_ID_SEQ.NEXTVAL, sale.CUST_ID, sale.PROD_ID, sale.AMOUNT_SOLD, v_payment_date, v_payment_method, v_visa, v_amex, v_discover, v_mc, v_banking_account, v_routing_number ); "

        sql_generate=sql_generate+" END LOOP; COMMIT; END; "

        connection.cursor().execute(sql_generate) 

    except oracledb.Error as e:
        print(f"Error:  {e}")

    connection.close()
    print(f"connection closed")
except oracledb.Error as e:
    print(f"Error connecting to database: {e}")

print(f"complete")