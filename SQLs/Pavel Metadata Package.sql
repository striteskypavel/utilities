CREATE OR REPLACE PACKAGE PAVEL_STRITESKY_METADATA_PROCEDURES AS
  PROCEDURE count_rows_in_tables_activations;
  PROCEDURE count_rows_in_tables_activations_seconds;
  PROCEDURE count_rows_in_tables_factor_data;
  PROCEDURE count_rows_in_tables_energy_bids_and_reserves;
  PROCEDURE count_rows_in_tables_energy_bids_and_reserves_seconds; 
  PROCEDURE count_rows_in_tables_measurements;
  PROCEDURE count_rows_in_tables_qualifications;
  PROCEDURE count_rows_in_tables_prices_and_exchange_rates;
  PROCEDURE count_rows_in_tables_prices_and_exchange_rates_seconds;
  PROCEDURE count_rows_in_tables_spectrum_data_seconds;
  PROCEDURE count_rows_in_tables_spectrum_data;
  PROCEDURE count_rows_in_tables_schedules;

  PROCEDURE fix_process_recreate_names;
  PROCEDURE set_process_to_asynchronous_recreate_process;
  PROCEDURE fix_process_category_create;
  PROCEDURE set_process_to_asynchronous_create_process;

  PROCEDURE update_second_data_activations_all (
      from_time IN TIMESTAMP,
      to_time IN TIMESTAMP
  );
  PROCEDURE update_second_data_energy_bids_and_reserves_all (
      from_time IN TIMESTAMP,
      to_time IN TIMESTAMP
  );
  PROCEDURE update_second_prices_all (
      from_time IN TIMESTAMP,
      to_time IN TIMESTAMP
  );
  PROCEDURE update_input_data_activations_all (
      from_time IN TIMESTAMP,
      to_time IN TIMESTAMP
  );
  PROCEDURE update_input_data_factor_data_all (
      from_time IN TIMESTAMP,
      to_time IN TIMESTAMP
  );
  PROCEDURE update_input_data_energy_bids_and_reserves_all (
      from_time IN TIMESTAMP,
      to_time IN TIMESTAMP
  );
  PROCEDURE update_input_data_measurements_all (
      from_time IN TIMESTAMP,
      to_time IN TIMESTAMP
  );
  PROCEDURE update_input_data_qualifications_all (
      from_time IN TIMESTAMP,
      to_time IN TIMESTAMP
  );
  PROCEDURE update_input_data_prices_and_exchanges_all (
      from_time IN TIMESTAMP,
      to_time IN TIMESTAMP
  );
  PROCEDURE update_input_data_schedules_all (
      from_time IN TIMESTAMP,
      to_time IN TIMESTAMP
  );
END PAVEL_STRITESKY_METADATA_PROCEDURES;


/

