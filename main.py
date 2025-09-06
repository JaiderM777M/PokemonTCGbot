import discord
from discord.ext import commands
from discord.ui import View, Select
import requests, random, json, os
import config

# -----------------------------
# CONFIGURACIÓN DEL BOT
# -----------------------------
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Archivo donde guardaremos el inventario
INVENTARIO_FILE = "inventario.json"

# Diccionario en memoria
inventario = {}

# -----------------------------
# FUNCIONES DE GUARDADO / CARGA
# -----------------------------
def guardar_inventario():
    with open(INVENTARIO_FILE, "w", encoding="utf-8") as f:
        json.dump(inventario, f, ensure_ascii=False, indent=4)

def cargar_inventario():
    global inventario
    if os.path.exists(INVENTARIO_FILE):
        with open(INVENTARIO_FILE, "r", encoding="utf-8") as f:
            inventario = json.load(f)
    else:
        inventario = {}

# Cargamos inventario al iniciar
cargar_inventario()

# -----------------------------
# COMANDO PARA SACAR CARTA
# -----------------------------
@bot.command()
async def pokem(ctx):
    try:
        # Pide las cartas
        url = "https://api.tcgdex.net/v2/en/cards"
        response = requests.get(url).json()
        card = random.choice(response)

        # Datos de la carta
        card_name = card.get("name", "Desconocido")
        card_rarity = card.get("rarity", "Normal")
        image_url = f"{card['image']}/high.png"

        # Guarda en inventario (organizado por rareza oficial)
        user_id = str(ctx.author.id)
        if user_id not in inventario:
            inventario[user_id] = {}
        if card_rarity not in inventario[user_id]:
            inventario[user_id][card_rarity] = []
        inventario[user_id][card_rarity].append({"name": card_name, "url": image_url})
        guardar_inventario()

        # Muestra en embed
        embed = discord.Embed(
            title=f"🎴 {card_name}",
            description=f"**Rareza:** {card_rarity}",
            color=discord.Color.blue()
        )
        embed.set_image(url=image_url)
        await ctx.send(embed=embed)

    except Exception as e:
        await ctx.send(f"Ocurrió un error: {e}")

# -----------------------------
# COMANDO PARA VER INVENTARIO (MENÚ INTERACTIVO)
# -----------------------------
@bot.command(name="inve")
async def inve(ctx):
    user_id = str(ctx.author.id)
    if user_id not in inventario or not any(inventario[user_id].values()):
        await ctx.send("📭 No tienes cartas todavía. Usa `!pokem` para conseguir una.")
        return

    # Juntar todas las cartas del usuario (ordenadas por rareza)
    cartas_total = []
    for rareza, cartas in inventario[user_id].items():
        for carta in cartas:
            cartas_total.append({"name": carta["name"], "url": carta["url"], "rareza": rareza})

    # Crear opciones para el menú desplegable (máx. 25 por Discord)
    opciones = [
        discord.SelectOption(
            label=carta["name"],
            description=f"Rareza: {carta['rareza']}",
            value=str(i)
        )
        for i, carta in enumerate(cartas_total[:25])
    ]

    # Crear el menú
    select = Select(
        placeholder="📚 Selecciona una carta para ver...",
        options=opciones
    )

    async def select_callback(interaction: discord.Interaction):
        index = int(select.values[0])
        carta = cartas_total[index]

        embed = discord.Embed(
            title=f"🎴 {carta['name']}",
            description=f"**Rareza oficial:** {carta['rareza']}",
            color=discord.Color.green()
        )
        embed.set_image(url=carta["url"])
        await interaction.response.send_message(embed=embed, ephemeral=True)

    select.callback = select_callback

    # Crear vista con el menú
    view = View()
    view.add_item(select)

    await ctx.send("📚 Aquí está tu inventario, selecciona una carta:", view=view)

# -----------------------------
# INICIO DEL BOT
# -----------------------------
bot.run(config.TOKEN)
