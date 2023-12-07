WITH valueranks AS (
    SELECT ws."Measurement_ID",
        s."Device_ID",
        ws."Stream_ID",
        dt."Variable",
        ws."Value",
        ws."Create_Time",
        rank() OVER (PARTITION BY s."Device_ID", dt."Variable" ORDER BY ws."Value" DESC) AS "MaxRank",
        rank() OVER (PARTITION BY s."Device_ID", dt."Variable" ORDER BY ws."Value") AS "MinRank",
        lag(ws."Value") OVER (PARTITION BY s."Device_ID", dt."Variable" ORDER BY ws."Create_Time") AS "PreviousValue"
       FROM "Payload" ws
         JOIN "Stream" s ON ws."Stream_ID" = s."Stream_ID"
         JOIN "Data_Type" dt ON ws."Type_ID" = dt."Type_ID"
      WHERE ws."Create_Time" > (CURRENT_TIMESTAMP - interval '24 hours')
    )
SELECT v."Measurement_ID",
    v."Device_ID",
    v."Stream_ID",
    v."Variable",
    v."Value",
    v."Create_Time",
    max(v."Value") FILTER (WHERE v."MaxRank" = 1) OVER (PARTITION BY v."Device_ID", v."Variable") AS "Max",
    max(v."Create_Time") FILTER (WHERE v."MaxRank" = 1) OVER (PARTITION BY v."Device_ID", v."Variable") AS "Max_Time",
    min(v."Value") FILTER (WHERE v."MinRank" = 1) OVER (PARTITION BY v."Device_ID", v."Variable") AS "Min",
    min(v."Create_Time") FILTER (WHERE v."MinRank" = 1) OVER (PARTITION BY v."Device_ID", v."Variable") AS "Min_Time",
    v."PreviousValue",
    CASE
        WHEN v."Value" > v."PreviousValue" THEN 1
        WHEN v."Value" < v."PreviousValue" THEN -1
        ELSE 0
    END AS "Trend"
FROM valueranks v
ORDER BY v."Stream_ID" DESC, v."Create_Time" DESC;
