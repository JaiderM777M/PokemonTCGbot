# 🎴 Bot de Cartas Pokémon para Discord

Este es un bot de Discord que permite a los usuarios sacar cartas Pokémon aleatorias desde la [PokeAPI](https://pokeapi.co/) y guardarlas en su inventario personal. El bot incluye comandos básicos para interactuar y gestionar tu colección.

---

## ⚙️ Instalación

1. Descarga el proyecto en formato `.zip` o cópialo en tu computadora.
2. Asegúrate de tener **Python 3.10+** instalado.
3. Abre una terminal dentro de la carpeta del proyecto.
4. Instala las dependencias con:
   bash
   pip install -r requirements.txt
   
5. Configura el archivo `config.py` con tu token de Discord:
   python
   TOKEN = "tu_token_aqui"
   
6. Ejecuta el bot con:
   bash
   python bot.py
  


## 🎮 Uso del Bot

Una vez que el bot esté en línea en tu servidor de Discord, puedes usar los siguientes comandos:

- !pokem  → Obtiene una carta Pokémon aleatoria de la PokeAPI.
- !inve → Muestra tu inventario de cartas.

El inventario se guarda en un archivo `inventario.json` para que no pierdas tu colección aunque apagues el bot.



## 📂 Archivos principales

- **bot.py** → Código principal del bot.
- **config.py** → Contiene tu token de autenticación de Discord por tanto ingresar token propio para las pruebas.
- **requirements.txt** → Lista de dependencias necesarias para ejecutar el bot.
- **inventario.json** → Se genera automáticamente para almacenar las cartas de cada usuario.

---

## ✅ Requisitos previos

- Tener una cuenta en [Discord](https://discord.com/).
- Crear una aplicación y bot en el [Portal de Desarrolladores de Discord](https://discord.com/developers/applications).
- Invitar el bot a tu servidor con los permisos correspondientes.

