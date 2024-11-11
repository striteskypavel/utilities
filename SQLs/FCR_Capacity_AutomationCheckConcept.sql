SET SERVEROUTPUT ON;

-- vždy se musí použít začátek nebo konec měsíce
-- pozor na intervalizaci u factor data, musí být nastavená na měsíc nebo menší
-- pozor na přechod času - zimní, letní 22:00 nebo 23:00

DECLARE
    v_sql VARCHAR2(4000);
    v_time TIMESTAMP;
    v_to_time TIMESTAMP;
    v_time_str VARCHAR2(20);
    v_to_time_str VARCHAR2(20);
    v_value VARCHAR2(4000);
    v_table_name VARCHAR2(100);
    v_t201name VARCHAR2(100);
    v_full_code VARCHAR2(4000);
    v_cursor SYS_REFCURSOR;
BEGIN
    -- Uživatelsky definovaná hodnota from_time a to_time
    v_time := TO_TIMESTAMP('31.07.24 22:00:00', 'DD.MM.RR HH24:MI:SS');
    v_to_time := TO_TIMESTAMP('31.07.24 22:00:00', 'DD.MM.RR HH24:MI:SS');
    v_time_str := TO_CHAR(v_time, 'DD.MM.RR HH24:MI:SS');
    v_to_time_str := TO_CHAR(v_to_time, 'DD.MM.RR HH24:MI:SS');
    
    FOR rec IN (
        SELECT t201data_table,
               t201name,
               get_full_code(oid) AS full_code
        FROM t201timeseries
        WHERE get_full_code(oid) IN (
            '\SS_CONTROL_ENERGY\PREPARATION_SETTLEMENT\PREPARATION_SETTLEMENT\CORRECTED_POWER_PERFORMANCE',
            '\SS_INPUT_DATA\ENERGY_BIDS_AND_RESERVES\ENERGY_BID_AND_RESERVES\FCR_RESERVE_BID_PRICE',
            '\SS_INPUT_DATA\ENERGY_BIDS_AND_RESERVES\ENERGY_BID_AND_RESERVES_SECOND\FCR_CONFIGURED_CHARACTERISTIC',
            '\SS_INPUT_DATA\SPECTRUM\SPECTRUM_DATA_SECOND\FREQUENCY',
            '\SS_INPUT_DATA\FACTOR_DATA\FACTOR_DATA\CONSTANT_TOLERANCE_OF_FCR_POWER',
            '\SS_INPUT_DATA\FACTOR_DATA\FACTOR_DATA\DEVIATION_TOLERANCE_FCR_POWER',
            '\SS_INPUT_DATA\FACTOR_DATA\FACTOR_DATA\AVAILABILITY_TOLERANCE_LEVEL',
            '\SS_INPUT_DATA\ENERGY_BIDS_AND_RESERVES\ENERGY_BID_AND_RESERVES\FCR_REQUESTED_CHARACTERISTICS',
            '\SS_INPUT_DATA\ENERGY_BIDS_AND_RESERVES\ENERGY_BID_AND_RESERVES\FCR_REPLACEMENT_QUANTITY',
            '\SS_INPUT_DATA\ENERGY_BIDS_AND_RESERVES\ENERGY_BID_AND_RESERVES\FCR_REPLACEMENT_PRICE',
            '\SS_INPUT_DATA\FACTOR_DATA\FACTOR_DATA\THRESHOLD',
            '\SS_INPUT_DATA\FACTOR_DATA\FACTOR_DATA\LOW_RATE_PENALTY',
            '\SS_INPUT_DATA\FACTOR_DATA\FACTOR_DATA\HIGH_RATE_PENALTY',
            '\SS_AVAILABILITY\FCR_BALANCING_CAPACITY\HOURLY_FCR_BALANCING_CAPACITY\FCR_POWER_CONFIGURED',
            '\SS_AVAILABILITY\FCR_BALANCING_CAPACITY\HOURLY_FCR_BALANCING_CAPACITY\FCR_LOWER_ACCEPTANCE',
            '\SS_AVAILABILITY\FCR_BALANCING_CAPACITY\HOURLY_FCR_BALANCING_CAPACITY\FCR_UPPER_ACCEPTANCE',
            '\SS_AVAILABILITY\FCR_BALANCING_CAPACITY\HOURLY_FCR_BALANCING_CAPACITY\RATING_AVAILABILITY',
            '\SS_AVAILABILITY\FCR_BALANCING_CAPACITY\HOURLY_FCR_BALANCING_CAPACITY\FCR_RATIO_AVAILABILITY',
            '\SS_AVAILABILITY\FCR_BALANCING_CAPACITY\HOURLY_FCR_BALANCING_CAPACITY\RATING_FCR_AVAILABILITY_QUARTER_HOUR',
            '\SS_AVAILABILITY\FCR_BALANCING_CAPACITY\HOURLY_FCR_BALANCING_CAPACITY\FCR_ACCEPTED_AVAILABILITY',
            '\SS_AVAILABILITY\FCR_BALANCING_CAPACITY\HOURLY_FCR_BALANCING_CAPACITY\FCR_NONFULFILLMENT_AVAILABILITY',
            '\SS_AVAILABILITY\FCR_BALANCING_CAPACITY\HOURLY_FCR_BALANCING_CAPACITY\FCR_AVAILABILITY_FEE',
            '\SS_AVAILABILITY\FCR_BALANCING_CAPACITY\HOURLY_FCR_BALANCING_CAPACITY\SERIAL_NUMBER',
            '\SS_AVAILABILITY\FCR_BALANCING_CAPACITY\HOURLY_FCR_BALANCING_CAPACITY\INCOMPLETE_FCR_PERFORMANCE',
            '\SS_AVAILABILITY\FCR_BALANCING_CAPACITY\HOURLY_FCR_BALANCING_CAPACITY\RATE_PENALTY',
            '\SS_AVAILABILITY\FCR_BALANCING_CAPACITY\HOURLY_FCR_BALANCING_CAPACITY\FCR_ADDITIONAL_COST',
            '\SS_AVAILABILITY\FCR_BALANCING_CAPACITY\HOURLY_FCR_BALANCING_CAPACITY\FCR_PENALTY',
            '\SS_AVAILABILITY\FCR_BALANCING_CAPACITY\HOURLY_FCR_BALANCING_CAPACITY\FCR_ADDITIONAL_COSTS_PARTY',
            '\SS_AVAILABILITY\FCR_BALANCING_CAPACITY\HOURLY_FCR_BALANCING_CAPACITY\FCR_PENALTY_PARTY',
            '\SS_AVAILABILITY\FCR_BALANCING_CAPACITY\MONTHLY_FCR_BALANCING_CAPACITY\FCR_PENALTY_MONTH',
            '\SS_AVAILABILITY\FCR_BALANCING_CAPACITY\MONTHLY_FCR_BALANCING_CAPACITY\FCR_ADDITIONAL_COSTS_MONTH',
            '\SS_AVAILABILITY\FCR_BALANCING_CAPACITY\MONTHLY_FCR_BALANCING_CAPACITY\MONTHLY_FCR_AVAILABILITY_FEE',
            '\SS_AVAILABILITY\FCR_BALANCING_CAPACITY\HOURLY_FCR_BALANCING_CAPACITY\FCR_ACCEPTED_AVAILABILITY',
            '\SS_AVAILABILITY\FCR_BALANCING_CAPACITY\MONTHLY_FCR_BALANCING_CAPACITY\FCR_ADDITIONAL_COSTS_MONTH_PARTY',
            '\SS_AVAILABILITY\FCR_BALANCING_CAPACITY\MONTHLY_FCR_BALANCING_CAPACITY\FCR_PENALTY_MONTH_PARTY'
        )
    ) LOOP
        v_table_name := rec.t201data_table;
        v_t201name := rec.t201name;
        v_full_code := rec.full_code;
        
        IF v_t201name LIKE '%Monthly%' THEN
            v_sql := 'SELECT TO_CHAR(from_time, ''DD.MM.RR HH24:MI:SS'') as from_time, TO_CHAR(TS_VALUE) as TS_VALUE FROM ' || v_table_name || 
                     ' WHERE from_time = TO_TIMESTAMP(''' || v_to_time_str || ''', ''DD.MM.RR HH24:MI:SS'') 
                     AND ROWNUM = 1
                     GROUP BY TO_CHAR(from_time, ''DD.MM.RR HH24:MI:SS''), TO_CHAR(TS_VALUE) 
                     ORDER BY TO_CHAR(from_time, ''DD.MM.RR HH24:MI:SS'') DESC';
        ELSE
            v_sql := 'SELECT TO_CHAR(from_time, ''DD.MM.RR HH24:MI:SS'') as from_time, TO_CHAR(TS_VALUE) as TS_VALUE FROM ' || v_table_name || 
                     ' WHERE from_time = TO_TIMESTAMP(''' || v_time_str || ''', ''DD.MM.RR HH24:MI:SS'') 
                     AND ROWNUM = 1
                     GROUP BY TO_CHAR(from_time, ''DD.MM.RR HH24:MI:SS''), TO_CHAR(TS_VALUE) 
                     ORDER BY TO_CHAR(from_time, ''DD.MM.RR HH24:MI:SS'') DESC';
        END IF;
        
        BEGIN
            OPEN v_cursor FOR v_sql;
            FETCH v_cursor INTO v_time_str, v_value;
            CLOSE v_cursor;
            
            DBMS_OUTPUT.PUT_LINE('Table: ' || v_table_name);
            DBMS_OUTPUT.PUT_LINE('Time Series Name: ' || v_t201name);
            DBMS_OUTPUT.PUT_LINE('from_time: ' || NVL(v_time_str, 'NULL'));
            DBMS_OUTPUT.PUT_LINE('TS_VALUE: ' || NVL(v_value, 'NULL'));
            DBMS_OUTPUT.PUT_LINE('full_code: ' || v_full_code);
            DBMS_OUTPUT.PUT_LINE('----------------------------------------');
        EXCEPTION
            WHEN NO_DATA_FOUND THEN
                DBMS_OUTPUT.PUT_LINE('Table: ' || v_table_name);
                DBMS_OUTPUT.PUT_LINE('Time Series Name: ' || v_t201name);
                DBMS_OUTPUT.PUT_LINE(' - No data found for the specified time.');
                DBMS_OUTPUT.PUT_LINE('full_code: ' || v_full_code);
                DBMS_OUTPUT.PUT_LINE('----------------------------------------');
            WHEN INVALID_NUMBER THEN
                DBMS_OUTPUT.PUT_LINE('Table: ' || v_table_name);
                DBMS_OUTPUT.PUT_LINE('Time Series Name: ' || v_t201name);
                DBMS_OUTPUT.PUT_LINE(' - Error: ORA-01722: invalid number');
                DBMS_OUTPUT.PUT_LINE('full_code: ' || v_full_code);
                DBMS_OUTPUT.PUT_LINE('----------------------------------------');
            WHEN OTHERS THEN
                DBMS_OUTPUT.PUT_LINE('Table: ' || v_table_name);
                DBMS_OUTPUT.PUT_LINE('Time Series Name: ' || v_t201name);
                DBMS_OUTPUT.PUT_LINE(' - Error: ' || SQLERRM);
                DBMS_OUTPUT.PUT_LINE('full_code: ' || v_full_code);
                DBMS_OUTPUT.PUT_LINE('----------------------------------------');
        END;
    END LOOP;
END;
/

