# "IoT Hardware" Servis

Sahada bulunan IoT cihazlardan gelen verileri karşılayan servistir. Bu servis gelen verilere şema kontrolü yaparak verileri doğrular. Gelen veri şemaya uygun ve doğrulanmış ise "Pack.RAW" topiği ile kafka kuyruğuna gönderir. Gelen veri şemaya uygun değil ise "Pack.ERROR" topiği ile kafka kuyruğuna gönderir.

Gelen veri paketi yapısı aşağıdaki gibidir:

```json
{
    "Info": {
        "Command": "Timed",
        "TimeStamp": "2024-03-20 14:40:49",
        "ID": "C50010011D05A970",
        "IMEI": "354485417649443",
        "ICCID": "8990000930090169339",
        "Firmware": "04.00.20"
    },
    "Device": {
        "Power": {
            "B_IV": 4.0,
            "B_AC": 0.47,
            "B_IC": 1600,
            "B_FC": 1500,
            "B_SOC": 99.00,
            "B_T": 24.50,
            "B_CS": 3
        },
        "IoT": {
            "RSSI": 66,
            "WDS": 3,
            "ConnTime": 3.724,
            "MCC": 286,
            "MNC": 1,
            "TAC": 8770,
            "Cell_ID": 53541
        }
    },
    "Payload": {
        "PCB_T": 45.13,
        "PCB_H": 19,
        "VRMS_R": 222.92,
        "VRMS_S": 222.82,
        "VRMS_T": 222.93,
        "VFun_MIN_R": 111
    }
}```

Info segmenti içerisinde yer alan bilgiler dışındaki kısımlar zorunlu veri değildir. Sayısal veri içeren değişkenler veritabanında yer alan "Variables" tablosunda tanımlı veriler olabilir. Bu paket geldiği gibi bir arkaplan görevi olarak kuyruğa gönderilir. Kuyruğa gönderilirken eğer doğrulanmış veri ise aşağıda belirtilen header bilgisi ile kuyruğa atılır.

* Device_IP
* Pack_Size
