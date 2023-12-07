SELECT 
    "SIM"."ICCID",
    COALESCE(SUM(CASE WHEN EXTRACT(MONTH FROM "Stream"."Stream_Time") = 1 THEN "Stream"."Size" ELSE 0 END), 0) AS January,
    COALESCE(SUM(CASE WHEN EXTRACT(MONTH FROM "Stream"."Stream_Time") = 2 THEN "Stream"."Size" ELSE 0 END), 0) AS February,
    COALESCE(SUM(CASE WHEN EXTRACT(MONTH FROM "Stream"."Stream_Time") = 3 THEN "Stream"."Size" ELSE 0 END), 0) AS March,
    COALESCE(SUM(CASE WHEN EXTRACT(MONTH FROM "Stream"."Stream_Time") = 4 THEN "Stream"."Size" ELSE 0 END), 0) AS April,
    COALESCE(SUM(CASE WHEN EXTRACT(MONTH FROM "Stream"."Stream_Time") = 5 THEN "Stream"."Size" ELSE 0 END), 0) AS May,
    COALESCE(SUM(CASE WHEN EXTRACT(MONTH FROM "Stream"."Stream_Time") = 6 THEN "Stream"."Size" ELSE 0 END), 0) AS June,
    COALESCE(SUM(CASE WHEN EXTRACT(MONTH FROM "Stream"."Stream_Time") = 7 THEN "Stream"."Size" ELSE 0 END), 0) AS July,
    COALESCE(SUM(CASE WHEN EXTRACT(MONTH FROM "Stream"."Stream_Time") = 8 THEN "Stream"."Size" ELSE 0 END), 0) AS August,
    COALESCE(SUM(CASE WHEN EXTRACT(MONTH FROM "Stream"."Stream_Time") = 9 THEN "Stream"."Size" ELSE 0 END), 0) AS September,
    COALESCE(SUM(CASE WHEN EXTRACT(MONTH FROM "Stream"."Stream_Time") = 10 THEN "Stream"."Size" ELSE 0 END), 0) AS October,
    COALESCE(SUM(CASE WHEN EXTRACT(MONTH FROM "Stream"."Stream_Time") = 11 THEN "Stream"."Size" ELSE 0 END), 0) AS November,
    COALESCE(SUM(CASE WHEN EXTRACT(MONTH FROM "Stream"."Stream_Time") = 12 THEN "Stream"."Size" ELSE 0 END), 0) AS December,
    COALESCE(SUM("Stream"."Size"), 0) AS "TotalTraffic"
FROM 
    "SIM"
LEFT JOIN 
    "Stream" ON "SIM"."ICCID" = "Stream"."ICCID"
WHERE 
    EXTRACT(YEAR FROM "Stream"."Stream_Time") = EXTRACT(YEAR FROM CURRENT_DATE) OR "Stream"."Stream_Time" IS NULL
GROUP BY 
    "SIM"."ICCID";
ORDER BY 
    "TotalTraffic" DESC;
