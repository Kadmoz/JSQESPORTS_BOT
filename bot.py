import discord
from discord.ext import commands, tasks
from datetime import datetime, timedelta
import json
import os

# Configuración del bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Archivo para guardar datos
DATA_FILE = 'torneos.json'

# Días de la semana en español
DIAS = {
    0: 'Lunes',
    1: 'Martes',
    2: 'Miércoles',
    3: 'Jueves',
    4: 'Viernes',
    5: 'Sábado',
    6: 'Domingo'
}

# Estructura inicial de datos
def cargar_datos():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        return {
            'torneos': [
                {'nombre': 'Liga Canalla Prime', 'dia': 'Lunes', 'hora': None, 'admin': None, 'stream': None, 'activo_desde': None, 'activo_hasta': None},
                {'nombre': 'EDR División F1 Nitro', 'dia': 'Lunes', 'hora': None, 'admin': None, 'stream': None, 'activo_desde': 'marzo', 'activo_hasta': None},
                {'nombre': 'TSL División 2', 'dia': 'Martes', 'hora': None, 'admin': None, 'stream': None, 'activo_desde': None, 'activo_hasta': None},
                {'nombre': 'EDR Summer', 'dia': 'Martes', 'hora': None, 'admin': None, 'stream': None, 'activo_desde': None, 'activo_hasta': 'febrero'},
                {'nombre': 'EDR División F1 Hyper', 'dia': 'Martes', 'hora': None, 'admin': None, 'stream': None, 'activo_desde': 'marzo', 'activo_hasta': None},
                {'nombre': 'Liga Canalla Elite', 'dia': 'Martes', 'hora': None, 'admin': None, 'stream': None, 'activo_desde': None, 'activo_hasta': None},
                {'nombre': 'TSL División 1', 'dia': 'Miércoles', 'hora': None, 'admin': None, 'stream': None, 'activo_desde': None, 'activo_hasta': None},
                {'nombre': 'MRS Summer', 'dia': 'Miércoles', 'hora': None, 'admin': None, 'stream': None, 'activo_desde': None, 'activo_hasta': 'febrero'},
                {'nombre': 'Liga del Pescador División Racing', 'dia': 'Miércoles', 'hora': None, 'admin': None, 'stream': None, 'activo_desde': None, 'activo_hasta': None},
                {'nombre': 'MRS Summer', 'dia': 'Jueves', 'hora': None, 'admin': None, 'stream': None, 'activo_desde': None, 'activo_hasta': 'febrero'},
                {'nombre': 'MRS División 1', 'dia': 'Jueves', 'hora': None, 'admin': None, 'stream': None, 'activo_desde': 'marzo', 'activo_hasta': None},
                {'nombre': 'Liga Prime Time', 'dia': 'Viernes', 'hora': None, 'admin': None, 'stream': None, 'activo_desde': None, 'activo_hasta': None}
            ],
            'canal_recordatorios': None
        }

def guardar_datos(datos):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)

datos = cargar_datos()

@bot.event
async def on_ready():
    print(f'{bot.user} está conectado!')
    recordatorio_carreras.start()

# ===== COMANDOS DE CONSULTA =====

@bot.command(name='calendario', aliases=['cal'])
async def calendario(ctx):
    """Muestra el calendario completo de torneos"""
    embed = discord.Embed(
        title="🏎️ Calendario Semanal de Torneos F1 25",
        color=discord.Color.red()
    )
    
    for dia in ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']:
        torneos_dia = [t for t in datos['torneos'] if t['dia'] == dia]
        if torneos_dia:
            texto = ""
            for t in torneos_dia:
                info_extra = []
                if t['hora']:
                    info_extra.append(f"⏰ {t['hora']}")
                if t['admin']:
                    info_extra.append(f"👤 {t['admin']}")
                if t['activo_desde'] or t['activo_hasta']:
                    periodo = []
                    if t['activo_desde']:
                        periodo.append(f"desde {t['activo_desde']}")
                    if t['activo_hasta']:
                        periodo.append(f"hasta {t['activo_hasta']}")
                    info_extra.append(f"📅 {' '.join(periodo)}")
                
                texto += f"**{t['nombre']}**\n"
                if info_extra:
                    texto += " | ".join(info_extra) + "\n"
                texto += "\n"
            
            embed.add_field(name=f"📍 {dia}", value=texto, inline=False)
    
    await ctx.send(embed=embed)

