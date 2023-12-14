# Setup Library
import sys
sys.path.append('/root/PostOffice/')

# Library Includes
from Setup import Definitions
from Functions import Kafka, Log, Handler
import discord, asyncio
from Setup.Config import APP_Settings

# Set Discord Intents
intents = discord.Intents.default()
intents.messages = False
intents.guilds = True

# Define Discord Client
Discord_Client = discord.Client(intents=intents)

# Define Discord Login
@Discord_Client.event
async def on_ready():

    # Log Message
    Log.Terminal_Log("INFO", f'Login as: {Discord_Client.user}')

    # Process Kafka Messages
    await Discord_Client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="PostOffice"))

    # Process Kafka Messages
    asyncio.create_task(Parse_Message())

# Mesaj gönderme fonksiyonu
async def Send_Discord_Message(channel_id, message):

    # Get Channel
    channel = Discord_Client.get_channel(channel_id)

    # Control Channel
    if channel:
        await channel.send(message)
    else:
        print("Kanal bulunamadı.")

# Try to Parse Topics
async def Parse_Message():

    try:

        # Parse Topics
        for RAW_Message in Kafka.Discord_Consumer:

            # Handle Headers
            RAW_Headers = Definitions.Handler_Headers(
                RAW_Message.headers[0][1].decode('ASCII'),
                RAW_Message.headers[1][1].decode('ASCII'),
                RAW_Message.headers[2][1].decode('ASCII'),
                RAW_Message.headers[3][1].decode('ASCII'),
                RAW_Message.headers[4][1].decode('ASCII'),
                RAW_Message.headers[5][1].decode('ASCII'),
                RAW_Message.headers[6][1].decode('ASCII'),
                RAW_Message.headers[7][1].decode('ASCII'),
            )

            # Convert Device Time (str) to datetime
            Device_Time = RAW_Headers.Device_Time.replace("T", " ").replace("Z", "")

            # Decode Message
            Message = Kafka.Decode_Discord_Message(RAW_Message)

            # Sleep
            await asyncio.sleep(0)



            # Set Name
            if RAW_Headers.Device_ID == "A20000011D13BD70":
                Device_Name = "Diyodlu / izolesiz / Açık Yeşil Pil"
            elif RAW_Headers.Device_ID == "3E0000011D2BA170":
                Device_Name = "Diyodsuz / izolesiz / Gri Pil"
            elif RAW_Headers.Device_ID == "370000011D157470":
                Device_Name = "Diyodsuz / izoleli / Gri Pil"
            else:
                Device_Name = "Bilinmeyen"
            



            # Get Parameters
            B_IV = Handler.Get_Parameter_Measurement(RAW_Headers.Device_ID, "B_IV")
            B_SOC = Handler.Get_Parameter_Measurement(RAW_Headers.Device_ID, "B_SOC")
            B_AC = Handler.Get_Parameter_Measurement(RAW_Headers.Device_ID, "B_AC")
            B_CS = Handler.Get_Parameter_Measurement(RAW_Headers.Device_ID, "B_CS")

            # Set Message
            Discord_Message = f"```ansi\r\nDevice ID: [2;32m{RAW_Headers.Device_ID}[0m\r\n"

            # Handle Status and Project
            if RAW_Headers.Status_ID == "1": Status = "Test Device"
            elif RAW_Headers.Status_ID == "2": Status = "Demo Device"
            else: RAW_Headers.Status_ID = "Unknown"
            if RAW_Headers.Project_ID == "1": Project = "WeatherStat"
            elif RAW_Headers.Project_ID == "2": Project = "PowerStat"
            else: RAW_Headers.Project_ID = "Unknown"

            Discord_Message += f"Device Type: [2;35m{Project} / {Status}[0m\r\n"
            Discord_Message += f"Device Description: [2;32m{Device_Name}[0m\r\n"
            Discord_Message += f"Device Time: [2;34m{Device_Time}[0m\r\n"
            if Message.AT is not None: Discord_Message += f"Hava Sıcaklığı: [2;35m{Message.AT}[0m[2;33m[0m °C\r\n"
            if Message.AH is not None: Discord_Message += f"Bağıl Nem: [2;35m{Message.AH}[0m %\r\n"
            if Message.P is not None: Discord_Message += f"Hava Basıncı: [2;35m{Message.P}[0m hPa\r\n"
            if Message.R is not None: Discord_Message += f"Yağış: [2;35m{Message.R}[0m tip\r\n"
            if Message.WS is not None: Discord_Message += f"Rüzgar Hızı: [2;35m{Message.WS}[0m m/s\r\n"
            if Message.WD is not None: Discord_Message += f"Rüzgar Yönü: [2;35m{Message.WD}[0m °\r\n"
            if Message.UV is not None: Discord_Message += f"UV: [2;35m{Message.UV}[0m index\r\n"
            if Message.ST0 is not None: Discord_Message += f"Toprak Sıcaklığı 10cm: [2;35m{Message.ST0}[0m °C\r\n"
            if Message.ST1 is not None: Discord_Message += f"Toprak Sıcaklığı 20cm: [2;35m{Message.ST1}[0m °C\r\n"
            if Message.ST2 is not None: Discord_Message += f"Toprak Sıcaklığı 30cm: [2;35m{Message.ST2}[0m °C\r\n"
            if Message.ST3 is not None: Discord_Message += f"Toprak Sıcaklığı 40cm: [2;35m{Message.ST3}[0m °C\r\n"
            if Message.ST4 is not None: Discord_Message += f"Toprak Sıcaklığı 50cm: [2;35m{Message.ST4}[0m °C\r\n"
            if Message.ST5 is not None: Discord_Message += f"Toprak Sıcaklığı 60cm: [2;35m{Message.ST5}[0m °C\r\n"
            if Message.ST6 is not None: Discord_Message += f"Toprak Sıcaklığı 70cm: [2;35m{Message.ST6}[0m °C\r\n"
            if Message.ST7 is not None: Discord_Message += f"Toprak Sıcaklığı 80cm: [2;35m{Message.ST7}[0m °C\r\n"
            if Message.ST8 is not None: Discord_Message += f"Toprak Sıcaklığı 90cm: [2;35m{Message.ST8}[0m °C\r\n"
            if Message.ST9 is not None: Discord_Message += f"Toprak Sıcaklığı 100cm: [2;35m{Message.ST9}[0m °C\r\n"
            Discord_Message += f"------------------------------------------\r\n"
            if B_IV is not None: Discord_Message += f"Batarya Voltajı: [2;35m{B_IV.Last_Value}[0m V\r\n"
            if B_AC is not None: Discord_Message += f"Batarya Ortalama Akım: [2;35m{B_AC.Last_Value}[0m mA\r\n"
            if B_SOC is not None: Discord_Message += f"Batarya Yüzdesi: [2;35m{B_SOC.Last_Value}[0m %\r\n"
            if B_CS is not None:
                if B_CS.Last_Value == 0:
                    Discord_Message += f"Şarj Durumu: [2;31mNot Charging[0m\r\n"
                elif B_CS.Last_Value == 1:
                    Discord_Message += f"Şarj Durumu: [2;32mPre Charge[0m\r\n"
                elif B_CS.Last_Value == 2:
                    Discord_Message += f"Şarj Durumu: [2;32mFast Charge[0m\r\n"
                else:
                    Discord_Message += f"Şarj Durumu: [2;32mCharge Termination / Done[0m\r\n"
            Discord_Message += f"```"

            # Send Discord Message
            await Send_Discord_Message(APP_Settings.DISCORD_CHANNEL_ID, Discord_Message)

            # Commit Kafka Consumer
            Kafka.Discord_Consumer.commit()

            # Sleep
            await asyncio.sleep(0)

            # Log Message
            Log.Terminal_Log("INFO", f"******************************")

    # Handle Errors
    except Exception as e:

        # Log Message
        Log.Terminal_Log("ERROR", f"Handler Error: {e}")

# Run Discord Bot
Discord_Client.run(APP_Settings.DISCORD_TOKEN)
