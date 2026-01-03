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

# Campos configurables disponibles
CAMPOS_DISPONIBLES = [
    'hora', 'admin', 'stream', 'telefono', 'instagram', 
    'twitter', 'discord_liga', 'organizador', 'tipo_competencia',
    'plataforma', 'notas', 'activo_desde', 'activo_hasta'
]

# Estructura inicial de datos
def cargar_datos():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        return {
            'torneos': [
                {'nombre': 'Liga Canalla Prime', 'dia': 'Lunes'},
                {'nombre': 'EDR División F1 Nitro', 'dia': 'Lunes', 'activo_desde': 'marzo'},
                {'nombre': 'TSL División 2', 'dia': 'Martes'},
                {'nombre': 'EDR Summer', 'dia': 'Martes', 'activo_hasta': 'febrero'},
                {'nombre': 'EDR División F1 Hyper', 'dia': 'Martes', 'activo_desde': 'marzo'},
                {'nombre': 'Liga Canalla Elite', 'dia': 'Martes'},
                {'nombre': 'TSL División 1', 'dia': 'Miércoles'},
                {'nombre': 'MRS Summer', 'dia': 'Miércoles', 'activo_hasta': 'febrero'},
                {'nombre': 'Liga del Pescador División Racing', 'dia': 'Miércoles'},
                {'nombre': 'MRS Summer', 'dia': 'Jueves', 'activo_hasta': 'febrero'},
                {'nombre': 'MRS División 1', 'dia': 'Jueves', 'activo_desde': 'marzo'},
                {'nombre': 'Liga Prime Time', 'dia': 'Viernes'}
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
        torneos_dia = [t for t in datos['torneos'] if t.get('dia') == dia]
        if torneos_dia:
            texto = ""
            for t in torneos_dia:
                info_extra = []
                if t.get('hora'):
                    info_extra.append(f"⏰ {t['hora']}")
                if t.get('admin'):
                    info_extra.append(f"👤 {t['admin']}")
                if t.get('activo_desde') or t.get('activo_hasta'):
                    periodo = []
                    if t.get('activo_desde'):
                        periodo.append(f"desde {t['activo_desde']}")
                    if t.get('activo_hasta'):
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
    torneos_hoy = [t for t in datos['torneos'] if t.get('dia') == dia_actual]
    
    if not torneos_hoy:
        await ctx.send(f"No hay carreras programadas para hoy ({dia_actual}) 😢")
        return
    
    embed = discord.Embed(
        title=f"🏁 Carreras de Hoy - {dia_actual}",
        color=discord.Color.green()
    )
    
    for t in torneos_hoy:
        info = []
        if t.get('hora'):
            info.append(f"**Hora:** {t['hora']}")
        if t.get('admin'):
            info.append(f"**Admin:** {t['admin']}")
        if t.get('stream'):
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
        torneos_dia = [t for t in datos['torneos'] if t.get('dia') == dia_buscar and t.get('hora')]
        
        if torneos_dia:
            # Ordenar por hora
            torneos_dia.sort(key=lambda x: x.get('hora', '99:99'))
            
            for t in torneos_dia:
                if i == 0:  # Hoy
                    try:
                        hora_carrera = datetime.strptime(t['hora'], '%H:%M').time()
                        if hora_carrera <= ahora.time():
                            continue
                    except:
                        pass
                
                embed = discord.Embed(
                    title="🏎️ Próxima Carrera",
                    description=f"**{t['nombre']}**",
                    color=discord.Color.gold()
                )
                embed.add_field(name="📅 Día", value=t['dia'], inline=True)
                embed.add_field(name="⏰ Hora", value=t['hora'], inline=True)
                
                if t.get('admin'):
                    embed.add_field(name="👤 Admin", value=t['admin'], inline=False)
                if t.get('stream'):
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
    
    # Información básica
    embed.add_field(name="📅 Día", value=torneo.get('dia', 'Sin definir'), inline=True)
    embed.add_field(name="⏰ Hora", value=torneo.get('hora', 'Sin definir'), inline=True)
    
    # Admin y organizador
    if torneo.get('admin'):
        embed.add_field(name="👤 Administrador", value=torneo['admin'], inline=False)
    if torneo.get('organizador'):
        embed.add_field(name="🏢 Organizador", value=torneo['organizador'], inline=False)
    
    # Stream
    if torneo.get('stream'):
        embed.add_field(name="📺 Stream", value=torneo['stream'], inline=False)
    
    # Redes sociales
    redes = []
    if torneo.get('instagram'):
        redes.append(f"📸 Instagram: {torneo['instagram']}")
    if torneo.get('twitter'):
        redes.append(f"🐦 Twitter: {torneo['twitter']}")
    if torneo.get('discord_liga'):
        redes.append(f"💬 Discord: {torneo['discord_liga']}")
    if redes:
        embed.add_field(name="🌐 Redes Sociales", value="\n".join(redes), inline=False)
    
    # Contacto
    if torneo.get('telefono'):
        embed.add_field(name="📞 Teléfono", value=torneo['telefono'], inline=True)
    
    # Detalles técnicos
    if torneo.get('plataforma'):
        embed.add_field(name="🎮 Plataforma", value=torneo['plataforma'], inline=True)
    if torneo.get('tipo_competencia'):
        embed.add_field(name="🏆 Tipo", value=torneo['tipo_competencia'], inline=True)
    
    # Periodo
    if torneo.get('activo_desde') or torneo.get('activo_hasta'):
        periodo = []
        if torneo.get('activo_desde'):
            periodo.append(f"Desde {torneo['activo_desde']}")
        if torneo.get('activo_hasta'):
            periodo.append(f"Hasta {torneo['activo_hasta']}")
        embed.add_field(name="📆 Periodo", value=" | ".join(periodo), inline=False)
    
    # Notas
    if torneo.get('notas'):
        embed.add_field(name="📝 Notas", value=torneo['notas'], inline=False)
    
    await ctx.send(embed=embed)

@bot.command(name='campos')
async def campos(ctx):
    """Muestra todos los campos disponibles para configurar"""
    embed = discord.Embed(
        title="📋 Campos Disponibles para Configurar",
        description="Estos son todos los campos que puedes añadir a cada torneo:",
        color=discord.Color.purple()
    )
    
    campos_info = {
        'dia': '📅 Día de la semana',
        'hora': '⏰ Hora de inicio (formato 24h: 20:30)',
        'admin': '👤 Nombre del administrador',
        'organizador': '🏢 Nombre del organizador/empresa',
        'stream': '📺 Enlace al stream (Twitch, YouTube, etc)',
        'telefono': '📞 Teléfono de contacto',
        'instagram': '📸 Usuario o enlace de Instagram',
        'twitter': '🐦 Usuario o enlace de Twitter',
        'discord_liga': '💬 Enlace al Discord de la liga',
        'plataforma': '🎮 Plataforma (PC, PS5, Xbox, etc)',
        'tipo_competencia': '🏆 Tipo (Sprint, Carrera larga, Campeonato, etc)',
        'activo_desde': '📅 Mes desde cuando está activo',
        'activo_hasta': '📅 Mes hasta cuando está activo',
        'notas': '📝 Notas adicionales o información importante'
    }
    
    texto = ""
    for campo, descripcion in campos_info.items():
        texto += f"**{campo}**: {descripcion}\n"
    
    embed.add_field(name="Campos", value=texto, inline=False)
    embed.add_field(
        name="💡 Ejemplo de uso",
        value="`!actualizar Liga Canalla | hora: 20:30 | instagram: @ligacanalla | telefono: +56912345678`",
        inline=False
    )
    
    await ctx.send(embed=embed)

# ===== COMANDOS DE ADMINISTRACIÓN =====

@bot.command(name='actualizar')
@commands.has_permissions(administrator=True)
async def actualizar(ctx, *, args):
    """
    Actualiza información de un torneo
    Uso: !actualizar Nombre del Torneo | campo: valor | campo2: valor2
    Para ver todos los campos disponibles: !campos
    Ejemplo: !actualizar Liga Canalla Prime | hora: 20:30 | admin: Juan | stream: twitch.tv/liga | telefono: +56912345678
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
        campos_actualizados = []
        for parte in partes[1:]:
            if ':' in parte:
                campo, valor = parte.split(':', 1)
                campo = campo.strip().lower()
                valor = valor.strip()
                
                # Validar que el campo existe
                if campo == 'dia':
                    if valor.capitalize() not in ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']:
                        await ctx.send(f"❌ Día inválido: {valor}. Usa: Lunes, Martes, Miércoles, etc.")
                        continue
                    valor = valor.capitalize()
                
                torneo[campo] = valor
                campos_actualizados.append(campo)
        
        guardar_datos(datos)
        
        if campos_actualizados:
            await ctx.send(f"✅ Torneo **{torneo['nombre']}** actualizado\nCampos modificados: {', '.join(campos_actualizados)}")
        else:
            await ctx.send(f"⚠️ No se actualizó ningún campo. Verifica el formato: `campo: valor`")
        
    except Exception as e:
        await ctx.send(f"❌ Error al actualizar. Uso correcto: `!actualizar Nombre del Torneo | campo: valor`")

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
        'dia': dia.capitalize()
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
    if not datos.get('canal_recordatorios'):
        return
    
    canal = bot.get_channel(datos['canal_recordatorios'])
    if not canal:
        return
    
    ahora = datetime.now()
    dia_actual = DIAS[ahora.weekday()]
    hora_actual = ahora.time()
    
    # Buscar carreras en la próxima hora
    torneos_hoy = [t for t in datos['torneos'] if t.get('dia') == dia_actual and t.get('hora')]
    
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
                if t.get('admin'):
                    embed.add_field(name="👤 Admin", value=t['admin'], inline=True)
                if t.get('stream'):
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
        `!campos` - Ver campos configurables
        """,
        inline=False
    )
    
    embed.add_field(
        name="⚙️ Administración (solo admins)",
        value="""
        `!actualizar Torneo | campo: valor`
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
