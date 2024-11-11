SET SERVEROUTPUT ON;

DECLARE
    row_count NUMBER;
BEGIN
    FOR r IN (
        SELECT t201data_table, get_full_code(oid) full_codes
        FROM t201timeseries ts
        WHERE t206entity IN (
            SELECT oid FROM t206entity WHERE get_full_code(oid) IN (
                '\SS_INPUT_DATA\ENERGY_BIDS_AND_RESERVES\ENERGY_BID_AND_RESERVES',
                '\SS_INPUT_DATA\ENERGY_BIDS_AND_RESERVES\ENERGY_BID_AND_RESERVES_SECOND'
            )
        )
        AND T201IS_SYSTEM = 0
        AND t201data_table LIKE '%TT%'
    ) LOOP
        EXECUTE IMMEDIATE 'SELECT count(*) FROM ' || r.t201data_table INTO row_count;
        DBMS_OUTPUT.PUT_LINE('Table ' || r.t201data_table || ' has ' || row_count || ' rows ;           ' || r.full_codes);
    END LOOP;
END;
/