create or replace PACKAGE BODY PAVEL_STRITESKY_METADATA_PROCEDURES AS

  PROCEDURE count_rows_in_tables_activations IS
    v_count NUMBER;
  BEGIN
    FOR r IN (
        SELECT t201data_table 
        FROM t201timeseries 
        WHERE t206entity IN (
            SELECT oid 
            FROM t206entity 
            WHERE get_full_code(OID) = '\SS_INPUT_DATA\ACTIVATION\ACTIVATION'
        ) 
        AND t201data_table IS NOT NULL 
        AND T201IS_SYSTEM = 0
        AND T201DATA_TABLE NOT LIKE '%TSVIEW_99601000004987721%'
    ) LOOP
        EXECUTE IMMEDIATE 'SELECT COUNT(*) FROM ' || r.t201data_table INTO v_count;
        DBMS_OUTPUT.PUT_LINE('Table:  ' || r.t201data_table || ' has ' || v_count || ' rows.');
    END LOOP;
  END count_rows_in_tables_activations;

  PROCEDURE count_rows_in_tables_activations_seconds IS
    v_count NUMBER;
  BEGIN
    FOR r IN (
        SELECT t201data_table 
        FROM t201timeseries 
        WHERE t206entity IN (
            SELECT oid 
            FROM t206entity 
            WHERE get_full_code(OID) = '\SS_INPUT_DATA\ACTIVATION\ACTIVATION_SECOND'
        ) 
        AND t201data_table IS NOT NULL 
        AND T201IS_SYSTEM = 0
        AND T201DATA_TABLE NOT LIKE '%TSVIEW_99601000004987721%'
    ) LOOP
        EXECUTE IMMEDIATE 'SELECT COUNT(*) FROM ' || r.t201data_table INTO v_count;
        DBMS_OUTPUT.PUT_LINE('Table:  ' || r.t201data_table || ' has ' || v_count || ' rows.');
    END LOOP;
  END count_rows_in_tables_activations_seconds;

  PROCEDURE count_rows_in_tables_factor_data IS
    v_count NUMBER;
  BEGIN
    FOR r IN (
        SELECT t201data_table 
        FROM t201timeseries 
        WHERE t206entity IN (
            SELECT oid 
            FROM t206entity 
            WHERE get_full_code(OID) = '\SS_INPUT_DATA\FACTOR_DATA\FACTOR_DATA'
        ) 
        AND t201data_table IS NOT NULL 
        AND T201IS_SYSTEM = 0
        AND T201DATA_TABLE NOT LIKE '%TSVIEW_99601000004987721%'
    ) LOOP
        EXECUTE IMMEDIATE 'SELECT COUNT(*) FROM ' || r.t201data_table INTO v_count;
        DBMS_OUTPUT.PUT_LINE('Table:  ' || r.t201data_table || ' has ' || v_count || ' rows.');
    END LOOP;
  END count_rows_in_tables_factor_data;

  PROCEDURE count_rows_in_tables_energy_bids_and_reserves IS
    v_count NUMBER;
  BEGIN
    FOR r IN (
        SELECT t201data_table 
        FROM t201timeseries 
        WHERE t206entity IN (
            SELECT oid 
            FROM t206entity 
            WHERE get_full_code(OID) = '\SS_INPUT_DATA\ENERGY_BIDS_AND_RESERVES\ENERGY_BID_AND_RESERVES'
        ) 
        AND t201data_table IS NOT NULL 
        AND T201IS_SYSTEM = 0
        AND T201DATA_TABLE NOT LIKE '%TSVIEW_99601000004987721%'
    ) LOOP
        EXECUTE IMMEDIATE 'SELECT COUNT(*) FROM ' || r.t201data_table INTO v_count;
        DBMS_OUTPUT.PUT_LINE('Table:  ' || r.t201data_table || ' has ' || v_count || ' rows.');
    END LOOP;
  END count_rows_in_tables_energy_bids_and_reserves;

  PROCEDURE count_rows_in_tables_energy_bids_and_reserves_seconds IS
    v_count NUMBER;
  BEGIN
    FOR r IN (
        SELECT t201data_table 
        FROM t201timeseries 
        WHERE t206entity IN (
            SELECT oid 
            FROM t206entity 
            WHERE get_full_code(OID) = '\SS_INPUT_DATA\ENERGY_BIDS_AND_RESERVES\ENERGY_BID_AND_RESERVES_SECOND'
        ) 
        AND t201data_table IS NOT NULL 
        AND T201IS_SYSTEM = 0
        AND T201DATA_TABLE NOT LIKE '%TSVIEW_99601000004987721%'
    ) LOOP
        EXECUTE IMMEDIATE 'SELECT COUNT(*) FROM ' || r.t201data_table INTO v_count;
        DBMS_OUTPUT.PUT_LINE('Table:  ' || r.t201data_table || ' has ' || v_count || ' rows.');
    END LOOP;
  END count_rows_in_tables_energy_bids_and_reserves_seconds;

  PROCEDURE count_rows_in_tables_measurements IS
    v_count NUMBER;
  BEGIN
    FOR r IN (
        SELECT t201data_table 
        FROM t201timeseries 
        WHERE t206entity IN (
            SELECT oid 
            FROM t206entity 
            WHERE get_full_code(OID) = '\SS_INPUT_DATA\MEASUREMENTS\MEASUREMENTS'
        ) 
        AND t201data_table IS NOT NULL 
        AND T201IS_SYSTEM = 0
        AND T201DATA_TABLE NOT LIKE '%TSVIEW_99601000004987721%'
    ) LOOP
        EXECUTE IMMEDIATE 'SELECT COUNT(*) FROM ' || r.t201data_table INTO v_count;
        DBMS_OUTPUT.PUT_LINE('Table:  ' || r.t201data_table || ' has ' || v_count || ' rows.');
    END LOOP;
  END count_rows_in_tables_measurements;

  PROCEDURE count_rows_in_tables_operational_state IS
    v_count NUMBER;
  BEGIN
    FOR r IN (
        SELECT t201data_table 
        FROM t201timeseries 
        WHERE t206entity IN (
            SELECT oid 
            FROM t206entity 
            WHERE get_full_code(OID) = '\SS_INPUT_DATA\OPERATIONAL_STATE\OPERATIONAL_STATE'
        ) 
        AND t201data_table IS NOT NULL 
        AND T201IS_SYSTEM = 0
        AND T201DATA_TABLE NOT LIKE '%TSVIEW_99601000004987721%'
    ) LOOP
        EXECUTE IMMEDIATE 'SELECT COUNT(*) FROM ' || r.t201data_table INTO v_count;
        DBMS_OUTPUT.PUT_LINE('Table:  ' || r.t201data_table || ' has ' || v_count || ' rows.');
    END LOOP;
  END count_rows_in_tables_operational_state;

  PROCEDURE count_rows_in_tables_qualifications IS
    v_count NUMBER;
  BEGIN
    FOR r IN (
        SELECT t201data_table 
        FROM t201timeseries 
        WHERE t206entity IN (
            SELECT oid 
            FROM t206entity 
            WHERE get_full_code(OID) = '\SS_INPUT_DATA\QUALIFICATIONS\QUALIFICATIONS'
        ) 
        AND t201data_table IS NOT NULL 
        AND T201IS_SYSTEM = 0
        AND T201DATA_TABLE NOT LIKE '%TSVIEW_99601000004987721%'
    ) LOOP
        EXECUTE IMMEDIATE 'SELECT COUNT(*) FROM ' || r.t201data_table INTO v_count;
        DBMS_OUTPUT.PUT_LINE('Table:  ' || r.t201data_table || ' has ' || v_count || ' rows.');
    END LOOP;
  END count_rows_in_tables_qualifications;

  PROCEDURE count_rows_in_tables_prices_and_exchange_rates IS
    v_count NUMBER;
  BEGIN
    FOR r IN (
        SELECT t201data_table 
        FROM t201timeseries 
        WHERE t206entity IN (
            SELECT oid 
            FROM t206entity 
            WHERE get_full_code(OID) = '\SS_INPUT_DATA\PRICES_AND_RATES\PRICES_AND_EXCHANGE_RATES'
        ) 
        AND t201data_table IS NOT NULL 
        AND T201IS_SYSTEM = 0
        AND T201DATA_TABLE NOT LIKE '%TSVIEW_99601000004987721%'
    ) LOOP
        EXECUTE IMMEDIATE 'SELECT COUNT(*) FROM ' || r.t201data_table INTO v_count;
        DBMS_OUTPUT.PUT_LINE('Table:  ' || r.t201data_table || ' has ' || v_count || ' rows.');
    END LOOP;
  END count_rows_in_tables_prices_and_exchange_rates;

  PROCEDURE count_rows_in_tables_prices_and_exchange_rates_seconds IS
    v_count NUMBER;
  BEGIN
    FOR r IN (
        SELECT t201data_table 
        FROM t201timeseries 
        WHERE t206entity IN (
            SELECT oid 
            FROM t206entity 
            WHERE get_full_code(OID) = '\SS_INPUT_DATA\PRICES_AND_RATES\PRICES_AND_EXCHANGE_RATES_SECOND'
        ) 
        AND t201data_table IS NOT NULL 
        AND T201IS_SYSTEM = 0
        AND T201DATA_TABLE NOT LIKE '%TSVIEW_99601000004987721%'
    ) LOOP
        EXECUTE IMMEDIATE 'SELECT COUNT(*) FROM ' || r.t201data_table INTO v_count;
        DBMS_OUTPUT.PUT_LINE('Table:  ' || r.t201data_table || ' has ' || v_count || ' rows.');
    END LOOP;
  END count_rows_in_tables_prices_and_exchange_rates_seconds;

  PROCEDURE count_rows_in_tables_spectrum_data_seconds IS
    v_count NUMBER;
  BEGIN
    FOR r IN (
        SELECT t201data_table 
        FROM t201timeseries 
        WHERE t206entity IN (
            SELECT oid 
            FROM t206entity 
            WHERE get_full_code(OID) = '\SS_INPUT_DATA\SPECTRUM\SPECTRUM_DATA_SECOND'
        ) 
        AND t201data_table IS NOT NULL 
        AND T201IS_SYSTEM = 0
        AND T201DATA_TABLE NOT LIKE '%TSVIEW_99601000004987721%'
    ) LOOP
        EXECUTE IMMEDIATE 'SELECT COUNT(*) FROM ' || r.t201data_table INTO v_count;
        DBMS_OUTPUT.PUT_LINE('Table:  ' || r.t201data_table || ' has ' || v_count || ' rows.');
    END LOOP;
  END count_rows_in_tables_spectrum_data_seconds;

  PROCEDURE count_rows_in_tables_spectrum_data IS
    v_count NUMBER;
  BEGIN
    FOR r IN (
        SELECT t201data_table 
        FROM t201timeseries 
        WHERE t206entity IN (
            SELECT oid 
            FROM t206entity 
            WHERE get_full_code(OID) = '\SS_INPUT_DATA\SPECTRUM\SPECTRUM_DATA'
        ) 
        AND t201data_table IS NOT NULL 
        AND T201IS_SYSTEM = 0
        AND T201DATA_TABLE NOT LIKE '%TSVIEW_99601000004987721%'
    ) LOOP
        EXECUTE IMMEDIATE 'SELECT COUNT(*) FROM ' || r.t201data_table INTO v_count;
        DBMS_OUTPUT.PUT_LINE('Table:  ' || r.t201data_table || ' has ' || v_count || ' rows.');
    END LOOP;
  END count_rows_in_tables_spectrum_data;

  PROCEDURE count_rows_in_tables_schedules IS
    v_count NUMBER;
  BEGIN
    FOR r IN (
        SELECT t201data_table 
        FROM t201timeseries 
        WHERE t206entity IN (
            SELECT oid 
            FROM t206entity 
            WHERE get_full_code(OID) LIKE '%SCHEDULES%'
        ) 
        AND t201data_table IS NOT NULL 
        AND T201IS_SYSTEM = 0
        AND T201DATA_TABLE NOT LIKE '%TSVIEW_99601000004987721%'
    ) LOOP
        EXECUTE IMMEDIATE 'SELECT COUNT(*) FROM ' || r.t201data_table INTO v_count;
        DBMS_OUTPUT.PUT_LINE('Table:  ' || r.t201data_table || ' has ' || v_count || ' rows.');
    END LOOP;
  END count_rows_in_tables_schedules;

  PROCEDURE fix_process_recreate_names IS
  BEGIN
    UPDATE t801process
    SET T801NAME = 'Recreate'
    WHERE t801code LIKE 'RECREATE%' AND T458OBJECT_CLASS = 'BUL';
  END fix_process_recreate_names;

  PROCEDURE set_process_to_asynchronous_recreate_process IS
  BEGIN
    UPDATE t801process
    SET T801IS_RUN_SYNCHRONOUS = 0
    WHERE t801code LIKE 'RECREATE%' AND T458OBJECT_CLASS = 'BUL';
  END set_process_to_asynchronous_recreate_process;

  PROCEDURE fix_process_category_create IS
  BEGIN
    UPDATE t801process
    SET T441PROCESS_CATHEGORY = 'CATHEGORY_OPEN'
    WHERE t801code LIKE 'CREATE%' AND T458OBJECT_CLASS = 'BUL';
  END fix_process_category_create;

  PROCEDURE set_process_to_asynchronous_create_process IS
  BEGIN
    UPDATE t801process
    SET T801IS_RUN_SYNCHRONOUS = 0
    WHERE t801code LIKE 'CREATE%' AND T458OBJECT_CLASS = 'BUL';
  END set_process_to_asynchronous_create_process;

  PROCEDURE update_second_data_activations_all (
      from_time IN TIMESTAMP,
      to_time IN TIMESTAMP
  ) IS
      v_rows_updated NUMBER;
  BEGIN
      FOR r IN (
          SELECT t201data_table 
          FROM t201timeseries 
          WHERE t206entity IN (
              SELECT oid 
              FROM t206entity 
              WHERE get_full_code(OID) LIKE '%\SS_INPUT_DATA\ACTIVATION\ACTIVATION_SECOND%'
          ) 
          AND t201data_table IS NOT NULL 
          AND T201IS_SYSTEM = 0
      ) LOOP
          EXECUTE IMMEDIATE 'UPDATE ' || r.t201data_table || 
                            ' SET TS_VALUE = ''1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1'' ' ||
                            ' WHERE FROM_TIME >= :1 AND TO_TIME <= :2'
          USING from_time, to_time;

          v_rows_updated := SQL%ROWCOUNT;
          DBMS_OUTPUT.PUT_LINE('Table: ' || r.t201data_table || ' had ' || v_rows_updated || ' rows updated.');
      END LOOP;
  END update_second_data_activations_all;

  PROCEDURE update_second_data_energy_bids_and_reserves_all (
      from_time IN TIMESTAMP,
      to_time IN TIMESTAMP
  ) IS
      v_rows_updated NUMBER;
  BEGIN
      FOR r IN (
          SELECT t201data_table 
          FROM t201timeseries 
          WHERE t206entity IN (
              SELECT oid 
              FROM t206entity 
              WHERE get_full_code(OID) = '\SS_INPUT_DATA\ENERGY_BIDS_AND_RESERVES\ENERGY_BID_AND_RESERVES_SECOND'
          ) 
          AND t201data_table IS NOT NULL 
          AND T201IS_SYSTEM = 0
      ) LOOP
          EXECUTE IMMEDIATE 'UPDATE ' || r.t201data_table || 
                            ' SET TS_VALUE = ''1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1'' ' ||
                            ' WHERE FROM_TIME >= :1 AND TO_TIME <= :2'
          USING from_time, to_time;

          v_rows_updated := SQL%ROWCOUNT;
          DBMS_OUTPUT.PUT_LINE('Table: ' || r.t201data_table || ' had ' || v_rows_updated || ' rows updated.');
      END LOOP;
  END update_second_data_energy_bids_and_reserves_all;

  PROCEDURE update_second_prices_all (
      from_time IN TIMESTAMP,
      to_time IN TIMESTAMP
  ) IS
      v_rows_updated NUMBER;
  BEGIN
      FOR r IN (
          SELECT t201data_table 
          FROM t201timeseries 
          WHERE t206entity IN (
              SELECT oid 
              FROM t206entity 
              WHERE get_full_code(OID) = '\SS_INPUT_DATA\PRICES_AND_RATES\PRICES_AND_EXCHANGE_RATES_SECOND'
          ) 
          AND t201data_table IS NOT NULL 
          AND T201IS_SYSTEM = 0
      ) LOOP
          EXECUTE IMMEDIATE 'UPDATE ' || r.t201data_table || 
                            ' SET TS_VALUE = ''1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1'' ' ||
                            ' WHERE FROM_TIME >= :1 AND TO_TIME <= :2'
          USING from_time, to_time;

          v_rows_updated := SQL%ROWCOUNT;
          DBMS_OUTPUT.PUT_LINE('Table: ' || r.t201data_table || ' had ' || v_rows_updated || ' rows updated.');
      END LOOP;
  END update_second_prices_all;

  PROCEDURE update_input_data_activations_all (
      from_time IN TIMESTAMP,
      to_time IN TIMESTAMP
  ) IS
      v_rows_updated NUMBER;
  BEGIN
      FOR r IN (
          SELECT t201data_table 
          FROM t201timeseries 
          WHERE t206entity IN (
              SELECT oid 
              FROM t206entity 
              WHERE get_full_code(OID) = '\SS_INPUT_DATA\ACTIVATION\ACTIVATION'
          ) 
          AND t201data_table IS NOT NULL 
          AND T201IS_SYSTEM = 0
          AND T405TYPE = 'TS_PRIMARY'
              and T201DATA_TABLE like '%TT%'
           AND GET_FULL_CODE(OID) != '\SS_INPUT_DATA\ACTIVATION\ACTIVATION\TSO_SCHEDULE_MODIFICATION_RIR_START_UP_PRICE'
      ) LOOP
          EXECUTE IMMEDIATE 'UPDATE ' || r.t201data_table || 
                            ' SET TS_VALUE = 1 ' ||
                            ' WHERE FROM_TIME >= :1 AND TO_TIME <= :2'
          USING from_time, to_time;

          v_rows_updated := SQL%ROWCOUNT;
          DBMS_OUTPUT.PUT_LINE('Table: ' || r.t201data_table || ' had ' || v_rows_updated || ' rows updated.');
      END LOOP;
  END update_input_data_activations_all;

  PROCEDURE update_input_data_factor_data_all (
      from_time IN TIMESTAMP,
      to_time IN TIMESTAMP
  ) IS
      v_rows_updated NUMBER;
  BEGIN
      FOR r IN (
          SELECT t201data_table 
          FROM t201timeseries 
          WHERE t206entity IN (
              SELECT oid 
              FROM t206entity 
              WHERE get_full_code(OID) = '\SS_INPUT_DATA\FACTOR_DATA\FACTOR_DATA'
          ) 
          AND t201data_table IS NOT NULL 
          AND T201IS_SYSTEM = 0
          AND T405TYPE = 'TS_PRIMARY'
              and T201DATA_TABLE like '%TT%'
      ) LOOP
          EXECUTE IMMEDIATE 'UPDATE ' || r.t201data_table || 
                            ' SET TS_VALUE = 1 ' ||
                            ' WHERE FROM_TIME >= :1 AND TO_TIME <= :2'
          USING from_time, to_time;

          v_rows_updated := SQL%ROWCOUNT;
          DBMS_OUTPUT.PUT_LINE('Table: ' || r.t201data_table || ' had ' || v_rows_updated || ' rows updated.');
      END LOOP;
  END update_input_data_factor_data_all;

  PROCEDURE update_input_data_energy_bids_and_reserves_all (
      from_time IN TIMESTAMP,
      to_time IN TIMESTAMP
  ) IS
      v_rows_updated NUMBER;
  BEGIN
      FOR r IN (
          SELECT t201data_table 
          FROM t201timeseries 
          WHERE t206entity IN (
              SELECT oid 
              FROM t206entity 
              WHERE get_full_code(OID) = '\SS_INPUT_DATA\ENERGY_BIDS_AND_RESERVES\ENERGY_BID_AND_RESERVES'
          ) 
          AND t201data_table IS NOT NULL 
          AND T201IS_SYSTEM = 0
          AND T405TYPE = 'TS_PRIMARY'
          and T201DATA_TABLE like '%TT%'
      ) LOOP
          EXECUTE IMMEDIATE 'UPDATE ' || r.t201data_table || 
                            ' SET TS_VALUE = 1 ' ||
                            ' WHERE FROM_TIME >= :1 AND TO_TIME <= :2'
          USING from_time, to_time;

          v_rows_updated := SQL%ROWCOUNT;
          DBMS_OUTPUT.PUT_LINE('Table: ' || r.t201data_table || ' had ' || v_rows_updated || ' rows updated.');
      END LOOP;
  END update_input_data_energy_bids_and_reserves_all;

  PROCEDURE update_input_data_measurements_all (
      from_time IN TIMESTAMP,
      to_time IN TIMESTAMP
  ) IS
      v_rows_updated NUMBER;
  BEGIN
      FOR r IN (
          SELECT t201data_table 
          FROM t201timeseries 
          WHERE t206entity IN (
              SELECT oid 
              FROM t206entity 
              WHERE get_full_code(OID) = '\SS_INPUT_DATA\MEASUREMENTS\MEASUREMENTS'
          ) 
          AND t201data_table IS NOT NULL 
          AND T201IS_SYSTEM = 0
          AND T405TYPE = 'TS_PRIMARY'
              and T201DATA_TABLE like '%TT%'
      ) LOOP
          EXECUTE IMMEDIATE 'UPDATE ' || r.t201data_table || 
                            ' SET TS_VALUE = 1 ' ||
                            ' WHERE FROM_TIME >= :1 AND TO_TIME <= :2'
          USING from_time, to_time;

          v_rows_updated := SQL%ROWCOUNT;
          DBMS_OUTPUT.PUT_LINE('Table: ' || r.t201data_table || ' had ' || v_rows_updated || ' rows updated.');
      END LOOP;
  END update_input_data_measurements_all;



  PROCEDURE update_input_data_qualifications_all (
      from_time IN TIMESTAMP,
      to_time IN TIMESTAMP
  ) IS
      v_rows_updated NUMBER;
  BEGIN
      FOR r IN (
          SELECT t201data_table 
          FROM t201timeseries 
          WHERE t206entity IN (
              SELECT oid 
              FROM t206entity 
              WHERE get_full_code(OID) = '\SS_INPUT_DATA\QUALIFICATIONS\QUALIFICATIONS'
          ) 
          AND t201data_table IS NOT NULL 
          AND T201IS_SYSTEM = 0
          AND T405TYPE = 'TS_PRIMARY'
              and T201DATA_TABLE like '%TT%'
      ) LOOP
          EXECUTE IMMEDIATE 'UPDATE ' || r.t201data_table || 
                            ' SET TS_VALUE = 1 ' ||
                            ' WHERE FROM_TIME >= :1 AND TO_TIME <= :2'
          USING from_time, to_time;

          v_rows_updated := SQL%ROWCOUNT;
          DBMS_OUTPUT.PUT_LINE('Table: ' || r.t201data_table || ' had ' || v_rows_updated || ' rows updated.');
      END LOOP;
  END update_input_data_qualifications_all;

  PROCEDURE update_input_data_prices_and_exchanges_all (
      from_time IN TIMESTAMP,
      to_time IN TIMESTAMP
  ) IS
      v_rows_updated NUMBER;
  BEGIN
      FOR r IN (
          SELECT t201data_table 
          FROM t201timeseries 
          WHERE t206entity IN (
              SELECT oid 
              FROM t206entity 
              WHERE get_full_code(OID) = '\SS_INPUT_DATA\PRICES_AND_RATES\PRICES_AND_EXCHANGE_RATES'
          ) 
          AND t201data_table IS NOT NULL 
          AND T201IS_SYSTEM = 0
          AND T405TYPE = 'TS_PRIMARY'
              and T201DATA_TABLE like '%TT%'
      ) LOOP
          EXECUTE IMMEDIATE 'UPDATE ' || r.t201data_table || 
                            ' SET TS_VALUE = 1 ' ||
                            ' WHERE FROM_TIME >= :1 AND TO_TIME <= :2'
          USING from_time, to_time;

          v_rows_updated := SQL%ROWCOUNT;
          DBMS_OUTPUT.PUT_LINE('Table: ' || r.t201data_table || ' had ' || v_rows_updated || ' rows updated.');
      END LOOP;
  END update_input_data_prices_and_exchanges_all;

  PROCEDURE update_input_data_schedules_all (
      from_time IN TIMESTAMP,
      to_time IN TIMESTAMP
  ) IS
      v_rows_updated NUMBER;
  BEGIN
      FOR r IN (
          SELECT t201data_table 
          FROM t201timeseries 
          WHERE t206entity IN (
              SELECT oid 
              FROM t206entity 
              WHERE get_full_code(OID) = '\SS_INPUT_DATA\SCHEDULES\SCHEDULES'
          ) 
          AND t201data_table IS NOT NULL 
          AND T201IS_SYSTEM = 0
          AND T405TYPE = 'TS_PRIMARY'
              and T201DATA_TABLE like '%TT%'
      ) LOOP
          EXECUTE IMMEDIATE 'UPDATE ' || r.t201data_table || 
                            ' SET TS_VALUE = 1 ' ||
                            ' WHERE FROM_TIME >= :1 AND TO_TIME <= :2'
          USING from_time, to_time;

          v_rows_updated := SQL%ROWCOUNT;
          DBMS_OUTPUT.PUT_LINE('Table: ' || r.t201data_table || ' had ' || v_rows_updated || ' rows updated.');
      END LOOP;
  END update_input_data_schedules_all;

