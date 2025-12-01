from dotenv import load_dotenv
import os
import discord


class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = discord.app_commands.CommandTree(self)

    async def on_ready(self):
        GUILD_ID = discord.Object(id=os.getenv("SERVER_ID"))
        await self.tree.sync(guild=GUILD_ID)

        # Ohne Angabe einer Guild werden die Befehle global registriert.
        # await self.tree.sync()
        print(f'Eingeloggt als {self.user} und Befehle synchronisiert!')


intents = discord.Intents.default()
client = MyClient(intents=intents)


@client.tree.command(name="hallo", description="Sagt Hallo und begrüßt dich.")
async def hallo_command(interaction: discord.Interaction):
    await interaction.response.send_message(f'Hallo, {interaction.user.mention}!')

@client.tree.command(name="add", description="Addiert zwei Zahlen für dich.")
@discord.app_commands.describe(
    zahl1="Die erste Zahl, die du addieren möchtest",
    zahl2="Die zweite Zahl, die du addieren möchtest"
)
async def add_command(interaction: discord.Interaction, zahl1: int, zahl2: int):
    ergebnis = zahl1 + zahl2
    await interaction.response.send_message(f'Das Ergebnis von {zahl1} + {zahl2} ist {ergebnis}.')

if __name__ == '__main__':
    load_dotenv()
    dc_token = os.getenv('DC_TOKEN')
    client.run(dc_token)
