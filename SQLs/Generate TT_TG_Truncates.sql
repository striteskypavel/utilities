CREATE OR REPLACE PACKAGE PAVEL_STRITESKY_METADATA_TRUNCATES AS
  PROCEDURE generate_truncate_statements_activations_seconds;
  PROCEDURE generate_truncate_statements_energy_bids_and_reserves_seconds;
  PROCEDURE generate_truncate_statements_prices_and_exchange_rates_seconds;
  PROCEDURE generate_truncate_statements_activations;
  PROCEDURE generate_truncate_statements_factor_data;
  PROCEDURE generate_truncate_statements_energy_bids_and_reserves;
  PROCEDURE generate_truncate_statements_measurements;
  PROCEDURE generate_truncate_statements_qualifications;
  PROCEDURE generate_truncate_statements_prices_and_exchanges;
  PROCEDURE generate_truncate_statements_schedules;
  PROCEDURE generate_truncate_statements_operational_state;

  PROCEDURE generate_truncate_statements_availability_daily;
  PROCEDURE generate_truncate_statements_control_energy_daily;
  PROCEDURE generate_truncate_statements_settlement_daily;
  PROCEDURE generate_truncate_statements_settlement_afrr_daily;
  PROCEDURE generate_truncate_statements_settlement_balancing_energy_bids_daily;
  PROCEDURE generate_truncate_statements_settlement_mfrr_daily;
  PROCEDURE generate_truncate_statements_tso_tso_daily;

  PROCEDURE generate_truncate_statements_afrr_balancing_capacity_daily;
  PROCEDURE generate_truncate_statements_mfrr_balancing_capacity_daily;
  PROCEDURE generate_truncate_statements_providing_international_assistance_daily;
  PROCEDURE generate_truncate_statements_using_international_assistance_daily;
  PROCEDURE generate_truncate_statements_tso_schedule_modification_rir_daily;
  PROCEDURE generate_truncate_statements_providing_igcc_basic_data_daily;
  PROCEDURE generate_truncate_statements_providing_multilateral_remedial_action_basic_data_daily;

  PROCEDURE generate_truncate_statements_availability_monthly;
  PROCEDURE generate_truncate_statements_control_energy_monthly;
  PROCEDURE generate_truncate_statements_afrr_balancing_capacity_monthly;
  PROCEDURE generate_truncate_statements_fcr_balancing_capacity_monthly;
  PROCEDURE generate_truncate_statements_mfrr_balancing_capacity_monthly;
  PROCEDURE generate_truncate_statements_u_q_control_reactive_power_monthly;
  PROCEDURE generate_truncate_statements_providing_international_assistance_monthly;
  PROCEDURE generate_truncate_statements_using_international_assistance_monthly;
  PROCEDURE generate_truncate_statements_afrr_monthly;
  PROCEDURE generate_truncate_statements_tso_schedule_modification_rir_monthly;
  PROCEDURE generate_truncate_statements_providing_multilateral_remedial_action_basic_data_monthly;
  PROCEDURE generate_truncate_statements_black_start_service_monthly;
  PROCEDURE generate_truncate_statements_measurements_monthly;
  PROCEDURE generate_truncate_statements_mfrr_monthly;

  PROCEDURE generate_truncate_statements_fcr_balancing_capacity_hourly;
  PROCEDURE generate_truncate_statements_schedules_qh;
  PROCEDURE generate_truncate_statements_spectrum_data_qh;
  PROCEDURE generate_truncate_statements_spectrum_data_seconds_qh;
  PROCEDURE generate_truncate_statements_prices_and_exchange_rates_seconds_qh;
  PROCEDURE generate_truncate_statements_afrr_seconds_qh;
  PROCEDURE generate_truncate_statements_activation_second_qh;
  PROCEDURE generate_truncate_statements_mfrr_seconds_qh;
  PROCEDURE generate_truncate_statements_preparation_settlement_qh;
  PROCEDURE generate_truncate_statements_energy_bids_and_reserves_seconds_qh;
END PAVEL_STRITESKY_METADATA_TRUNCATES;
/