END PAVEL_STRITESKY_METADATA_PROCEDURES;




-- CALLING PROCEDURES 

-- Volání procedur from_time a to_time pro červenec
BEGIN
    PAVEL_STRITESKY_METADATA_PROCEDURES.update_input_data_measurements_all(
        TO_TIMESTAMP('2024-07-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS'),
        TO_TIMESTAMP('2024-07-31 23:59:59', 'YYYY-MM-DD HH24:MI:SS')
    );
END;
/

BEGIN
    PAVEL_STRITESKY_METADATA_PROCEDURES.update_input_data_schedules_all(
        TO_TIMESTAMP('2024-07-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS'),
        TO_TIMESTAMP('2024-07-31 23:59:59', 'YYYY-MM-DD HH24:MI:SS')
    );
END;
/

-- Volání procedur from_time a to_time pro červenec
BEGIN
    PAVEL_STRITESKY_METADATA_PROCEDURES.update_second_data_activations_all(
        TO_TIMESTAMP('2024-07-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS'),
        TO_TIMESTAMP('2024-07-31 23:59:59', 'YYYY-MM-DD HH24:MI:SS')
    );
END;
/

BEGIN
    PAVEL_STRITESKY_METADATA_PROCEDURES.update_second_data_energy_bids_and_reserves_all(
        TO_TIMESTAMP('2024-07-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS'),
        TO_TIMESTAMP('2024-07-31 23:59:59', 'YYYY-MM-DD HH24:MI:SS')
    );
