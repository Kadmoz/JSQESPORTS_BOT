import discord
from discord.ext import commands, tasks
from datetime import datetime, timedelta
import json
import os
import pytz
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración del bot
CHILE_TZ = pytz.timezone('America/Santiago')
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
            datos_cargados = json.load(f)
            # Asegurar que existan las nuevas claves
            if 'cumpleaños' not in datos_cargados:
                datos_cargados['cumpleaños'] = []
            if 'canal_cumpleaños' not in datos_cargados:
                datos_cargados['canal_cumpleaños'] = None
            if 'canal_comandos' not in datos_cargados:
                datos_cargados['canal_comandos'] = None
            return datos_cargados
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
            'canal_recordatorios': None,
            'canal_cumpleaños': None,
            'canal_comandos': None,
            'cumpleaños': []
        }

def guardar_datos(datos):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)

datos = cargar_datos()

@bot.event
async def on_ready():
    print(f'{bot.user} está conectado!')
    recordatorio_carreras.start()
    verificar_cumpleaños.start()

# ===== COMANDOS DE CONSULTA =====

def solo_canal_comandos():
    """Decorador para restringir comandos al canal configurado"""
    async def predicate(ctx):
        # Si no hay canal configurado, permitir en cualquier lado
        if not datos.get('canal_comandos'):
            return True
        # Si hay canal configurado, solo permitir ahí
        return ctx.channel.id == datos.get('canal_comandos')
    return commands.check(predicate)

@bot.command(name='calendario', aliases=['cal'])
@solo_canal_comandos()
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
@solo_canal_comandos()
async def hoy(ctx):
    """Muestra las carreras de hoy"""
    dia_actual = DIAS[datetime.now(CHILE_TZ).weekday()]
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

@bot.command(name='lunes')
@solo_canal_comandos()
async def lunes(ctx):
    """Muestra las carreras del lunes"""
    await mostrar_carreras_dia(ctx, 'Lunes')

@bot.command(name='martes')
@solo_canal_comandos()
async def martes(ctx):
    """Muestra las carreras del martes"""
    await mostrar_carreras_dia(ctx, 'Martes')

@bot.command(name='miercoles')
@solo_canal_comandos()
async def miercoles(ctx):
    """Muestra las carreras del miércoles"""
    await mostrar_carreras_dia(ctx, 'Miércoles')

@bot.command(name='jueves')
@solo_canal_comandos()
async def jueves(ctx):
    """Muestra las carreras del jueves"""
    await mostrar_carreras_dia(ctx, 'Jueves')

@bot.command(name='viernes')
@solo_canal_comandos()
async def viernes(ctx):
    """Muestra las carreras del viernes"""
    await mostrar_carreras_dia(ctx, 'Viernes')

@bot.command(name='sabado')
@solo_canal_comandos()
async def sabado(ctx):
    """Muestra las carreras del sábado"""
    await mostrar_carreras_dia(ctx, 'Sábado')

@bot.command(name='domingo')
@solo_canal_comandos()
async def domingo(ctx):
    """Muestra las carreras del domingo"""
    await mostrar_carreras_dia(ctx, 'Domingo')

async def mostrar_carreras_dia(ctx, dia):
    """Función auxiliar para mostrar carreras de un día específico"""
    torneos_dia = [t for t in datos['torneos'] if t.get('dia') == dia]
    
    if not torneos_dia:
        await ctx.send(f"No hay carreras programadas para el {dia} 😢")
        return
    
    embed = discord.Embed(
        title=f"🏎️ Carreras del {dia}",
        color=discord.Color.blue()
    )
    
    for t in torneos_dia:
        info = []
        if t.get('hora'):
            info.append(f"**Hora:** {t['hora']}")
        if t.get('admin'):
            info.append(f"**Admin:** {t['admin']}")
        if t.get('stream'):
            info.append(f"**Stream:** {t['stream']}")
        if t.get('activo_desde') or t.get('activo_hasta'):
            periodo = []
            if t.get('activo_desde'):
                periodo.append(f"desde {t['activo_desde']}")
            if t.get('activo_hasta'):
                periodo.append(f"hasta {t['activo_hasta']}")
            info.append(f"📅 {' '.join(periodo)}")
        
        valor = "\n".join(info) if info else "Información pendiente"
        embed.add_field(name=t['nombre'], value=valor, inline=False)
    
    await ctx.send(embed=embed)

