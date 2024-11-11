 -- Vytvoření těla balíčku metadata_checks
CREATE OR REPLACE PACKAGE BODY metadata_checks AS

    PROCEDURE count_rows_in_TG_tables IS
        row_count NUMBER;
    BEGIN
        FOR r IN (
            SELECT t201data_table, get_full_code(oid) full_codes
            FROM t201timeseries ts
            WHERE T201IS_SYSTEM = 0
              AND t201data_table LIKE '%TG%'
              AND GET_FULL_CODE(OID) NOT LIKE '%\SS_SYS\SS_SYS_SYS%'
              AND T201DATA_TABLE IS NOT NULL
        ) LOOP
            EXECUTE IMMEDIATE 'SELECT count(*) FROM ' || r.t201data_table INTO row_count;
            DBMS_OUTPUT.PUT_LINE('Table ' || r.t201data_table || ' has ' || row_count || ' rows ; ' || r.full_codes);
        END LOOP;
    END count_rows_in_TG_tables;

    PROCEDURE count_rows_in_TT_tables IS
        row_count NUMBER;
    BEGIN
        FOR r IN (
            SELECT t201data_table, get_full_code(oid) full_codes
            FROM t201timeseries ts
            WHERE T201IS_SYSTEM = 0
              AND t201data_table LIKE '%TT%'
              AND GET_FULL_CODE(OID) NOT LIKE '%\SS_SYS\SS_SYS_SYS%'
              AND T201DATA_TABLE IS NOT NULL
        ) LOOP
            EXECUTE IMMEDIATE 'SELECT count(*) FROM ' || r.t201data_table INTO row_count;
            DBMS_OUTPUT.PUT_LINE('Table ' || r.t201data_table || ' has ' || row_count || ' rows ; ' || r.full_codes);
        END LOOP;
    END count_rows_in_TT_tables;

END metadata_checks;
/

;


SET SERVEROUTPUT ON;

BEGIN
    metadata_checks.count_rows_in_TG_tables;
    metadata_checks.count_rows_in_TT_tables;
END;
/