END;
/

BEGIN
    PAVEL_STRITESKY_METADATA_PROCEDURES.update_second_prices_all(
        TO_TIMESTAMP('2024-07-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS'),
        TO_TIMESTAMP('2024-07-31 23:59:59', 'YYYY-MM-DD HH24:MI:SS')
    );
END;
/

BEGIN
    PAVEL_STRITESKY_METADATA_PROCEDURES.update_input_data_activations_all(
        TO_TIMESTAMP('2024-07-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS'),
        TO_TIMESTAMP('2024-07-31 23:59:59', 'YYYY-MM-DD HH24:MI:SS')
    );
END;
/

BEGIN
    PAVEL_STRITESKY_METADATA_PROCEDURES.update_input_data_factor_data_all(
        TO_TIMESTAMP('2024-07-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS'),
        TO_TIMESTAMP('2024-07-31 23:59:59', 'YYYY-MM-DD HH24:MI:SS')
    );
END;
/

BEGIN
    PAVEL_STRITESKY_METADATA_PROCEDURES.update_input_data_energy_bids_and_reserves_all(
        TO_TIMESTAMP('2024-07-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS'),
        TO_TIMESTAMP('2024-07-31 23:59:59', 'YYYY-MM-DD HH24:MI:SS')
    );
END;
/

