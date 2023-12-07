SELECT 
    "Device_ID",
    SUM(CASE WHEN "Create_Time" >= NOW() - INTERVAL '1 hour' THEN "Value" ELSE 0 END) AS "R_1",
    SUM(CASE WHEN "Create_Time" >= NOW() - INTERVAL '24 hours' THEN "Value" ELSE 0 END) AS "R_24",
    SUM(CASE WHEN "Create_Time" >= NOW() - INTERVAL '48 hours' THEN "Value" ELSE 0 END) AS "R_48",
    SUM(CASE WHEN "Create_Time" >= NOW() - INTERVAL '7 days' THEN "Value" ELSE 0 END) AS "R_168"
FROM 
    "Payload_Measurement"
WHERE 
    "Variable" = 'R'
GROUP BY 
    "Device_ID";