CREATE OR REPLACE PACKAGE BODY PAVEL_STRITESKY_METADATA_TRUNCATES AS

  PROCEDURE generate_truncate_statements_activations_seconds IS
    v_sql VARCHAR2(4000);
  BEGIN
    FOR r IN (
        SELECT t201data_table, t201iq_data_table
        FROM t201timeseries 
        WHERE t206entity IN (
            SELECT oid 
            FROM t206entity 
            WHERE get_full_code(OID) LIKE '%\SS_INPUT_DATA\ACTIVATION\ACTIVATION_SECOND%'
        ) 
        AND t201data_table IS NOT NULL 
        AND T201IS_SYSTEM = 0
    ) LOOP
        v_sql := 'TRUNCATE TABLE ' || r.t201data_table || ' ;';
        DBMS_OUTPUT.PUT_LINE(v_sql);
        
        IF r.t201iq_data_table IS NOT NULL THEN
            v_sql := 'TRUNCATE TABLE ' || r.t201iq_data_table || ' ;';
            DBMS_OUTPUT.PUT_LINE(v_sql);
        END IF;
    END LOOP;
  END generate_truncate_statements_activations_seconds;

  PROCEDURE generate_truncate_statements_energy_bids_and_reserves_seconds IS
    v_sql VARCHAR2(4000);
  BEGIN
    FOR r IN (
        SELECT t201data_table, t201iq_data_table
        FROM t201timeseries 
        WHERE t206entity IN (
            SELECT oid 
            FROM t206entity 
            WHERE get_full_code(OID) = '\SS_INPUT_DATA\ENERGY_BIDS_AND_RESERVES\ENERGY_BID_AND_RESERVES_SECOND'
        ) 
        AND t201data_table IS NOT NULL 
        AND T201IS_SYSTEM = 0
    ) LOOP
        v_sql := 'TRUNCATE TABLE ' || r.t201data_table || ' ;';
        DBMS_OUTPUT.PUT_LINE(v_sql);
        
        IF r.t201iq_data_table IS NOT NULL THEN
            v_sql := 'TRUNCATE TABLE ' || r.t201iq_data_table || ' ;';
            DBMS_OUTPUT.PUT_LINE(v_sql);
        END IF;
    END LOOP;
  END generate_truncate_statements_energy_bids_and_reserves_seconds;

  PROCEDURE generate_truncate_statements_prices_and_exchange_rates_seconds IS
    v_sql VARCHAR2(4000);
  BEGIN
    FOR r IN (
        SELECT t201data_table, t201iq_data_table
        FROM t201timeseries 
        WHERE t206entity IN (
            SELECT oid 
            FROM t206entity 
            WHERE get_full_code(OID) = '\SS_INPUT_DATA\PRICES_AND_RATES\PRICES_AND_EXCHANGE_RATES_SECOND'
        ) 
        AND t201data_table IS NOT NULL 
        AND T201IS_SYSTEM = 0
    ) LOOP
        v_sql := 'TRUNCATE TABLE ' || r.t201data_table || ' ;';
        DBMS_OUTPUT.PUT_LINE(v_sql);
        
        IF r.t201iq_data_table IS NOT NULL THEN
            v_sql := 'TRUNCATE TABLE ' || r.t201iq_data_table || ' ;';
            DBMS_OUTPUT.PUT_LINE(v_sql);
        END IF;
    END LOOP;
  END generate_truncate_statements_prices_and_exchange_rates_seconds;

  PROCEDURE generate_truncate_statements_activations IS
    v_sql VARCHAR2(4000);
  BEGIN
    FOR r IN (
        SELECT t201data_table, t201iq_data_table
        FROM t201timeseries 
        WHERE t206entity IN (
            SELECT oid 
            FROM t206entity 
            WHERE get_full_code(OID) = '\SS_INPUT_DATA\ACTIVATION\ACTIVATION'
        ) 
        AND t201data_table IS NOT NULL 
        AND T201IS_SYSTEM = 0
          AND T405TYPE = 'TS_PRIMARY'
          AND GET_FULL_CODE(OID) != '\SS_INPUT_DATA\ACTIVATION\ACTIVATION\TSO_SCHEDULE_MODIFICATION_RIR_START_UP_PRICE'
    ) LOOP
        v_sql := 'TRUNCATE TABLE ' || r.t201data_table || ' ;';
        DBMS_OUTPUT.PUT_LINE(v_sql);
        
        IF r.t201iq_data_table IS NOT NULL THEN
            v_sql := 'TRUNCATE TABLE ' || r.t201iq_data_table || ' ;';
            DBMS_OUTPUT.PUT_LINE(v_sql);
        END IF;
    END LOOP;
  END generate_truncate_statements_activations;

  PROCEDURE generate_truncate_statements_factor_data IS
    v_sql VARCHAR2(4000);
  BEGIN
    FOR r IN (
        SELECT t201data_table, t201iq_data_table
        FROM t201timeseries 
        WHERE t206entity IN (
            SELECT oid 
            FROM t206entity 
            WHERE get_full_code(OID) = '\SS_INPUT_DATA\FACTOR_DATA\FACTOR_DATA'
        ) 
        AND t201data_table IS NOT NULL 
        AND T201IS_SYSTEM = 0
        AND T405TYPE = 'TS_PRIMARY'
    ) LOOP
        v_sql := 'TRUNCATE TABLE ' || r.t201data_table || ' ;';
        DBMS_OUTPUT.PUT_LINE(v_sql);
        
        IF r.t201iq_data_table IS NOT NULL THEN
            v_sql := 'TRUNCATE TABLE ' || r.t201iq_data_table || ' ;';
            DBMS_OUTPUT.PUT_LINE(v_sql);
        END IF;
    END LOOP;
  END generate_truncate_statements_factor_data;

  PROCEDURE generate_truncate_statements_energy_bids_and_reserves IS
    v_sql VARCHAR2(4000);
  BEGIN
    FOR r IN (
        SELECT t201data_table, t201iq_data_table
        FROM t201timeseries 
        WHERE t206entity IN (
            SELECT oid 
            FROM t206entity 
            WHERE get_full_code(OID) = '\SS_INPUT_DATA\ENERGY_BIDS_AND_RESERVES\ENERGY_BID_AND_RESERVES'
        ) 
        AND t201data_table IS NOT NULL 
        AND T201IS_SYSTEM = 0
        AND T405TYPE = 'TS_PRIMARY'
    ) LOOP
        v_sql := 'TRUNCATE TABLE ' || r.t201data_table || ' ;';
        DBMS_OUTPUT.PUT_LINE(v_sql);
        
        IF r.t201iq_data_table IS NOT NULL THEN
            v_sql := 'TRUNCATE TABLE ' || r.t201iq_data_table || ' ;';
            DBMS_OUTPUT.PUT_LINE(v_sql);
        END IF;
    END LOOP;
  END generate_truncate_statements_energy_bids_and_reserves;

  PROCEDURE generate_truncate_statements_measurements IS
    v_sql VARCHAR2(4000);
  BEGIN
    FOR r IN (
        SELECT t201data_table, t201iq_data_table
        FROM t201timeseries 
        WHERE t206entity IN (
            SELECT oid 
            FROM t206entity 
            WHERE get_full_code(OID) = '\SS_INPUT_DATA\MEASUREMENTS\MEASUREMENTS'
        ) 
        AND t201data_table IS NOT NULL 
        AND T201IS_SYSTEM = 0
        AND T405TYPE = 'TS_PRIMARY'
    ) LOOP
        v_sql := 'TRUNCATE TABLE ' || r.t201data_table || ' ;';
        DBMS_OUTPUT.PUT_LINE(v_sql);
        
        IF r.t201iq_data_table IS NOT NULL THEN
            v_sql := 'TRUNCATE TABLE ' || r.t201iq_data_table || ' ;';
            DBMS_OUTPUT.PUT_LINE(v_sql);
        END IF;
    END LOOP;
  END generate_truncate_statements_measurements;

  PROCEDURE generate_truncate_statements_qualifications IS
    v_sql VARCHAR2(4000);
  BEGIN
    FOR r IN (
        SELECT t201data_table, t201iq_data_table
        FROM t201timeseries 
        WHERE t206entity IN (
            SELECT oid 
            FROM t206entity 
            WHERE get_full_code(OID) = '\SS_INPUT_DATA\QUALIFICATIONS\QUALIFICATIONS'
        ) 
        AND t201data_table IS NOT NULL 
        AND T201IS_SYSTEM = 0
        AND T405TYPE = 'TS_PRIMARY'
    ) LOOP
        v_sql := 'TRUNCATE TABLE ' || r.t201data_table || ' ;';
        DBMS_OUTPUT.PUT_LINE(v_sql);
        
        IF r.t201iq_data_table IS NOT NULL THEN
            v_sql := 'TRUNCATE TABLE ' || r.t201iq_data_table || ' ;';
            DBMS_OUTPUT.PUT_LINE(v_sql);
        END IF;
    END LOOP;
  END generate_truncate_statements_qualifications;

  PROCEDURE generate_truncate_statements_prices_and_exchanges IS
    v_sql VARCHAR2(4000);
  BEGIN
    FOR r IN (
        SELECT t201data_table, t201iq_data_table
        FROM t201timeseries 
        WHERE t206entity IN (
            SELECT oid 
            FROM t206entity 
            WHERE get_full_code(OID) = '\SS_INPUT_DATA\PRICES_AND_RATES\PRICES_AND_EXCHANGE_RATES'
        ) 
        AND t201data_table IS NOT NULL 
        AND T201IS_SYSTEM = 0
        AND T405TYPE = 'TS_PRIMARY'
    ) LOOP
        v_sql := 'TRUNCATE TABLE ' || r.t201data_table || ' ;';
        DBMS_OUTPUT.PUT_LINE(v_sql);
        
        IF r.t201iq_data_table IS NOT NULL THEN
            v_sql := 'TRUNCATE TABLE ' || r.t201iq_data_table || ' ;';
            DBMS_OUTPUT.PUT_LINE(v_sql);
        END IF;
    END LOOP;
  END generate_truncate_statements_prices_and_exchanges;

  PROCEDURE generate_truncate_statements_schedules IS
    v_sql VARCHAR2(4000);
  BEGIN
    FOR r IN (
        SELECT t201data_table, t201iq_data_table
        FROM t201timeseries 
        WHERE t206entity IN (
            SELECT oid 
            FROM t206entity 
            WHERE get_full_code(OID) = '\SS_INPUT_DATA\SCHEDULES\SCHEDULES'
        ) 
        AND t201data_table IS NOT NULL 
        AND T201IS_SYSTEM = 0
        AND T405TYPE = 'TS_PRIMARY'
    ) LOOP
        v_sql := 'TRUNCATE TABLE ' || r.t201data_table || ' ;';
        DBMS_OUTPUT.PUT_LINE(v_sql);
        
        IF r.t201iq_data_table IS NOT NULL THEN
            v_sql := 'TRUNCATE TABLE ' || r.t201iq_data_table || ' ;';
            DBMS_OUTPUT.PUT_LINE(v_sql);
        END IF;
    END LOOP;
  END generate_truncate_statements_schedules;

  PROCEDURE generate_truncate_statements_operational_state IS
    v_sql VARCHAR2(4000);
  BEGIN
    FOR r IN (
        SELECT t201data_table, t201iq_data_table
        FROM t201timeseries 
        WHERE t206entity IN (
            SELECT oid 
            FROM t206entity 
            WHERE get_full_code(OID) = '\SS_INPUT_DATA\OPERATIONAL_STATE\OPERATIONAL_STATE'
        ) 
        AND t201data_table IS NOT NULL 
        AND T201IS_SYSTEM = 0
    ) LOOP
        v_sql := 'TRUNCATE TABLE ' || r.t201data_table || ' ;';
        DBMS_OUTPUT.PUT_LINE(v_sql);
        
        IF r.t201iq_data_table IS NOT NULL THEN
            v_sql := 'TRUNCATE TABLE ' || r.t201iq_data_table || ' ;';
            DBMS_OUTPUT.PUT_LINE(v_sql);
        END IF;
    END LOOP;
  END generate_truncate_statements_operational_state;

  PROCEDURE generate_truncate_statements_availability_daily IS
    v_sql VARCHAR2(4000);
  BEGIN
    FOR r IN (
        SELECT t201data_table, t201iq_data_table
        FROM t201timeseries 
        WHERE t206entity IN (
            SELECT oid 
            FROM t206entity 
            WHERE get_full_code(OID) LIKE '%\MONITORING_AND_CONTROL\AVAILABILITY\DAILY_AVAILABILITY_WORKFLOW%'
        ) 
        AND t201data_table IS NOT NULL 
        AND T201IS_SYSTEM = 0
    ) LOOP
        v_sql := 'TRUNCATE TABLE ' || r.t201data_table || ' ;';
        DBMS_OUTPUT.PUT_LINE(v_sql);
        
        IF r.t201iq_data_table IS NOT NULL THEN
            v_sql := 'TRUNCATE TABLE ' || r.t201iq_data_table || ' ;';
            DBMS_OUTPUT.PUT_LINE(v_sql);
        END IF;
    END LOOP;
  END generate_truncate_statements_availability_daily;

  PROCEDURE generate_truncate_statements_control_energy_daily IS
    v_sql VARCHAR2(4000);
  BEGIN
    FOR r IN (
        SELECT t201data_table, t201iq_data_table
        FROM t201timeseries 
        WHERE t206entity IN (
            SELECT oid 
            FROM t206entity 
            WHERE get_full_code(OID) LIKE '%\MONITORING_AND_CONTROL\CONTROL_ENERGY\DAILY_CONTROL_ENERGY_WORKFLOW%'
        ) 
        AND t201data_table IS NOT NULL 
        AND T201IS_SYSTEM = 0
    ) LOOP
        v_sql := 'TRUNCATE TABLE ' || r.t201data_table || ' ;';
        DBMS_OUTPUT.PUT_LINE(v_sql);
        
        IF r.t201iq_data_table IS NOT NULL THEN
            v_sql := 'TRUNCATE TABLE ' || r.t201iq_data_table || ' ;';
            DBMS_OUTPUT.PUT_LINE(v_sql);
        END IF;
    END LOOP;
  END generate_truncate_statements_control_energy_daily;

  PROCEDURE generate_truncate_statements_settlement_daily IS
    v_sql VARCHAR2(4000);
  BEGIN
    FOR r IN (
        SELECT t201data_table, t201iq_data_table
        FROM t201timeseries 
        WHERE t206entity IN (
            SELECT oid 
            FROM t206entity 
            WHERE get_full_code(OID) LIKE '%\MONITORING_AND_CONTROL\CONTROL_ENERGY\PREPARATION_SETTLEMENT_WORKFLOW%'
        ) 
        AND t201data_table IS NOT NULL 
        AND T201IS_SYSTEM = 0
    ) LOOP
        v_sql := 'TRUNCATE TABLE ' || r.t201data_table || ' ;';
        DBMS_OUTPUT.PUT_LINE(v_sql);
        
        IF r.t201iq_data_table IS NOT NULL THEN
            v_sql := 'TRUNCATE TABLE ' || r.t201iq_data_table || ' ;';
            DBMS_OUTPUT.PUT_LINE(v_sql);
        END IF;
    END LOOP;
  END generate_truncate_statements_settlement_daily;

  PROCEDURE generate_truncate_statements_settlement_afrr_daily IS
    v_sql VARCHAR2(4000);
  BEGIN
    FOR r IN (
        SELECT t201data_table, t201iq_data_table
        FROM t201timeseries
        WHERE t206entity IN (
            SELECT oid
            FROM t206entity
            WHERE get_full_code(OID) LIKE '%\MONITORING_AND_CONTROL\CONTROL_ENERGY\PUBLICATION_SETTLEMENT_AFRR_WORKFLOW%'
        )
        AND t201data_table IS NOT NULL
        AND T201IS_SYSTEM = 0
    ) LOOP
        v_sql := 'TRUNCATE TABLE ' || r.t201data_table || ' ;';
        DBMS_OUTPUT.PUT_LINE(v_sql);
        
        IF r.t201iq_data_table IS NOT NULL THEN
            v_sql := 'TRUNCATE TABLE ' || r.t201iq_data_table || ' ;';
            DBMS_OUTPUT.PUT_LINE(v_sql);
        END IF;
    END LOOP;
  END generate_truncate_statements_settlement_afrr_daily;

  PROCEDURE generate_truncate_statements_settlement_balancing_energy_bids_daily IS
    v_sql VARCHAR2(4000);
  BEGIN
    FOR r IN (
        SELECT t201data_table, t201iq_data_table
        FROM t201timeseries
        WHERE t206entity IN (
            SELECT oid
            FROM t206entity
            WHERE get_full_code(OID) LIKE '%\MONITORING_AND_CONTROL\CONTROL_ENERGY\PUBLICATION_SETTLEMENT_BALANCING_ENERGY_BIDS_WORKFLOW%'
        )
        AND t201data_table IS NOT NULL
        AND T201IS_SYSTEM = 0
    ) LOOP
        v_sql := 'TRUNCATE TABLE ' || r.t201data_table || ' ;';
        DBMS_OUTPUT.PUT_LINE(v_sql);
        
        IF r.t201iq_data_table IS NOT NULL THEN
            v_sql := 'TRUNCATE TABLE ' || r.t201iq_data_table || ' ;';
            DBMS_OUTPUT.PUT_LINE(v_sql);
        END IF;
    END LOOP;
  END generate_truncate_statements_settlement_balancing_energy_bids_daily;

  PROCEDURE generate_truncate_statements_settlement_mfrr_daily IS
    v_sql VARCHAR2(4000);
  BEGIN
    FOR r IN (
        SELECT t201data_table, t201iq_data_table
        FROM t201timeseries
        WHERE t206entity IN (
            SELECT oid
            FROM t206entity
            WHERE get_full_code(OID) LIKE '%\MONITORING_AND_CONTROL\CONTROL_ENERGY\PUBLICATION_SETTLEMENT_MFRR_WORKFLOW%'
        )
        AND t201data_table IS NOT NULL
        AND T201IS_SYSTEM = 0
    ) LOOP
        v_sql := 'TRUNCATE TABLE ' || r.t201data_table || ' ;';
        DBMS_OUTPUT.PUT_LINE(v_sql);
        
        IF r.t201iq_data_table IS NOT NULL THEN
            v_sql := 'TRUNCATE TABLE ' || r.t201iq_data_table || ' ;';
            DBMS_OUTPUT.PUT_LINE(v_sql);
        END IF;
    END LOOP;
  END generate_truncate_statements_settlement_mfrr_daily;

  PROCEDURE generate_truncate_statements_tso_tso_daily IS
    v_sql VARCHAR2(4000);
  BEGIN
    FOR r IN (
        SELECT t201data_table, t201iq_data_table
        FROM t201timeseries 
        WHERE t206entity IN (
            SELECT oid 
            FROM t206entity 
            WHERE get_full_code(OID) LIKE '%\MONITORING_AND_CONTROL\TSO_TSO\DAILY_TSO_TSO_WORKFLOW%'
        ) 
        AND t201data_table IS NOT NULL 
        AND T201IS_SYSTEM = 0
    ) LOOP
        v_sql := 'TRUNCATE TABLE ' || r.t201data_table || ' ;';
        DBMS_OUTPUT.PUT_LINE(v_sql);
        
        IF r.t201iq_data_table IS NOT NULL THEN
            v_sql := 'TRUNCATE TABLE ' || r.t201iq_data_table || ' ;';
            DBMS_OUTPUT.PUT_LINE(v_sql);
        END IF;
    END LOOP;
  END generate_truncate_statements_tso_tso_daily;

  PROCEDURE generate_truncate_statements_afrr_balancing_capacity_daily IS
    v_sql VARCHAR2(4000);
  BEGIN
    FOR r IN (
        SELECT t201data_table, t201iq_data_table
        FROM t201timeseries 
        WHERE t206entity IN (
            SELECT oid 
            FROM t206entity 
            WHERE get_full_code(OID) LIKE '%\SS_AVAILABILITY\AFRR_BALANCING_CAPACITY\DAILY_AFRR_BALANCING_CAPACITY%'
        ) 
        AND t201data_table IS NOT NULL 
        AND T201IS_SYSTEM = 0
    ) LOOP
        v_sql := 'TRUNCATE TABLE ' || r.t201data_table || ' ;';
        DBMS_OUTPUT.PUT_LINE(v_sql);
        
        IF r.t201iq_data_table IS NOT NULL THEN
            v_sql := 'TRUNCATE TABLE ' || r.t201iq_data_table || ' ;';
            DBMS_OUTPUT.PUT_LINE(v_sql);
        END IF;
    END LOOP;
  END generate_truncate_statements_afrr_balancing_capacity_daily;

  PROCEDURE generate_truncate_statements_mfrr_balancing_capacity_daily IS
    v_sql VARCHAR2(4000);
  BEGIN
    FOR r IN (
        SELECT t201data_table, t201iq_data_table
        FROM t201timeseries 
        WHERE t206entity IN (
            SELECT oid 
            FROM t206entity 
            WHERE get_full_code(OID) LIKE '%\SS_AVAILABILITY\MFRR_BALANCING_CAPACITY\DAILY_MFRR_BALANCING_CAPACITY%'
        ) 
        AND t201data_table IS NOT NULL 
        AND T201IS_SYSTEM = 0
    ) LOOP
        v_sql := 'TRUNCATE TABLE ' || r.t201data_table || ' ;';
        DBMS_OUTPUT.PUT_LINE(v_sql);
        
        IF r.t201iq_data_table IS NOT NULL THEN
            v_sql := 'TRUNCATE TABLE ' || r.t201iq_data_table || ' ;';
            DBMS_OUTPUT.PUT_LINE(v_sql);
        END IF;
    END LOOP;
  END generate_truncate_statements_mfrr_balancing_capacity_daily;

  PROCEDURE generate_truncate_statements_providing_international_assistance_daily IS
    v_sql VARCHAR2(4000);
  BEGIN
    FOR r IN (
        SELECT t201data_table, t201iq_data_table
        FROM t201timeseries 
        WHERE t206entity IN (
            SELECT oid 
            FROM t206entity 
            WHERE get_full_code(OID) LIKE '%\SS_CONTROL_ENERGY\INTERNATIONAL_ASSISTANCE\DAILY_PROVIDING_INTERNATIONAL_ASSISTENCE%'
        ) 
        AND t201data_table IS NOT NULL 
        AND T201IS_SYSTEM = 0
    ) LOOP
        v_sql := 'TRUNCATE TABLE ' || r.t201data_table || ' ;';
        DBMS_OUTPUT.PUT_LINE(v_sql);
        
        IF r.t201iq_data_table IS NOT NULL THEN
            v_sql := 'TRUNCATE TABLE ' || r.t201iq_data_table || ' ;';
            DBMS_OUTPUT.PUT_LINE(v_sql);
        END IF;
    END LOOP;
  END generate_truncate_statements_providing_international_assistance_daily;

  PROCEDURE generate_truncate_statements_using_international_assistance_daily IS
    v_sql VARCHAR2(4000);
  BEGIN
    FOR r IN (
        SELECT t201data_table, t201iq_data_table
        FROM t201timeseries 
        WHERE t206entity IN (
            SELECT oid 
            FROM t206entity 
            WHERE get_full_code(OID) LIKE '%\SS_CONTROL_ENERGY\INTERNATIONAL_ASSISTANCE\DAILY_USING_INTERNATIONAL_ASSISTENCE%'
        ) 
        AND t201data_table IS NOT NULL 
        AND T201IS_SYSTEM = 0
    ) LOOP
        v_sql := 'TRUNCATE TABLE ' || r.t201data_table || ' ;';
        DBMS_OUTPUT.PUT_LINE(v_sql);
        
        IF r.t201iq_data_table IS NOT NULL THEN
            v_sql := 'TRUNCATE TABLE ' || r.t201iq_data_table || ' ;';
            DBMS_OUTPUT.PUT_LINE(v_sql);
        END IF;
    END LOOP;
  END generate_truncate_statements_using_international_assistance_daily;

  PROCEDURE generate_truncate_statements_tso_schedule_modification_rir_daily IS
    v_sql VARCHAR2(4000);
  BEGIN
    FOR r IN (
        SELECT t201data_table, t201iq_data_table
        FROM t201timeseries 
        WHERE t206entity IN (
            SELECT oid 
            FROM t206entity 
            WHERE get_full_code(OID) LIKE '%\SS_CONTROL_ENERGY\TSO_SCHEDULE_MODIFICATION_RIR\DAILY_TSO_SCHEDULE_MODIFICATION_RIR%'
        ) 
        AND t201data_table IS NOT NULL 
        AND T201IS_SYSTEM = 0
    ) LOOP
        v_sql := 'TRUNCATE TABLE ' || r.t201data_table || ' ;';
        DBMS_OUTPUT.PUT_LINE(v_sql);
        
        IF r.t201iq_data_table IS NOT NULL THEN
            v_sql := 'TRUNCATE TABLE ' || r.t201iq_data_table || ' ;';
            DBMS_OUTPUT.PUT_LINE(v_sql);
        END IF;
    END LOOP;
  END generate_truncate_statements_tso_schedule_modification_rir_daily;

  PROCEDURE generate_truncate_statements_providing_igcc_basic_data_daily IS
    v_sql VARCHAR2(4000);
  BEGIN
    FOR r IN (
        SELECT t201data_table, t201iq_data_table
        FROM t201timeseries
        WHERE t206entity IN (
            SELECT oid
            FROM t206entity
            WHERE get_full_code(OID) LIKE '%\SS_TSO_TSO\PROVIDING_IGCC_BASIC_DATA\DAILY_PROVIDING_IGCC_BASIC_DATA%'
        )
        AND t201data_table IS NOT NULL
        AND T201IS_SYSTEM = 0
    ) LOOP
        v_sql := 'TRUNCATE TABLE ' || r.t201data_table || ' ;';
        DBMS_OUTPUT.PUT_LINE(v_sql);
        
        IF r.t201iq_data_table IS NOT NULL THEN
            v_sql := 'TRUNCATE TABLE ' || r.t201iq_data_table || ' ;';
            DBMS_OUTPUT.PUT_LINE(v_sql);
        END IF;
    END LOOP;
  END generate_truncate_statements_providing_igcc_basic_data_daily;

  PROCEDURE generate_truncate_statements_providing_multilateral_remedial_action_basic_data_daily IS
    v_sql VARCHAR2(4000);
  BEGIN
    FOR r IN (
        SELECT t201data_table, t201iq_data_table
        FROM t201timeseries
        WHERE t206entity IN (
            SELECT oid
            FROM t206entity
            WHERE get_full_code(OID) LIKE '%\SS_TSO_TSO\PROVIDING_MULTILATERAL_REMEDIAL_ACTION_BASIC_DATA\DAILY_PROVIDING_MULTILATERAL_REMEDIAL_ACTION_BASIC_DATA%'
        )
        AND t201data_table IS NOT NULL
        AND T201IS_SYSTEM = 0
    ) LOOP
        v_sql := 'TRUNCATE TABLE ' || r.t201data_table || ' ;';
        DBMS_OUTPUT.PUT_LINE(v_sql);
        
        IF r.t201iq_data_table IS NOT NULL THEN
            v_sql := 'TRUNCATE TABLE ' || r.t201iq_data_table || ' ;';
            DBMS_OUTPUT.PUT_LINE(v_sql);
        END IF;
    END LOOP;
  END generate_truncate_statements_providing_multilateral_remedial_action_basic_data_daily;

  PROCEDURE generate_truncate_statements_availability_monthly IS
    v_sql VARCHAR2(4000);
  BEGIN
    FOR r IN (
        SELECT t201data_table, t201iq_data_table
        FROM t201timeseries 
        WHERE t206entity IN (
            SELECT oid 
            FROM t206entity 
            WHERE get_full_code(OID) LIKE '%\MONITORING_AND_CONTROL\AVAILABILITY\MONTHLY_AVAILABILITY_WORKFLOW%'
        ) 
        AND t201data_table IS NOT NULL 
        AND T201IS_SYSTEM = 0
    ) LOOP
        v_sql := 'TRUNCATE TABLE ' || r.t201data_table || ' ;';
        DBMS_OUTPUT.PUT_LINE(v_sql);
        
        IF r.t201iq_data_table IS NOT NULL THEN
            v_sql := 'TRUNCATE TABLE ' || r.t201iq_data_table || ' ;';
            DBMS_OUTPUT.PUT_LINE(v_sql);
        END IF;
    END LOOP;
  END generate_truncate_statements_availability_monthly;

  PROCEDURE generate_truncate_statements_control_energy_monthly IS
    v_sql VARCHAR2(4000);
  BEGIN
    FOR r IN (
        SELECT t201data_table, t201iq_data_table
        FROM t201timeseries 
        WHERE t206entity IN (
            SELECT oid 
            FROM t206entity 
            WHERE get_full_code(OID) LIKE '%\MONITORING_AND_CONTROL\CONTROL_ENERGY\MONTHLY_CONTROL_ENERGY_WORKFLOW%'
        ) 
        AND t201data_table IS NOT NULL 
        AND T201IS_SYSTEM = 0
    ) LOOP
        v_sql := 'TRUNCATE TABLE ' || r.t201data_table || ' ;';
        DBMS_OUTPUT.PUT_LINE(v_sql);
        
        IF r.t201iq_data_table IS NOT NULL THEN
            v_sql := 'TRUNCATE TABLE ' || r.t201iq_data_table || ' ;';
            DBMS_OUTPUT.PUT_LINE(v_sql);
        END IF;
    END LOOP;
  END generate_truncate_statements_control_energy_monthly;

  PROCEDURE generate_truncate_statements_afrr_balancing_capacity_monthly IS
    v_sql VARCHAR2(4000);
  BEGIN
    FOR r IN (
        SELECT t201data_table, t201iq_data_table
        FROM t201timeseries
        WHERE t206entity IN (
            SELECT oid
            FROM t206entity
            WHERE get_full_code(OID) LIKE '%\SS_AVAILABILITY\AFRR_BALANCING_CAPACITY\MONTHLY_AFRR_BALANCING_CAPACITY%'
        )
        AND t201data_table IS NOT NULL
        AND T201IS_SYSTEM = 0
    ) LOOP
        v_sql := 'TRUNCATE TABLE ' || r.t201data_table || ' ;';
        DBMS_OUTPUT.PUT_LINE(v_sql);
        
        IF r.t201iq_data_table IS NOT NULL THEN
            v_sql := 'TRUNCATE TABLE ' || r.t201iq_data_table || ' ;';
            DBMS_OUTPUT.PUT_LINE(v_sql);
        END IF;
    END LOOP;
  END generate_truncate_statements_afrr_balancing_capacity_monthly;

  PROCEDURE generate_truncate_statements_fcr_balancing_capacity_monthly IS
    v_sql VARCHAR2(4000);
  BEGIN
    FOR r IN (
        SELECT t201data_table, t201iq_data_table
        FROM t201timeseries
        WHERE t206entity IN (
            SELECT oid
            FROM t206entity
            WHERE get_full_code(OID) LIKE '%\SS_AVAILABILITY\FCR_BALANCING_CAPACITY\MONTHLY_FCR_BALANCING_CAPACITY%'
        )
        AND t201data_table IS NOT NULL
        AND T201IS_SYSTEM = 0
    ) LOOP
        v_sql := 'TRUNCATE TABLE ' || r.t201data_table || ' ;';
        DBMS_OUTPUT.PUT_LINE(v_sql);
        
        IF r.t201iq_data_table IS NOT NULL THEN
            v_sql := 'TRUNCATE TABLE ' || r.t201iq_data_table || ' ;';
            DBMS_OUTPUT.PUT_LINE(v_sql);
        END IF;
    END LOOP;
  END generate_truncate_statements_fcr_balancing_capacity_monthly;

  PROCEDURE generate_truncate_statements_mfrr_balancing_capacity_monthly IS
    v_sql VARCHAR2(4000);
  BEGIN
    FOR r IN (
        SELECT t201data_table, t201iq_data_table
        FROM t201timeseries
        WHERE t206entity IN (
            SELECT oid
            FROM t206entity
            WHERE get_full_code(OID) LIKE '%\SS_AVAILABILITY\MFRR_BALANCING_CAPACITY\MONTHLY_MFRR_BALANCING_CAPACITY%'
        )
        AND t201data_table IS NOT NULL
        AND T201IS_SYSTEM = 0
    ) LOOP
        v_sql := 'TRUNCATE TABLE ' || r.t201data_table || ' ;';
        DBMS_OUTPUT.PUT_LINE(v_sql);
        
        IF r.t201iq_data_table IS NOT NULL THEN
            v_sql := 'TRUNCATE TABLE ' || r.t201iq_data_table || ' ;';
            DBMS_OUTPUT.PUT_LINE(v_sql);
        END IF;
    END LOOP;
  END generate_truncate_statements_mfrr_balancing_capacity_monthly;

  PROCEDURE generate_truncate_statements_u_q_control_reactive_power_monthly IS
    v_sql VARCHAR2(4000);
  BEGIN
    FOR r IN (
        SELECT t201data_table, t201iq_data_table
        FROM t201timeseries
        WHERE t206entity IN (
            SELECT oid
            FROM t206entity
            WHERE get_full_code(OID) LIKE '%\SS_AVAILABILITY\U_Q_CONTROL_REACTIVE_POWER\U_Q_CONTROL_REACTIVE_POWER%'
        )
        AND t201data_table IS NOT NULL
        AND T201IS_SYSTEM = 0
    ) LOOP
        v_sql := 'TRUNCATE TABLE ' || r.t201data_table || ' ;';
        DBMS_OUTPUT.PUT_LINE(v_sql);
        
        IF r.t201iq_data_table IS NOT NULL THEN
            v_sql := 'TRUNCATE TABLE ' || r.t201iq_data_table || ' ;';
            DBMS_OUTPUT.PUT_LINE(v_sql);
        END IF;
    END LOOP;
  END generate_truncate_statements_u_q_control_reactive_power_monthly;

  PROCEDURE generate_truncate_statements_providing_international_assistance_monthly IS
    v_sql VARCHAR2(4000);
  BEGIN
    FOR r IN (
        SELECT t201data_table, t201iq_data_table
        FROM t201timeseries
        WHERE t206entity IN (
            SELECT oid
            FROM t206entity
            WHERE get_full_code(OID) LIKE '%\SS_CONTROL_ENERGY\INTERNATIONAL_ASSISTANCE\MONTHLY_PROVIDING_INTERNATIONAL_ASSISTANCE%'
        )
        AND t201data_table IS NOT NULL
        AND T201IS_SYSTEM = 0
    ) LOOP
        v_sql := 'TRUNCATE TABLE ' || r.t201data_table || ' ;';
        DBMS_OUTPUT.PUT_LINE(v_sql);
        
        IF r.t201iq_data_table IS NOT NULL THEN
            v_sql := 'TRUNCATE TABLE ' || r.t201iq_data_table || ' ;';
            DBMS_OUTPUT.PUT_LINE(v_sql);
        END IF;
    END LOOP;
  END generate_truncate_statements_providing_international_assistance_monthly;

  PROCEDURE generate_truncate_statements_using_international_assistance_monthly IS
    v_sql VARCHAR2(4000);
  BEGIN
    FOR r IN (
        SELECT t201data_table, t201iq_data_table
        FROM t201timeseries
        WHERE t206entity IN (
            SELECT oid
            FROM t206entity
            WHERE get_full_code(OID) LIKE '%\SS_CONTROL_ENERGY\INTERNATIONAL_ASSISTANCE\MONTHLY_USING_INTERNATIONAL_ASSISTANCE%'
        )
        AND t201data_table IS NOT NULL
        AND T201IS_SYSTEM = 0
    ) LOOP
        v_sql := 'TRUNCATE TABLE ' || r.t201data_table || ' ;';
        DBMS_OUTPUT.PUT_LINE(v_sql);
        
        IF r.t201iq_data_table IS NOT NULL THEN
            v_sql := 'TRUNCATE TABLE ' || r.t201iq_data_table || ' ;';
            DBMS_OUTPUT.PUT_LINE(v_sql);
        END IF;
    END LOOP;
  END generate_truncate_statements_using_international_assistance_monthly;

  PROCEDURE generate_truncate_statements_afrr_monthly IS
    v_sql VARCHAR2(4000);
  BEGIN
    FOR r IN (
        SELECT t201data_table, t201iq_data_table
        FROM t201timeseries
        WHERE t206entity IN (
            SELECT oid
            FROM t206entity
            WHERE get_full_code(OID) LIKE '%\SS_CONTROL_ENERGY\AFRR\MONTHLY_AFRR%'
        )
        AND t201data_table IS NOT NULL
        AND T201IS_SYSTEM = 0
    ) LOOP
        v_sql := 'TRUNCATE TABLE ' || r.t201data_table || ' ;';
        DBMS_OUTPUT.PUT_LINE(v_sql);
        
        IF r.t201iq_data_table IS NOT NULL THEN
            v_sql := 'TRUNCATE TABLE ' || r.t201iq_data_table || ' ;';
            DBMS_OUTPUT.PUT_LINE(v_sql);
        END IF;
    END LOOP;
  END generate_truncate_statements_afrr_monthly;

  PROCEDURE generate_truncate_statements_tso_schedule_modification_rir_monthly IS
    v_sql VARCHAR2(4000);
  BEGIN
    FOR r IN (
        SELECT t201data_table, t201iq_data_table
        FROM t201timeseries
        WHERE t206entity IN (
            SELECT oid
            FROM t206entity
            WHERE get_full_code(OID) LIKE '%\SS_CONTROL_ENERGY\TSO_SCHEDULE_MODIFICATION_RIR\MONTHLY_TSO_SCHEDULE_MODIFICATION_RIR%'
        )
        AND t201data_table IS NOT NULL
        AND T201IS_SYSTEM = 0
    ) LOOP
        v_sql := 'TRUNCATE TABLE ' || r.t201data_table || ' ;';
        DBMS_OUTPUT.PUT_LINE(v_sql);
        
        IF r.t201iq_data_table IS NOT NULL THEN
            v_sql := 'TRUNCATE TABLE ' || r.t201iq_data_table || ' ;';
            DBMS_OUTPUT.PUT_LINE(v_sql);
        END IF;
    END LOOP;
  END generate_truncate_statements_tso_schedule_modification_rir_monthly;

  PROCEDURE generate_truncate_statements_providing_multilateral_remedial_action_basic_data_monthly IS
    v_sql VARCHAR2(4000);
  BEGIN
    FOR r IN (
        SELECT t201data_table, t201iq_data_table
        FROM t201timeseries
        WHERE t206entity IN (
            SELECT oid
            FROM t206entity
            WHERE get_full_code(OID) LIKE '%\SS_TSO_TSO\PROVIDING_MULTILATERAL_REMEDIAL_ACTION_BASIC_DATA\MONTHLY_PROVIDING_MULTILATERAL_REMEDIAL_ACTION_BASIC_DATA%'
        )
        AND t201data_table IS NOT NULL
        AND T201IS_SYSTEM = 0
    ) LOOP
        v_sql := 'TRUNCATE TABLE ' || r.t201data_table || ' ;';
        DBMS_OUTPUT.PUT_LINE(v_sql);
        
        IF r.t201iq_data_table IS NOT NULL THEN
            v_sql := 'TRUNCATE TABLE ' || r.t201iq_data_table || ' ;';
            DBMS_OUTPUT.PUT_LINE(v_sql);
        END IF;
    END LOOP;
  END generate_truncate_statements_providing_multilateral_remedial_action_basic_data_monthly;

  PROCEDURE generate_truncate_statements_black_start_service_monthly IS
    v_sql VARCHAR2(4000);
  BEGIN
    FOR r IN (
        SELECT t201data_table, t201iq_data_table
        FROM t201timeseries
        WHERE t206entity IN (
            SELECT oid
            FROM t206entity
            WHERE get_full_code(OID) LIKE '%\SS_AVAILABILITY\BLACK_START_SERVICE\BLACK_START_SERVICE%'
        )
        AND t201data_table IS NOT NULL
        AND T201IS_SYSTEM = 0
    ) LOOP
        v_sql := 'TRUNCATE TABLE ' || r.t201data_table || ' ;';
        DBMS_OUTPUT.PUT_LINE(v_sql);
        
        IF r.t201iq_data_table IS NOT NULL THEN
            v_sql := 'TRUNCATE TABLE ' || r.t201iq_data_table || ' ;';
            DBMS_OUTPUT.PUT_LINE(v_sql);
        END IF;
    END LOOP;
  END generate_truncate_statements_black_start_service_monthly;

  PROCEDURE generate_truncate_statements_measurements_monthly IS
    v_sql VARCHAR2(4000);
  BEGIN
    FOR r IN (
        SELECT t201data_table, t201iq_data_table
        FROM t201timeseries
        WHERE t206entity IN (
            SELECT oid
            FROM t206entity
            WHERE get_full_code(OID) LIKE '%\SS_INPUT_DATA\MEASUREMENTS\MEASUREMENTS%'
        )
        AND t201data_table IS NOT NULL
        AND T201IS_SYSTEM = 0
    ) LOOP
        v_sql := 'TRUNCATE TABLE ' || r.t201data_table || ' ;';
        DBMS_OUTPUT.PUT_LINE(v_sql);
        
        IF r.t201iq_data_table IS NOT NULL THEN
            v_sql := 'TRUNCATE TABLE ' || r.t201iq_data_table || ' ;';
            DBMS_OUTPUT.PUT_LINE(v_sql);
        END IF;
    END LOOP;
  END generate_truncate_statements_measurements_monthly;

  PROCEDURE generate_truncate_statements_mfrr_monthly IS
    v_sql VARCHAR2(4000);
  BEGIN
    FOR r IN (
        SELECT t201data_table, t201iq_data_table
        FROM t201timeseries
        WHERE t206entity IN (
            SELECT oid
            FROM t206entity
            WHERE get_full_code(OID) LIKE '%\SS_CONTROL_ENERGY\MFRR\MONTHLY_MFRR%'
        )
        AND t201data_table IS NOT NULL
        AND T201IS_SYSTEM = 0
    ) LOOP
        v_sql := 'TRUNCATE TABLE ' || r.t201data_table || ' ;';
        DBMS_OUTPUT.PUT_LINE(v_sql);
        
        IF r.t201iq_data_table IS NOT NULL THEN
            v_sql := 'TRUNCATE TABLE ' || r.t201iq_data_table || ' ;';
            DBMS_OUTPUT.PUT_LINE(v_sql);
        END IF;
    END LOOP;
  END generate_truncate_statements_mfrr_monthly;

  PROCEDURE generate_truncate_statements_fcr_balancing_capacity_hourly IS
    v_sql VARCHAR2(4000);
  BEGIN
    FOR r IN (
        SELECT t201data_table, t201iq_data_table
        FROM t201timeseries
        WHERE t206entity IN (
            SELECT oid
            FROM t206entity
            WHERE get_full_code(OID) LIKE '%\SS_AVAILABILITY\FCR_BALANCING_CAPACITY\HOURLY_FCR_BALANCING_CAPACITY%'
        )
        AND t201data_table IS NOT NULL
        AND T201IS_SYSTEM = 0
    ) LOOP
        v_sql := 'TRUNCATE TABLE ' || r.t201data_table || ' ;';
        DBMS_OUTPUT.PUT_LINE(v_sql);
        
        IF r.t201iq_data_table IS NOT NULL THEN
            v_sql := 'TRUNCATE TABLE ' || r.t201iq_data_table || ' ;';
            DBMS_OUTPUT.PUT_LINE(v_sql);
        END IF;
    END LOOP;
  END generate_truncate_statements_fcr_balancing_capacity_hourly;

  PROCEDURE generate_truncate_statements_schedules_qh IS
    v_sql VARCHAR2(4000);
  BEGIN
    FOR r IN (
        SELECT t201data_table, t201iq_data_table
        FROM t201timeseries
        WHERE t206entity IN (
            SELECT oid
            FROM t206entity
            WHERE get_full_code(OID) LIKE '%\SS_INPUT_DATA\SCHEDULES\SCHEDULES%'
        )
        AND t201data_table IS NOT NULL
        AND T201IS_SYSTEM = 0
    ) LOOP
        v_sql := 'TRUNCATE TABLE ' || r.t201data_table || ' ;';
        DBMS_OUTPUT.PUT_LINE(v_sql);
        
        IF r.t201iq_data_table IS NOT NULL THEN
            v_sql := 'TRUNCATE TABLE ' || r.t201iq_data_table || ' ;';
            DBMS_OUTPUT.PUT_LINE(v_sql);
        END IF;
    END LOOP;
  END generate_truncate_statements_schedules_qh;

  PROCEDURE generate_truncate_statements_spectrum_data_qh IS
    v_sql VARCHAR2(4000);
  BEGIN
    FOR r IN (
        SELECT t201data_table, t201iq_data_table
        FROM t201timeseries
        WHERE t206entity IN (
            SELECT oid
            FROM t206entity
            WHERE get_full_code(OID) LIKE '%\SS_INPUT_DATA\SPECTRUM\SPECTRUM_DATA%'
        )
        AND t201data_table IS NOT NULL
        AND T201IS_SYSTEM = 0
    ) LOOP
        v_sql := 'TRUNCATE TABLE ' || r.t201data_table || ' ;';
        DBMS_OUTPUT.PUT_LINE(v_sql);
        
        IF r.t201iq_data_table IS NOT NULL THEN
            v_sql := 'TRUNCATE TABLE ' || r.t201iq_data_table || ' ;';
            DBMS_OUTPUT.PUT_LINE(v_sql);
        END IF;
    END LOOP;
  END generate_truncate_statements_spectrum_data_qh;

  PROCEDURE generate_truncate_statements_spectrum_data_seconds_qh IS
    v_sql VARCHAR2(4000);
  BEGIN
    FOR r IN (
        SELECT t201data_table, t201iq_data_table
        FROM t201timeseries
        WHERE t206entity IN (
            SELECT oid
            FROM t206entity
            WHERE get_full_code(OID) LIKE '%\SS_INPUT_DATA\SPECTRUM\SPECTRUM_DATA_SECOND%'
        )
        AND t201data_table IS NOT NULL
        AND T201IS_SYSTEM = 0
    ) LOOP
        v_sql := 'TRUNCATE TABLE ' || r.t201data_table || ' ;';
        DBMS_OUTPUT.PUT_LINE(v_sql);
        
        IF r.t201iq_data_table IS NOT NULL THEN
            v_sql := 'TRUNCATE TABLE ' || r.t201iq_data_table || ' ;';
            DBMS_OUTPUT.PUT_LINE(v_sql);
        END IF;
    END LOOP;
  END generate_truncate_statements_spectrum_data_seconds_qh;

  PROCEDURE generate_truncate_statements_prices_and_exchange_rates_seconds_qh IS
    v_sql VARCHAR2(4000);
  BEGIN
    FOR r IN (
        SELECT t201data_table, t201iq_data_table
        FROM t201timeseries
        WHERE t206entity IN (
            SELECT oid
            FROM t206entity
            WHERE get_full_code(OID) LIKE '%\SS_INPUT_DATA\PRICES_AND_RATES\PRICES_AND_EXCHANGE_RATES_SECOND%'
        )
        AND t201data_table IS NOT NULL
        AND T201IS_SYSTEM = 0
    ) LOOP
        v_sql := 'TRUNCATE TABLE ' || r.t201data_table || ' ;';
        DBMS_OUTPUT.PUT_LINE(v_sql);
        
        IF r.t201iq_data_table IS NOT NULL THEN
            v_sql := 'TRUNCATE TABLE ' || r.t201iq_data_table || ' ;';
            DBMS_OUTPUT.PUT_LINE(v_sql);
        END IF;
    END LOOP;
  END generate_truncate_statements_prices_and_exchange_rates_seconds_qh;

  PROCEDURE generate_truncate_statements_afrr_seconds_qh IS
    v_sql VARCHAR2(4000);
  BEGIN
    FOR r IN (
        SELECT t201data_table, t201iq_data_table
        FROM t201timeseries
        WHERE t206entity IN (
            SELECT oid
            FROM t206entity
            WHERE get_full_code(OID) LIKE '%\SS_CONTROL_ENERGY\AFRR\AFRR_SECONDS%'
        )
        AND t201data_table IS NOT NULL
        AND T201IS_SYSTEM = 0
    ) LOOP
        v_sql := 'TRUNCATE TABLE ' || r.t201data_table || ' ;';
        DBMS_OUTPUT.PUT_LINE(v_sql);
        
        IF r.t201iq_data_table IS NOT NULL THEN
            v_sql := 'TRUNCATE TABLE ' || r.t201iq_data_table || ' ;';
            DBMS_OUTPUT.PUT_LINE(v_sql);
        END IF;
    END LOOP;
  END generate_truncate_statements_afrr_seconds_qh;

  PROCEDURE generate_truncate_statements_activation_second_qh IS
    v_sql VARCHAR2(4000);
  BEGIN
    FOR r IN (
        SELECT t201data_table, t201iq_data_table
        FROM t201timeseries
        WHERE t206entity IN (
            SELECT oid
            FROM t206entity
            WHERE get_full_code(OID) LIKE '%\SS_INPUT_DATA\ACTIVATION\ACTIVATION_SECOND%'
        )
        AND t201data_table IS NOT NULL
        AND T201IS_SYSTEM = 0
    ) LOOP
        v_sql := 'TRUNCATE TABLE ' || r.t201data_table || ' ;';
        DBMS_OUTPUT.PUT_LINE(v_sql);
        
        IF r.t201iq_data_table IS NOT NULL THEN
            v_sql := 'TRUNCATE TABLE ' || r.t201iq_data_table || ' ;';
            DBMS_OUTPUT.PUT_LINE(v_sql);
        END IF;
    END LOOP;
  END generate_truncate_statements_activation_second_qh;

  PROCEDURE generate_truncate_statements_mfrr_seconds_qh IS
    v_sql VARCHAR2(4000);
  BEGIN
    FOR r IN (
        SELECT t201data_table, t201iq_data_table
        FROM t201timeseries
        WHERE t206entity IN (
            SELECT oid
            FROM t206entity
            WHERE get_full_code(OID) LIKE '%\SS_CONTROL_ENERGY\MFRR\MFRR_SECONDS%'
        )
        AND t201data_table IS NOT NULL
        AND T201IS_SYSTEM = 0
    ) LOOP
        v_sql := 'TRUNCATE TABLE ' || r.t201data_table || ' ;';
        DBMS_OUTPUT.PUT_LINE(v_sql);
        
        IF r.t201iq_data_table IS NOT NULL THEN
            v_sql := 'TRUNCATE TABLE ' || r.t201iq_data_table || ' ;';
            DBMS_OUTPUT.PUT_LINE(v_sql);
        END IF;
    END LOOP;
  END generate_truncate_statements_mfrr_seconds_qh;

  PROCEDURE generate_truncate_statements_preparation_settlement_qh IS
    v_sql VARCHAR2(4000);
  BEGIN
    FOR r IN (
        SELECT t201data_table, t201iq_data_table
        FROM t201timeseries
        WHERE t206entity IN (
            SELECT oid
            FROM t206entity
            WHERE get_full_code(OID) LIKE '%\SS_CONTROL_ENERGY\PREPARATION_SETTLEMENT\PREPARATION_SETTLEMENT%'
        )
        AND t201data_table IS NOT NULL
        AND T201IS_SYSTEM = 0
    ) LOOP
        v_sql := 'TRUNCATE TABLE ' || r.t201data_table || ' ;';
        DBMS_OUTPUT.PUT_LINE(v_sql);
        
        IF r.t201iq_data_table IS NOT NULL THEN
            v_sql := 'TRUNCATE TABLE ' || r.t201iq_data_table || ' ;';
            DBMS_OUTPUT.PUT_LINE(v_sql);
        END IF;
    END LOOP;
  END generate_truncate_statements_preparation_settlement_qh;

  PROCEDURE generate_truncate_statements_energy_bids_and_reserves_seconds_qh IS
    v_sql VARCHAR2(4000);
  BEGIN
    FOR r IN (
        SELECT t201data_table, t201iq_data_table
        FROM t201timeseries
        WHERE t206entity IN (
            SELECT oid
            FROM t206entity
            WHERE get_full_code(OID) LIKE '%\SS_INPUT_DATA\ENERGY_BIDS_AND_RESERVES\ENERGY_BID_AND_RESERVES_SECOND%'
        )
        AND t201data_table IS NOT NULL
        AND T201IS_SYSTEM = 0
    ) LOOP
        v_sql := 'TRUNCATE TABLE ' || r.t201data_table || ' ;';
        DBMS_OUTPUT.PUT_LINE(v_sql);
        
        IF r.t201iq_data_table IS NOT NULL THEN
            v_sql := 'TRUNCATE TABLE ' || r.t201iq_data_table || ' ;';
            DBMS_OUTPUT.PUT_LINE(v_sql);
        END IF;
    END LOOP;
  END generate_truncate_statements_energy_bids_and_reserves_seconds_qh;

END PAVEL_STRITESKY_METADATA_TRUNCATES;
/