BEGIN
    PAVEL_STRITESKY_METADATA_PROCEDURES.update_input_data_measurements_all(
        TO_TIMESTAMP('2024-07-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS'),
        TO_TIMESTAMP('2024-07-31 23:59:59', 'YYYY-MM-DD HH24:MI:SS')
    );
END;
/


BEGIN
    PAVEL_STRITESKY_METADATA_PROCEDURES.update_input_data_qualifications_all(
        TO_TIMESTAMP('2024-07-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS'),
        TO_TIMESTAMP('2024-07-31 23:59:59', 'YYYY-MM-DD HH24:MI:SS')
    );
END;
/

BEGIN
    PAVEL_STRITESKY_METADATA_PROCEDURES.update_input_data_prices_and_exchanges_all(
        TO_TIMESTAMP('2024-07-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS'),
        TO_TIMESTAMP('2024-07-31 23:59:59', 'YYYY-MM-DD HH24:MI:SS')
    );
END;
/

-- Volání procedur pro počítání řádků v tabulkách
BEGIN
  PAVEL_STRITESKY_METADATA_PROCEDURES.count_rows_in_tables_activations;
END;
/

BEGIN
  PAVEL_STRITESKY_METADATA_PROCEDURES.count_rows_in_tables_activations_seconds;
END;
/