@bot.command(name='proxima', aliases=['pc'])
@solo_canal_comandos()
async def proxima(ctx):
    """Muestra la próxima carrera"""
    ahora = datetime.now(CHILE_TZ)
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
@solo_canal_comandos()
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
    """Configura este canal para recibir recordatorios automáticos de carreras"""
    datos['canal_recordatorios'] = ctx.channel.id
    guardar_datos(datos)
    await ctx.send(f"✅ Este canal recibirá recordatorios automáticos de carreras")

@bot.command(name='canal_cumpleaños')
@commands.has_permissions(administrator=True)
async def canal_cumpleanos(ctx):
    """Configura este canal para recibir notificaciones de cumpleaños"""
    datos['canal_cumpleaños'] = ctx.channel.id
    guardar_datos(datos)
    await ctx.send(f"✅ Este canal recibirá notificaciones de cumpleaños 🎂")

@bot.command(name='canal_comandos')
@commands.has_permissions(administrator=True)
async def canal_comandos(ctx):
    """Configura este canal como el único donde funcionan los comandos de consulta"""
    datos['canal_comandos'] = ctx.channel.id
    guardar_datos(datos)
    await ctx.send(f"✅ Los comandos de torneos solo funcionarán en este canal 🏎️\nPara desactivar la restricción, usa `!desactivar_restriccion`")

@bot.command(name='desactivar_restriccion')
@commands.has_permissions(administrator=True)
async def desactivar_restriccion(ctx):
    """Permite usar comandos de consulta en cualquier canal"""
    datos['canal_comandos'] = None
    guardar_datos(datos)
    await ctx.send(f"✅ Los comandos de torneos ahora funcionan en cualquier canal")

@bot.command(name='ver_canales')
@commands.has_permissions(administrator=True)
async def ver_canales(ctx):
    """Muestra qué canales están configurados para notificaciones"""
    embed = discord.Embed(
        title="📺 Canales Configurados",
        color=discord.Color.blue()
    )
    
    # Canal de recordatorios de carreras
    if datos.get('canal_recordatorios'):
        canal_carreras = bot.get_channel(datos['canal_recordatorios'])
        nombre_carreras = canal_carreras.mention if canal_carreras else "Canal no encontrado"
    else:
        nombre_carreras = "No configurado"
    
    embed.add_field(
        name="🏎️ Recordatorios de Carreras",
        value=nombre_carreras,
        inline=False
    )
    
    # Canal de cumpleaños
    if datos.get('canal_cumpleaños'):
        canal_cumples = bot.get_channel(datos['canal_cumpleaños'])
        nombre_cumples = canal_cumples.mention if canal_cumples else "Canal no encontrado"
    else:
        nombre_cumples = "No configurado"
    
    embed.add_field(
        name="🎂 Cumpleaños",
        value=nombre_cumples,
        inline=False
    )
    
    # Canal de comandos
    if datos.get('canal_comandos'):
        canal_comandos = bot.get_channel(datos['canal_comandos'])
        nombre_comandos = canal_comandos.mention if canal_comandos else "Canal no encontrado"
    else:
        nombre_comandos = "Sin restricción (funciona en todos)"
    
    embed.add_field(
        name="🏎️ Canal de Comandos",
        value=nombre_comandos,
        inline=False
    )
    
    await ctx.send(embed=embed)

@bot.command(name='cumples')
async def cumples(ctx):
    """Muestra la lista de cumpleaños"""
    if not datos.get('cumpleaños'):
        await ctx.send("🎂 No hay cumpleaños registrados.")
        return
    
    embed = discord.Embed(
        title="🎂 Cumpleaños del Equipo",
        color=discord.Color.fuchsia()
    )
    
    # Ordenar por mes y día
    lista_ordenada = sorted(datos['cumpleaños'], key=lambda x: (int(x['fecha'].split('/')[1]), int(x['fecha'].split('/')[0])))
    
    texto = ""
    for c in lista_ordenada:
        texto += f"**{c['nombre']}** - {c['fecha']}\n"
    
    embed.description = texto
    await ctx.send(embed=embed)

