import discord, asyncio, random, json
from discord import app_commands
from discord.ext import commands

client = commands.Bot(command_prefix="!", intents=discord.Intents.all())
client.remove_command("help")
tree = client.tree

#Everything in the following comments should be edited
#
yourid = 301014178703998987
dbdir = "./db.json"
token = "nigger token"
#

@client.event
async def on_ready():
    print(f"Password Manager now online with {round(client.latency * 1000)}ms ping.")

create = app_commands.Group(name="create", description="Create a password")
tree.add_command(create)

@create.command(name="temp", description="Create a temporary password")
@app_commands.check(lambda interaction : interaction.user.id == yourid)
async def temp(interaction : discord.Interaction):
    await interaction.response.send_message("Loading...")
    chars = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    password = ""
    for el in range(20):
        password +=random.choice(chars)
    await interaction.edit_original_response(content=None, embed=discord.Embed(title="Temporary Password", colour=0x3cf55e, description=f"Your **one-time** password is;`{password}`").set_thumbnail(url="https://i.ibb.co/JC1mL9n/PFP.png"))

@create.command(name="perm", description="Create a permanent password")
@app_commands.check(lambda interaction : interaction.user.id == yourid)
async def perm(interaction : discord.Interaction, site : str):
    await interaction.response.send_message("Loading...")
    chars = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    password = ""
    for el in range(20):
        password += random.choice(chars)
    with open(dbdir, "r+") as f:
        data = json.load(f)
        data[password] = site
        f.seek(0)
        f.truncate()
        json.dump(data, f, indent=4)
    await interaction.edit_original_response(content=None, embed=discord.Embed(title="Permanent Password", colour=0x3cf55e, description=f"Your password for **{site}** is;`{password}`\nIt has been added to your database of passwords.").set_thumbnail(url="https://i.ibb.co/JC1mL9n/PFP.png"))

@tree.command(name="insert", description="Insert a password into you database")
@app_commands.check(lambda interaction : interaction.user.id == yourid)
async def insert(interaction : discord.Interaction, password : str, site : str):
    await interaction.response.send_message("Loading...")
    with open(dbdir, "r+") as f:
        data = json.load(f)
        data[password] = site
        f.seek(0)
        f.truncate()
        json.dump(data, f, indent=4)
    await interaction.edit_original_response(content=None, embed=discord.Embed(title="Password Insert", colour=0x3cf55e, description=f"Your password; `{password}` for **{site}** has been inserted into the database.").set_thumbnail(url="https://i.ibb.co/JC1mL9n/PFP.png"))

class PagesStart(discord.ui.View):
    def __init__(self, timeout):
        super().__init__(timeout=timeout)
        self.value = None
    
    @discord.ui.button(label='\U000027a1', style=discord.ButtonStyle.grey)
    async def right(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Next page", ephemeral=True)
        self.value = True
        self.stop()

class Pages(discord.ui.View):
    def __init__(self, timeout):
        super().__init__(timeout=timeout)
        self.value = None
    
    @discord.ui.button(label='\U00002b05', style=discord.ButtonStyle.grey)
    async def left(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Previous page", ephemeral=True)
        self.value = False
        self.stop()
    
    @discord.ui.button(label='\U000027a1', style=discord.ButtonStyle.grey)
    async def right(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Next page", ephemeral=True)
        self.value = True
        self.stop()

class PagesEnd(discord.ui.View):
    def __init__(self, timeout):
        super().__init__(timeout=timeout)
        self.value = None
    
    @discord.ui.button(label='\U00002b05', style=discord.ButtonStyle.grey)
    async def left(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Previous page", ephemeral=True)
        self.value = False
        self.stop()

@tree.command(name="db", description="Fetch your password database")
@app_commands.check(lambda interaction : interaction.user.id == yourid)
async def perm(interaction : discord.Interaction):
    await interaction.response.send_message("Loading...")
    small = None
    with open(dbdir, "r+") as f:
        data = json.load(f)
        if len(data.keys()) < 25:
            small = data
        else:
            big = data
    if small:
        embed = discord.Embed(
            title="Password Database",
            colour=0x3cf55e,
            description=None
        )
        embed.set_thumbnail(url="https://i.ibb.co/JC1mL9n/PFP.png")
        for el in small:
            embed.add_field(name=small[el], value=el, inline=False)
        await interaction.edit_original_response(content=None, embed=embed)
    else:
        pagesitems = []
        pages = []
        new = {}
        for key, value in big.items():
            new[key] = value
            if len(new) == 25:
                pagesitems.append(new)
                new = {}
        if new != {}:
            pagesitems.append(new)
        for el in pagesitems:
            embed = discord.Embed(
                title="Password Database",
                colour=0x3cf55e,
                description=f"Page {pagesitems.index(el)+1}"
            )
            embed.set_thumbnail(url="https://i.ibb.co/JC1mL9n/PFP.png")
            for foo, bar in el.items():
                embed.add_field(name=bar, value=foo, inline=False)
            pages.append(embed)
        activepage = pages[0]
        async def display(activepage):
            if activepage == pages[0]:
                view = PagesStart(timeout=60)
            elif activepage == pages[-1]:
                view = PagesEnd(timeout=60)
            else:
                view = Pages(timeout=60)
            await interaction.edit_original_response(content=None, embed=activepage, view=view)
            await view.wait()
            if view.value != None:
                if view.value == True:
                    #Up page
                    activepage = pages[pages.index(activepage)+1]
                else:
                    #Down page
                    activepage = pages[pages.index(activepage)-1]
                await display(activepage)
        await display(activepage)

@tree.command(name="search", description="Search within your password database")
@app_commands.check(lambda interaction : interaction.user.id == yourid)
async def perm(interaction : discord.Interaction, site : str):
    await interaction.response.send_message("Loading...")
    isin = None
    with open(dbdir, "r+") as f:
        data = json.load(f)
        if site.lower() in [el.lower() for el in data.values()]:
            isin = list(data.keys())[list(data.values()).index(site)]
    if isin:
        await interaction.edit_original_response(content=None, embed=discord.Embed(title="Password Search", colour=0x3cf55e, description=f"Your password for **{site}** is;`{isin}`").set_thumbnail(url="https://i.ibb.co/JC1mL9n/PFP.png"))
    else:
        await interaction.edit_original_response(content=None, embed=discord.Embed(title="Search Error", colour=0xf53c3c, description=f"Uh-oh, seems like we can't find a password under **{site}** in your database").set_thumbnail(url="https://i.ibb.co/JC1mL9n/PFP.png"))

@client.command()
@commands.check(lambda ctx : ctx.author.id == yourid)
async def connect(ctx):
    await tree.sync()

client.run(token)