BEGIN
  PAVEL_STRITESKY_METADATA_PROCEDURES.count_rows_in_tables_factor_data;
END;
/

BEGIN
  PAVEL_STRITESKY_METADATA_PROCEDURES.count_rows_in_tables_energy_bids_and_reserves;
END;
/

BEGIN
  PAVEL_STRITESKY_METADATA_PROCEDURES.count_rows_in_tables_energy_bids_and_reserves_seconds;
END;
/

BEGIN
  PAVEL_STRITESKY_METADATA_PROCEDURES.count_rows_in_tables_measurements;
END;
/

BEGIN
  PAVEL_STRITESKY_METADATA_PROCEDURES.count_rows_in_tables_qualifications;
END;
/

BEGIN
  PAVEL_STRITESKY_METADATA_PROCEDURES.count_rows_in_tables_prices_and_exchange_rates;
END;
/

BEGIN
  PAVEL_STRITESKY_METADATA_PROCEDURES.count_rows_in_tables_prices_and_exchange_rates_seconds;
END;
/

BEGIN
  PAVEL_STRITESKY_METADATA_PROCEDURES.count_rows_in_tables_spectrum_data_seconds;
END;
/

BEGIN
  PAVEL_STRITESKY_METADATA_PROCEDURES.count_rows_in_tables_spectrum_data;