@bot.command(name='proximo_cumple', aliases=['proximo_cumpleaños', 'pc_cumple'])
async def proximo_cumple(ctx):
    """Muestra el próximo cumpleaños"""
    if not datos.get('cumpleaños'):
        await ctx.send("🎂 No hay cumpleaños registrados.")
        return
    
    hoy = datetime.now(CHILE_TZ)
    
    # Calcular días hasta cada cumpleaños
    proximos = []
    for c in datos['cumpleaños']:
        dia, mes = map(int, c['fecha'].split('/'))
        
        # Crear fecha del cumpleaños este año
        try:
            cumple_este_año = datetime(hoy.year, mes, dia, tzinfo=CHILE_TZ)
        except ValueError:
            # Fecha inválida (ej: 29 feb en año no bisiesto)
            continue
        
        # Si ya pasó este año, usar el próximo año
        if cumple_este_año.date() < hoy.date():
            try:
                cumple_este_año = datetime(hoy.year + 1, mes, dia, tzinfo=CHILE_TZ)
            except ValueError:
                continue
        
        dias_faltantes = (cumple_este_año.date() - hoy.date()).days
        proximos.append({
            'nombre': c['nombre'],
            'fecha': c['fecha'],
            'dias': dias_faltantes,
            'fecha_completa': cumple_este_año
        })
    
    if not proximos:
        await ctx.send("🎂 No hay cumpleaños próximos.")
        return
    
    # Ordenar por días faltantes
    proximos.sort(key=lambda x: x['dias'])
    proximo = proximos[0]
    
    embed = discord.Embed(
        title="🎂 Próximo Cumpleaños",
        color=discord.Color.gold()
    )
    
    embed.add_field(name="👤 Nombre", value=proximo['nombre'], inline=True)
    embed.add_field(name="📅 Fecha", value=proximo['fecha'], inline=True)
    
    if proximo['dias'] == 0:
        embed.add_field(name="⏰ Cuándo", value="¡Hoy! 🎉", inline=False)
        embed.set_footer(text="¡Feliz cumpleaños! 🎊")
    elif proximo['dias'] == 1:
        embed.add_field(name="⏰ Cuándo", value="Mañana", inline=False)
    else:
        embed.add_field(name="⏰ Cuándo", value=f"En {proximo['dias']} días", inline=False)
    
    # Mostrar también los siguientes 2 cumpleaños si hay
    if len(proximos) > 1:
        siguientes = []
        for p in proximos[1:3]:
            if p['dias'] == 0:
                cuando = "Hoy"
            elif p['dias'] == 1:
                cuando = "Mañana"
            else:
                cuando = f"En {p['dias']} días"
            siguientes.append(f"**{p['nombre']}** ({p['fecha']}) - {cuando}")
        
        if siguientes:
            embed.add_field(
                name="📋 Siguientes cumpleaños",
                value="\n".join(siguientes),
                inline=False
            )
    
    await ctx.send(embed=embed)

@bot.command(name='añadir_cumple')
@commands.has_permissions(administrator=True)
async def añadir_cumple(ctx, *, args):
    """Añade un cumpleaños. Uso: !añadir_cumple Nombre | DD/MM"""
    try:
        nombre, fecha = [x.strip() for x in args.split('|')]
        # Validar formato fecha
        datetime.strptime(fecha, '%d/%m')
        
        # Eliminar si ya existe para actualizar
        datos['cumpleaños'] = [c for c in datos['cumpleaños'] if c['nombre'].lower() != nombre.lower()]
        
        datos['cumpleaños'].append({'nombre': nombre, 'fecha': fecha})
        guardar_datos(datos)
        await ctx.send(f"✅ Cumpleaños de **{nombre}** ({fecha}) guardado.")
    except:
        await ctx.send("❌ Formato incorrecto. Usa: `!añadir_cumple Nombre | DD/MM`")

@bot.command(name='eliminar_cumple')
@commands.has_permissions(administrator=True)
async def eliminar_cumple(ctx, *, nombre):
    """Elimina un cumpleaños"""
    original_len = len(datos['cumpleaños'])
    datos['cumpleaños'] = [c for c in datos['cumpleaños'] if c['nombre'].lower() != nombre.lower()]
    
    if len(datos['cumpleaños']) < original_len:
        guardar_datos(datos)
        await ctx.send(f"✅ Cumpleaños de **{nombre}** eliminado.")
    else:
        await ctx.send(f"❌ No se encontró a **{nombre}**.")

# ===== SISTEMA DE RECORDATORIOS =====

