CREATE OR REPLACE PACKAGE PAVEL_STRITESKY_METADATA_PROCEDURES AS
    PROCEDURE update_t201timeseries_hist_type;
END PAVEL_STRITESKY_METADATA_PROCEDURES;
/

CREATE OR REPLACE PACKAGE BODY PAVEL_STRITESKY_METADATA_PROCEDURES AS
    PROCEDURE update_t201timeseries_hist_type AS
    BEGIN
        UPDATE t201timeseries
        SET T487HISTORIZATION_TYPE = 'FULL_HISTORIZATION'
        WHERE oid IN (
            SELECT oid
            FROM t201timeseries
            WHERE T495STORAGE_TYPE != 'CLUSTERED_DATA_TABLE'
              AND T201IS_SYSTEM = 0
              AND t206entity IN (
                  SELECT oid
                  FROM t206entity
                  WHERE get_full_code(oid) NOT LIKE '%STANDING%'
                    AND get_full_code(oid) NOT LIKE '%SS_SYS%'
                    AND get_full_code(oid) NOT LIKE '%\MERDEV_%'
                    AND get_full_code(oid) NOT LIKE '%BUF_PERFORMANCE_TESTS%'
                    AND get_full_code(oid) NOT LIKE '%\ONLINE_SERVICE%'
              )
        );

        DBMS_OUTPUT.PUT_LINE(SQL%ROWCOUNT || ' rows updated in t201timeseries.');
    END update_t201timeseries_hist_type;
END PAVEL_STRITESKY_METADATA_PROCEDURES;
/


BEGIN
    PAVEL_STRITESKY_METADATA_PROCEDURES.update_t201timeseries_hist_type;
END;
/



Sub-System Internal User passive 
Module 
Entity 
View 