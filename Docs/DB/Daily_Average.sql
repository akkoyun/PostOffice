SELECT
    "Device_ID",
    DATE("Create_Time") as "Date",
    AVG(CASE WHEN "Variable" = 'AT' THEN "Value" ELSE NULL END) as "AT",
    AVG(CASE WHEN "Variable" = 'AH' THEN "Value" ELSE NULL END) as "AH",
    AVG(CASE WHEN "Variable" = 'AP' THEN "Value" ELSE NULL END) as "AP"
FROM
    "Payload_Measurement"
WHERE
    "Variable" IN ('AT', 'AH', 'AP')
GROUP BY
    "Device_ID", DATE("Create_Time");