@bot.command(name='hoy')
async def hoy(ctx):
    """Muestra las carreras de hoy"""
    dia_actual = DIAS[datetime.now().weekday()]
    torneos_hoy = [t for t in datos['torneos'] if t['dia'] == dia_actual]
    
    if not torneos_hoy:
        await ctx.send(f"No hay carreras programadas para hoy ({dia_actual}) 😢")
        return
    
    embed = discord.Embed(
        title=f"🏁 Carreras de Hoy - {dia_actual}",
        color=discord.Color.green()
    )
    
    for t in torneos_hoy:
        info = []
        if t['hora']:
            info.append(f"**Hora:** {t['hora']}")
        if t['admin']:
            info.append(f"**Admin:** {t['admin']}")
        if t['stream']:
            info.append(f"**Stream:** {t['stream']}")
        
        valor = "\n".join(info) if info else "Información pendiente"
        embed.add_field(name=t['nombre'], value=valor, inline=False)
    
    await ctx.send(embed=embed)

@bot.command(name='proxima', aliases=['pc'])
async def proxima(ctx):
    """Muestra la próxima carrera"""
    ahora = datetime.now()
    dia_actual = ahora.weekday()
    
    # Buscar próxima carrera
    for i in range(7):
        dia_buscar = DIAS[(dia_actual + i) % 7]
        torneos_dia = [t for t in datos['torneos'] if t['dia'] == dia_buscar and t['hora']]
        
        if torneos_dia:
            # Ordenar por hora
            torneos_dia.sort(key=lambda x: x['hora'] if x['hora'] else '99:99')
            
            for t in torneos_dia:
                if i == 0:  # Hoy
                    hora_carrera = datetime.strptime(t['hora'], '%H:%M').time()
                    if hora_carrera <= ahora.time():
                        continue
                
                embed = discord.Embed(
                    title="🏎️ Próxima Carrera",
                    description=f"**{t['nombre']}**",
                    color=discord.Color.gold()
                )
                embed.add_field(name="📅 Día", value=t['dia'], inline=True)
                embed.add_field(name="⏰ Hora", value=t['hora'], inline=True)
                
                if t['admin']:
                    embed.add_field(name="👤 Admin", value=t['admin'], inline=False)
                if t['stream']:
                    embed.add_field(name="📺 Stream", value=t['stream'], inline=False)
                
                await ctx.send(embed=embed)
                return
    
    await ctx.send("No hay carreras programadas próximamente con horario definido.")

@bot.command(name='info')
async def info(ctx, *, nombre_torneo):
    """Muestra información detallada de un torneo específico"""
    torneo = None
    for t in datos['torneos']:
        if nombre_torneo.lower() in t['nombre'].lower():
            torneo = t
            break
    
    if not torneo:
        await ctx.send(f"No se encontró el torneo '{nombre_torneo}'")
        return
    
    embed = discord.Embed(
        title=f"ℹ️ {torneo['nombre']}",
        color=discord.Color.blue()
    )
    
    embed.add_field(name="📅 Día", value=torneo['dia'], inline=True)
    embed.add_field(name="⏰ Hora", value=torneo['hora'] or "Sin definir", inline=True)
    embed.add_field(name="👤 Administrador", value=torneo['admin'] or "Sin definir", inline=False)
    
    if torneo['stream']:
        embed.add_field(name="📺 Stream", value=torneo['stream'], inline=False)
    
    if torneo['activo_desde'] or torneo['activo_hasta']:
        periodo = []
        if torneo['activo_desde']:
            periodo.append(f"Desde {torneo['activo_desde']}")
        if torneo['activo_hasta']:
            periodo.append(f"Hasta {torneo['activo_hasta']}")
        embed.add_field(name="📆 Periodo", value=" | ".join(periodo), inline=False)
    
    await ctx.send(embed=embed)

# ===== COMANDOS DE ADMINISTRACIÓN =====