END;
/

BEGIN
  PAVEL_STRITESKY_METADATA_PROCEDURES.count_rows_in_tables_schedules;
END;
/

-- Volání procedur pro opravy a nastavení procesů
BEGIN
  PAVEL_STRITESKY_METADATA_PROCEDURES.fix_process_recreate_names;
END;
/

BEGIN
  PAVEL_STRITESKY_METADATA_PROCEDURES.set_process_to_asynchronous_recreate_process;
END;
/

BEGIN
  PAVEL_STRITESKY_METADATA_PROCEDURES.fix_process_category_create;
END;
/

BEGIN
  PAVEL_STRITESKY_METADATA_PROCEDURES.set_process_to_asynchronous_create_process;
END;
/


1. Summary*

This user story outlines the implementation of the Imbalance GUI screens, as detailed in [chapter 10.5|https://sharepoint.mavir.local/Projektek/MERACE/8_Unicorn/8.8%20Detail%20Design/8.8.1%20Business%20Documents/8.8.1.1%20Settlement%20Specifications/MERACE-DD-003-Settlements%20(10%20-%20Control%20Energy).docx?d=wf485d9aa9782417eb053c34bc7f416ff], within the scope of the project. Namely, then:

- Daily BRP Schedules
- Monthly BRP Schedules
- Monthly BRP Schedules
- Daily BRP Measurements
- Monthly BRP Measurements
- Daily Final Position and Imbalance Adjustment
- Monthly Final Position and Imbalance Adjustment
- Daily Detailed Ordered Deviation
- Monthly Detailed Ordered Deviation
- Monthly BRP Imbalance
- Daily System Direction and System State
- Monthly System Direction and System State
- Daily BRP Imbalance Price
- Monthly BRP Imbalance Price
- Daily BRP Imbalance Price Details
- Monthly BRP Imbalance Price
- Daily Requested and Activated FRR and IGCC Volumes
- Monthly Requested and Activated AFB and IGCC Volumes
- Daily Activated AFB Fees
- Monthly Activated AFB Fees
- Daily BRP Imbalance Fee
- Monthly BRP Imbalance Fee

*2. Related story* 
- *{color:#de350b}TODO after import to MAVIR JIRA{color}*

*3. Detailed description of use cases and features* 

Within this story, Unicorn will implement GUI for aFRR Balancing Energy defined in chapter 10.2.5 GUI as well as Entity configuration for the Input Data.

*4. Demonstration* 
* Present the configuration of entity
* Present the configuration of views in the database
* Show configuration for views in XML
* Present the views on GUI (view structure, filtering, etc...)