-- problem s db monitorem

delete from CN_JM2_EU_BUSINESSGROUP_BIND where businessgroup = 'EXTERNAL_INTERFACE'; commit;

-- odstranení mfrr bidů z fronty job managera 

select oid from cn_jm2_job where created > sysdate -  1 and STATE = 'W' and name  like '%MFRR\MFRR_BID_ENTITY\CREATE%' order by created desc;

DECLARE  O_RESULT NUMBER;
begin
  for job in 
  (select oid from cn_jm2_job where created > sysdate -  1 and STATE = 'W' and name  like '%MFRR\MFRR_BID_ENTITY\CREATE%' order by created desc)
  
  loop
    CN_JM2_REGISTRY.JOB_SUSPEND(
      I_JOB => job.oid,
      O_RESULT => O_RESULT
    );
    DBMS_OUTPUT.PUT_LINE('O_RESULT = ' || O_RESULT);
  end loop;
end;