@bot.command(name='actualizar')
@commands.has_permissions(administrator=True)
async def actualizar(ctx, *, args):
    """
    Actualiza información de un torneo
    Uso: !actualizar Nombre del Torneo | campo: valor
    Campos: hora, admin, stream
    Ejemplo: !actualizar Liga Canalla Prime | hora: 20:30 | admin: Juan Pérez | stream: twitch.tv/liga
    """
    try:
        partes = args.split('|')
        nombre_torneo = partes[0].strip()
        
        # Buscar torneo
        torneo = None
        for t in datos['torneos']:
            if nombre_torneo.lower() in t['nombre'].lower():
                torneo = t
                break
        
        if not torneo:
            await ctx.send(f"❌ No se encontró el torneo '{nombre_torneo}'")
            return
        
        # Actualizar campos
        for parte in partes[1:]:
            if ':' in parte:
                campo, valor = parte.split(':', 1)
                campo = campo.strip().lower()
                valor = valor.strip()
                
                if campo in ['hora', 'admin', 'stream']:
                    torneo[campo] = valor
        
        guardar_datos(datos)
        await ctx.send(f"✅ Torneo **{torneo['nombre']}** actualizado correctamente")
        
    except Exception as e:
        await ctx.send(f"❌ Error al actualizar. Uso correcto: `!actualizar Nombre del Torneo | hora: 20:30 | admin: Nombre`")

@bot.command(name='nuevo_torneo')
@commands.has_permissions(administrator=True)
async def nuevo_torneo(ctx, dia: str, *, nombre: str):
    """
    Añade un nuevo torneo
    Uso: !nuevo_torneo Lunes Liga Nueva
    """
    if dia.capitalize() not in ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']:
        await ctx.send("❌ Día inválido. Usa: Lunes, Martes, Miércoles, Jueves, Viernes, Sábado, Domingo")
        return
    
    nuevo = {
        'nombre': nombre,
        'dia': dia.capitalize(),
        'hora': None,
        'admin': None,
        'stream': None,
        'activo_desde': None,
        'activo_hasta': None
    }
    
    datos['torneos'].append(nuevo)
    guardar_datos(datos)
    await ctx.send(f"✅ Torneo **{nombre}** añadido para los {dia}")

@bot.command(name='eliminar_torneo')
@commands.has_permissions(administrator=True)
async def eliminar_torneo(ctx, *, nombre_torneo):
    """Elimina un torneo del calendario"""
    for i, t in enumerate(datos['torneos']):
        if nombre_torneo.lower() in t['nombre'].lower():
            datos['torneos'].pop(i)
            guardar_datos(datos)
            await ctx.send(f"✅ Torneo **{t['nombre']}** eliminado")
            return
    
    await ctx.send(f"❌ No se encontró el torneo '{nombre_torneo}'")

@bot.command(name='canal_recordatorios')
@commands.has_permissions(administrator=True)
async def canal_recordatorios(ctx):
    """Configura este canal para recibir recordatorios automáticos"""
    datos['canal_recordatorios'] = ctx.channel.id
    guardar_datos(datos)
    await ctx.send(f"✅ Este canal recibirá recordatorios automáticos de carreras")

# ===== SISTEMA DE RECORDATORIOS =====

@tasks.loop(minutes=30)
async def recordatorio_carreras():
    """Envía recordatorios 1 hora antes de cada carrera"""
    if not datos['canal_recordatorios']:
        return
    
    canal = bot.get_channel(datos['canal_recordatorios'])
    if not canal:
        return
    
    ahora = datetime.now()
    dia_actual = DIAS[ahora.weekday()]
    hora_actual = ahora.time()
    
    # Buscar carreras en la próxima hora
    torneos_hoy = [t for t in datos['torneos'] if t['dia'] == dia_actual and t['hora']]
    
    for t in torneos_hoy:
        try:
            hora_carrera = datetime.strptime(t['hora'], '%H:%M').time()
            diff = datetime.combine(datetime.today(), hora_carrera) - datetime.combine(datetime.today(), hora_actual)
            minutos = diff.total_seconds() / 60
            
            # Recordatorio 60 minutos antes (con margen de 15 min)
            if 45 <= minutos <= 75:
                embed = discord.Embed(
                    title="⚠️ RECORDATORIO DE CARRERA",
                    description=f"**{t['nombre']}** comienza en aproximadamente 1 hora",
                    color=discord.Color.orange()
                )
                embed.add_field(name="⏰ Hora", value=t['hora'], inline=True)
                if t['admin']:
                    embed.add_field(name="👤 Admin", value=t['admin'], inline=True)
                if t['stream']:
                    embed.add_field(name="📺 Stream", value=t['stream'], inline=False)
                
                await canal.send(embed=embed)
        except:
            continue

