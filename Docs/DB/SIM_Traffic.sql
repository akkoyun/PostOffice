SELECT "SIM"."ICCID", COALESCE(SUM("Stream"."Size"), 0) AS "TotalTraffic"
FROM "SIM"
LEFT JOIN "Stream" ON "SIM"."ICCID" = "Stream"."ICCID"
WHERE DATE_TRUNC('month', "Stream"."Stream_Time") = DATE_TRUNC('month', CURRENT_DATE) OR "Stream"."Stream_Time" IS NULL
GROUP BY "SIM"."ICCID"
ORDER BY "TotalTraffic" DESC;