@tasks.loop(minutes=30)
async def recordatorio_carreras():
    """Envía recordatorios 1 hora antes de cada carrera"""
    if not datos.get('canal_recordatorios'):
        return
    
    canal = bot.get_channel(datos['canal_recordatorios'])
    if not canal:
        return
    
    ahora = datetime.now(CHILE_TZ)
    dia_actual = DIAS[ahora.weekday()]
    hora_actual = ahora.time()
    
    # Buscar carreras en la próxima hora
    torneos_hoy = [t for t in datos['torneos'] if t.get('dia') == dia_actual and t.get('hora')]
    
    for t in torneos_hoy:
        try:
            hora_carrera = datetime.strptime(t['hora'], '%H:%M').time()
            # Combinar con fecha actual en Chile para cálculo correcto
            fecha_hoy_chile = ahora.date()
            dt_carrera = CHILE_TZ.localize(datetime.combine(fecha_hoy_chile, hora_carrera))
            
            diff = dt_carrera - ahora
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

            # Alerta de Inicio de Carrera / Transmisión (entre -5 y 25 minutos de la hora fijada)
            elif -5 <= minutos <= 25:
                embed = discord.Embed(
                    title="🏎️ ¡CARRERA INICIANDO!",
                    description=f"La carrera **{t['nombre']}** está por comenzar o ya ha iniciado.",
                    color=discord.Color.red()
                )
                embed.add_field(name="⏰ Hora Programada", value=t['hora'], inline=True)
                
                if t.get('stream'):
                    embed.add_field(name="📺 Ver Transmisión", value=f"[Haz clic aquí para ver en vivo]({t['stream']})", inline=False)
                
                if t.get('admin'):
                    embed.add_field(name="👤 Admin", value=t['admin'], inline=True)
                
                await canal.send(embed=embed)
        except:
            continue

@tasks.loop(hours=24)
async def verificar_cumpleaños():
    """Verifica si hoy es el cumpleaños de alguien"""
    # Usar el canal específico de cumpleaños si está configurado, sino usar el de recordatorios
    canal_id = datos.get('canal_cumpleaños') or datos.get('canal_recordatorios')
    
    if not canal_id:
        return
    
    canal = bot.get_channel(canal_id)
    if not canal:
        return
    
    hoy_str = datetime.now(CHILE_TZ).strftime('%d/%m')
    cumpleañeros = [c['nombre'] for c in datos['cumpleaños'] if c['fecha'] == hoy_str]
    
    if cumpleañeros:
        nombres = " y ".join(cumpleañeros)
        embed = discord.Embed(
            title="🎂 ¡FELIZ CUMPLEAÑOS!",
            description=f"Hoy celebramos el cumpleaños de: **{nombres}** 🎉",
            color=discord.Color.random()
        )
        embed.set_thumbnail(url="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNHJndnZndnZndnZndnZndnZndnZndnZndnZndnZndnZndnZndmcmImZXA9djFfaW50ZXJuYWxfZ2lmX2J5X2lkJmN0PWc/3o7TKSjP9pL6W1XUf6/giphy.gif")
        await canal.send(content="@everyone" if len(cumpleañeros) > 0 else "", embed=embed)

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
        `!lunes`, `!martes`, `!miercoles`, `!jueves`, `!viernes`, `!sabado`, `!domingo` - Carreras de un día específico
        `!proxima` o `!pc` - Ver próxima carrera
        `!info Nombre Torneo` - Info detallada de un torneo
        `!campos` - Ver campos configurables
        `!cumples` - Ver lista de cumpleaños
        `!proximo_cumple` o `!pc_cumple` - Ver próximo cumpleaños
        """,
        inline=False
    )
    
    embed.add_field(
        name="⚙️ Administración (solo admins)",
        value="""
        `!actualizar Torneo | campo: valor`
        `!nuevo_torneo Lunes Nombre del Torneo`
        `!eliminar_torneo Nombre del Torneo`
        `!canal_recordatorios` - Activar recordatorios de carreras
        `!canal_cumpleaños` - Activar notificaciones de cumpleaños
        `!canal_comandos` - Restringir comandos a un canal
        `!desactivar_restriccion` - Permitir comandos en todos los canales
        `!ver_canales` - Ver canales configurados
        `!añadir_cumple Nombre | DD/MM` - Añadir cumpleaños
        `!eliminar_cumple Nombre` - Eliminar cumpleaños
        """,
        inline=False
    )
    
    await ctx.send(embed=embed)

# Manejo de errores
@actualizar.error
@nuevo_torneo.error
@eliminar_torneo.error
@canal_recordatorios.error
@canal_cumpleanos.error
@canal_comandos.error
@desactivar_restriccion.error
@ver_canales.error
async def permisos_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ Solo los administradores pueden usar este comando")
    elif isinstance(error, commands.CheckFailure):
        if datos.get('canal_comandos'):
            canal = bot.get_channel(datos['canal_comandos'])
            if canal:
                await ctx.send(f"❌ Este comando solo puede usarse en {canal.mention}")
            else:
                await ctx.send("❌ Este comando está restringido a un canal específico")

# Ejecutar el bot con variable de entorno
bot.run(os.getenv('DISCORD_TOKEN'))