@bot.command(name='ayuda_bot')
async def ayuda_bot(ctx):
    """Muestra todos los comandos disponibles"""
    embed = discord.Embed(
        title="📖 Comandos del Bot de Simracing",
        description="Lista de comandos disponibles",
        color=discord.Color.purple()
    )
    
    embed.add_field(
        name="🔍 Consultas",
        value="""
        `!calendario` o `!cal` - Ver calendario completo
        `!hoy` - Ver carreras de hoy
        `!proxima` o `!pc` - Ver próxima carrera
        `!info Nombre Torneo` - Info detallada de un torneo
        """,
        inline=False
    )
    
    embed.add_field(
        name="⚙️ Administración (solo admins)",
        value="""
        `!actualizar Torneo | hora: 20:30 | admin: Nombre | stream: link`
        `!nuevo_torneo Lunes Nombre del Torneo`
        `!eliminar_torneo Nombre del Torneo`
        `!canal_recordatorios` - Activar recordatorios en este canal
        """,
        inline=False
    )
    
    await ctx.send(embed=embed)

# Manejo de errores
@actualizar.error
@nuevo_torneo.error
@eliminar_torneo.error
@canal_recordatorios.error
async def permisos_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ Solo los administradores pueden usar este comando")

# Ejecutar el bot con variable de entorno
bot.run(os.getenv('DISCORD_TOKEN'))
```

- Click en **"Commit changes"** (abajo)
- En el popup, click en **"Commit changes"** otra vez

**Archivo 2: requirements.txt**
- De vuelta en la página principal del repositorio, click en **"Add file"** → **"Create new file"**
- Nombre: `requirements.txt`
- Contenido:
```
discord.py==2.3.2
```
- Click en **"Commit changes"** → **"Commit changes"**

**Archivo 3: Procfile**
- Otra vez **"Add file"** → **"Create new file"**
- Nombre: `Procfile` (sin extensión, exactamente así)
- Contenido:
```
worker: python bot.py
```
- Click en **"Commit changes"** → **"Commit changes"**

✅ **¡GitHub listo!** Ahora vamos a Railway

---

## 🚂 PARTE 3: DESPLEGAR EN RAILWAY

**Paso 9: Crear cuenta en Railway**
- Ve a: https://railway.app
- Click en **"Login"**
- Elige **"Login with GitHub"**
- Autoriza Railway para acceder a tu cuenta de GitHub

**Paso 10: Crear nuevo proyecto**
- Click en **"New Project"**
- Selecciona **"Deploy from GitHub repo"**
- Busca y selecciona tu repositorio `bot-simracing-f1`
- Click en el repositorio para seleccionarlo

**Paso 11: Configurar variables de entorno**
- Railway comenzará a desplegar automáticamente
- Click en tu proyecto
- Click en la pestaña **"Variables"**
- Click en **"New Variable"**
- Variable name: `DISCORD_TOKEN`
- Variable value: **(pega el token que copiaste en el Paso 4)**
- Click en **"Add"**

**Paso 12: Verificar el despliegue**
- Ve a la pestaña **"Deployments"**
- Espera unos segundos, deberías ver el estado cambiar a **"SUCCESS"** con un check verde
- Click en **"View Logs"** para ver si dice: `Bot Simracing F1#1234 está conectado!`

✅ **¡BOT ACTIVO 24/7!**

---

## 🎮 PARTE 4: PROBAR EL BOT

**Paso 13: Configurar en Discord**
- Ve a tu servidor de Discord
- Verás que el bot ahora está **ONLINE** (círculo verde)
- En cualquier canal, escribe: `!ayuda_bot`
- Si responde, ¡funciona!

**Paso 14: Configurar recordatorios**
- En el canal donde quieras recibir notificaciones, escribe:
```
!canal_recordatorios
```

**Paso 15: Añadir información a las ligas**
```
!actualizar Liga Canalla Prime | hora: 20:30 | admin: NombreAdmin | stream: https://twitch.tv/canal
```

**Paso 16: Probar comandos**
```
!calendario
!hoy
!proxima
!info Liga Canalla Prime
