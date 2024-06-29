# Setup Root Path
import sys
sys.path.append('/home/postoffice/PostOffice/src')

# Include Libraries
import discord, asyncio, ssl, certifi, aiohttp
from Setup import Database, Models
from Functions import Log

# Send Message to Discord Channel
async def Send_Discord_Message(Discord_ID: int, Message: str):

    # Define Variables
    Discord_Token = None
    Discord_Channel_ID = None

    # Try to open a database session
    try:

        # Define DB
        with Database.SessionLocal() as DB_Module:

            # Try to query the Discord Channel
            try:

                # Query Discord Channel
                Discord_Query = DB_Module.query(Models.Discord).filter(
                    Models.Discord.Discord_ID == Discord_ID
                ).first()

                # Check if Channel Exists
                if Discord_Query:

                    # Get Token
                    Discord_Token = Discord_Query.Discord_Token

                    # Get Channel_ID
                    Discord_Channel_ID = Discord_Query.Discord_Channel_ID

                    # Log Message
                    Log.Terminal_Log('INFO', f"Token: {Discord_Token}, Channel_ID: {Discord_Channel_ID}")

                    # Set SSL Context
                    SSL_Context = ssl.create_default_context(cafile=certifi.where())

                    # Define Client
                    Intents = discord.Intents.default()
                    Intents.message_content = True
                    Intents.presences = True
                    Intents.members = True

                    # Define Client
                    class MyClient(discord.Client):

                        # On Ready
                        async def on_ready(self):

                            # Log Login
                            Log.Terminal_Log('INFO', f'Bot {self.user} logged in!')

                            # Try to send a message
                            try:

                                # Get Channel
                                Channel = self.get_channel(Discord_Channel_ID)

                                # Check if Channel Exists
                                if Channel:

                                    # Send Message
                                    await Channel.send(Message)

                                    # Log Message
                                    Log.Terminal_Log('INFO', f'Message sent to {Channel.name} channel.')

                                # Channel Not Found
                                else:

                                    # Log Message
                                    Log.Terminal_Log('ERROR', 'Channel not found.')

                            # Handle Exception
                            except Exception as e:

                                # Log Error
                                Log.Terminal_Log('ERROR', f"Error while sending message: {e}")

                            # Close Client
                            finally:

                                # Close Client
                                await self.close()

                        # Close Client
                        async def close(self):

                            # Check if Session Exists
                            if self.http._HTTPClient__session:

                                # Close Session
                                await self.http._HTTPClient__session.close()

                            await super().close()

                    # Create Client
                    Client = MyClient(intents=Intents)

                    # Run Client
                    async def run_bot():

                        # Create Connection
                        conn = aiohttp.TCPConnector(ssl=SSL_Context)

                        # Create Session
                        async with aiohttp.ClientSession(connector=conn) as Session:

                            # Set Session
                            Client.http._HTTPClient__session = Session

                            # Start Client
                            await Client.start(Discord_Token)

                            # Close Client
                            await Client.close()

                            # Close Session
                            await Session.close()

                    # Run Bot
                    await run_bot()

                # Channel Not Found
                else:

                    # Log Error
                    Log.Terminal_Log('ERROR', f"Discord Channel not found: {Discord_ID}")

                    # Exit Function
                    return
            
            # Handle Exception
            except Exception as e:

                # Log Error
                Log.Terminal_Log('ERROR', f"Error while querying command: {e}")

    # Handle Exception
    except Exception as e:

        # Log Error
        Log.Terminal_Log('ERROR', f"Error while opening database session: {e}")

# Run Discord Message Sender
asyncio.get_event_loop().run_until_complete(Send_Discord_Message(1, 'Birinci Deneme Mesajı'))
