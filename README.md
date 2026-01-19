# 🏎️ JSQESPORTS BOT

Bot de Discord para gestión de ligas y torneos de simracing F1 25 de JSQ ESPORTS.

[![Estado](https://img.shields.io/badge/Estado-Activo-success)](https://github.com/Kadmoz/JSQESPORTS_BOT)
[![Python](https://img.shields.io/badge/Python-3.8+-blue)](https://www.python.org/)
[![discord.py](https://img.shields.io/badge/discord.py-2.0+-blue)](https://discordpy.readthedocs.io/)

---

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Comandos para Usuarios](#-comandos-para-usuarios)
- [Comandos para Administradores](#️-comandos-para-administradores)
- [Sistema de Cumpleaños](#-sistema-de-cumpleaños)
- [Campos Configurables](#-campos-configurables)
- [Ejemplos de Uso](#-ejemplos-de-uso)
- [Preguntas Frecuentes](#-preguntas-frecuentes)

---

## ✨ Características

- 📅 **Calendario semanal** de todas las ligas y torneos
- 🗓️ **Consulta por día** - Ver carreras de cualquier día de la semana
- ⏰ **Recordatorios automáticos** 1 hora antes de cada carrera y al inicio
- 🎂 **Sistema de cumpleaños** con notificaciones automáticas diarias
- 📺 **Canales separados** para recordatorios de carreras y cumpleaños
- 🔗 **Enlaces directos** a streams de cada liga
- 📞 **Información de contacto** completa (teléfono, Instagram, Twitter, Discord)
- 🎮 **Detalles técnicos** (plataforma, tipo de competencia)
- 📆 **Gestión de temporadas** con fechas de inicio y fin
- 🔄 **100% configurable** desde Discord sin tocar código
- 💾 **Persistencia de datos** - Toda la información se guarda automáticamente
- 🌍 **Zona horaria** - Configurado para Chile (America/Santiago)

---

## 👥 Comandos para Usuarios

Estos comandos pueden ser usados por **cualquier miembro** del servidor:

### 📅 Consultas de Calendario

#### `!calendario` o `!cal`
Muestra el calendario completo de la semana con todas las ligas organizadas por día.

**Ejemplo:**
```
!calendario
```

---

#### `!hoy`
Muestra únicamente las carreras programadas para el día actual.

**Ejemplo:**
```
!hoy
```

---

#### `!lunes`, `!martes`, `!miercoles`, `!jueves`, `!viernes`, `!sabado`, `!domingo`
Muestra las carreras programadas para un día específico de la semana.

**Ejemplos:**
```
!lunes
!viernes
!domingo
```

**💡 Tip:** Útil para planificar tu semana o ver qué hay un día específico sin ver todo el calendario.

---

#### `!proxima` o `!pc`
Muestra la próxima carrera que se disputará (con horario más cercano).

**Ejemplo:**
```
!proxima
```

---

### ℹ️ Información Detallada

#### `!info <Nombre de la Liga>`
Muestra toda la información detallada de una liga específica.

**Ejemplo:**
```
!info Liga Canalla Prime
```

**Información mostrada:**
- Día y hora de carrera
- Administrador y organizador
- Stream
- Redes sociales (Instagram, Twitter, Discord)
- Teléfono de contacto
- Plataforma y tipo de competencia
- Periodo de actividad
- Notas adicionales

**💡 Tip:** No necesitas escribir el nombre completo exacto. Si escribes `!info canalla`, encontrará "Liga Canalla Prime".

---

#### `!campos`
Muestra todos los campos disponibles que se pueden configurar para cada liga.

**Ejemplo:**
```
!campos
```

---

### 🎂 Cumpleaños

#### `!cumples`
Muestra la lista completa de cumpleaños registrados en el equipo, ordenados por fecha.

**Ejemplo:**
```
!cumples
```

---

### 📖 Ayuda

#### `!ayuda_bot`
Muestra un resumen de todos los comandos disponibles.

**Ejemplo:**
```
!ayuda_bot
```

---

## ⚙️ Comandos para Administradores

Estos comandos solo pueden ser usados por miembros con **permisos de administrador** en el servidor:

### 🔧 Gestión de Ligas

#### `!nuevo_torneo <Día> <Nombre de la Liga>`
Añade una nueva liga al calendario.

**Sintaxis:**
```
!nuevo_torneo <Día> <Nombre de la Liga>
```

**Días válidos:** Lunes, Martes, Miércoles, Jueves, Viernes, Sábado, Domingo

**Ejemplos:**
```
!nuevo_torneo Sábado Liga Nocturna F1
!nuevo_torneo Miércoles Campeonato Endurance
```

**Nota:** Después de crear la liga, usa `!actualizar` para añadir más información.

---

#### `!actualizar <Nombre Liga> | campo: valor | campo2: valor2`
Actualiza o añade información a una liga existente. Puedes actualizar múltiples campos a la vez separándolos con `|`.

**Sintaxis:**
```
!actualizar <Nombre de la Liga> | campo: valor | campo: valor | ...
```

**Ejemplos:**

Actualizar solo la hora:
```
!actualizar Liga Canalla Prime | hora: 20:30
```

Actualizar múltiples campos:
```
!actualizar TSL División 2 | hora: 21:00 | admin: Carlos Pérez | stream: twitch.tv/tsl
```

Ejemplo completo:
```
!actualizar Liga Canalla Prime | hora: 20:30 | admin: Juan Pérez | stream: twitch.tv/canalla | telefono: +56912345678 | instagram: @ligacanalla | discord_liga: discord.gg/canalla | plataforma: PC | tipo_competencia: Campeonato
```

---

#### `!eliminar_torneo <Nombre de la Liga>`
Elimina completamente una liga del calendario.

**Sintaxis:**
```
!eliminar_torneo <Nombre de la Liga>
```

**Ejemplo:**
```
!eliminar_torneo Liga Nocturna F1
```

⚠️ **Advertencia:** Esta acción es permanente y elimina toda la información de la liga.

---

### 🔔 Configuración de Notificaciones

#### `!canal_recordatorios`
Configura el canal actual para recibir notificaciones automáticas de carreras.

**Uso:**
1. Ve al canal donde quieres recibir las notificaciones de carreras
2. Escribe:
```
!canal_recordatorios
```

**Notificaciones enviadas:**
- ⏰ **1 hora antes** de cada carrera
- 🏁 **Al inicio** de la carrera o transmisión

---

#### `!canal_cumpleaños`
Configura el canal actual para recibir notificaciones de cumpleaños.

**Uso:**
1. Ve al canal donde quieres recibir las notificaciones de cumpleaños
2. Escribe:
```
!canal_cumpleaños
```

**Notificaciones enviadas:**
- 🎂 **Al inicio del día** con mención @everyone

**💡 Tip:** Puedes tener un canal para carreras y otro separado para cumpleaños.

---

#### `!ver_canales`
Muestra qué canales están configurados para cada tipo de notificación.

**Ejemplo:**
```
!ver_canales
```

---

### 🎂 Gestión de Cumpleaños

#### `!añadir_cumple <Nombre> | <DD/MM>`
Añade un cumpleaños a la lista.

**Sintaxis:**
```
!añadir_cumple Nombre | DD/MM
```

**Ejemplos:**
```
!añadir_cumple Kadmoz | 27/11
!añadir_cumple Juan Pérez | 15/03
```

**Notas:**
- El formato de fecha debe ser DD/MM (día/mes)
- Si el nombre ya existe, se actualizará la fecha

---

#### `!eliminar_cumple <Nombre>`
Elimina un cumpleaños de la lista.

**Ejemplo:**
```
!eliminar_cumple Kadmoz
```

---

## 📝 Campos Configurables

Estos son todos los campos que puedes configurar para cada liga usando `!actualizar`:

| Campo | Descripción | Ejemplo |
|-------|-------------|---------|
| `dia` | Día de la semana | `Lunes`, `Martes`, `Miércoles`, etc. |
| `hora` | Hora de inicio (formato 24h) | `20:30`, `21:00`, `22:15` |
| `admin` | Nombre del administrador | `Juan Pérez` |
| `organizador` | Nombre del organizador/empresa | `Canalla Racing`, `JSQ Esports` |
| `stream` | Enlace al stream | `twitch.tv/canal`, `youtube.com/@canal` |
| `telefono` | Teléfono de contacto | `+56912345678` |
| `instagram` | Usuario o enlace de Instagram | `@ligacanalla`, `instagram.com/ligacanalla` |
| `twitter` | Usuario o enlace de Twitter | `@ligacanalla`, `twitter.com/ligacanalla` |
| `discord_liga` | Enlace al Discord de la liga | `discord.gg/invitacion` |
| `plataforma` | Plataforma de juego | `PC`, `PS5`, `Xbox`, `Crossplay` |
| `tipo_competencia` | Tipo de carrera | `Sprint`, `Carrera larga`, `Campeonato` |
| `activo_desde` | Mes desde cuando está activo | `marzo`, `abril 2025` |
| `activo_hasta` | Mes hasta cuando está activo | `febrero`, `diciembre 2025` |
| `notas` | Notas adicionales | Cualquier información importante |

---

## 💡 Ejemplos de Uso

### Ejemplo 1: Usuario consultando su semana

```
Lunes por la mañana - Ver qué hay hoy:
!hoy

Planificar el fin de semana:
!sabado
!domingo

Ver cuándo es la próxima carrera:
!proxima

Revisar detalles de una liga específica:
!info Liga Canalla Prime
```

---

### Ejemplo 2: Admin configurando liga nueva

```
Paso 1: Crear la liga
!nuevo_torneo Lunes Liga Canalla Prime

Paso 2: Añadir información básica
!actualizar Liga Canalla Prime | hora: 20:30 | admin: Juan Pérez | stream: twitch.tv/canalla

Paso 3: Añadir contacto y redes sociales
!actualizar Liga Canalla Prime | telefono: +56912345678 | instagram: @ligacanalla | discord_liga: discord.gg/canalla

Paso 4: Verificar que quedó bien
!info Liga Canalla Prime
```

---

### Ejemplo 3: Admin actualizando información

```
Cambió el administrador:
!actualizar TSL División 2 | admin: Carlos Rodríguez

Cambió la hora y el stream:
!actualizar TSL División 2 | hora: 21:30 | stream: youtube.com/@tsl

Nueva liga temporal (verano):
!nuevo_torneo Martes EDR Summer
!actualizar EDR Summer | activo_hasta: febrero | hora: 20:00
```

---

### Ejemplo 4: Admin configurando notificaciones

```
Paso 1: Configurar canal de carreras
(En el canal #carreras)
!canal_recordatorios

Paso 2: Configurar canal de cumpleaños
(En el canal #celebraciones)
!canal_cumpleaños

Paso 3: Verificar configuración
!ver_canales

Paso 4: Añadir cumpleaños del equipo
!añadir_cumple Juan | 15/03
!añadir_cumple María | 22/07
!añadir_cumple Carlos | 10/11
```

---

### Ejemplo 5: Gestión de temporadas

```
Liga que termina en febrero:
!actualizar EDR Summer | activo_hasta: febrero

Liga que empieza en marzo:
!actualizar EDR División F1 Nitro | activo_desde: marzo

Liga con periodo específico:
!actualizar MRS Winter | activo_desde: junio | activo_hasta: agosto
```

---

## ❓ Preguntas Frecuentes

### ¿Cómo veo las carreras de un día específico?
Usa el comando del día correspondiente: `!lunes`, `!martes`, `!miercoles`, `!jueves`, `!viernes`, `!sabado`, o `!domingo`.

### ¿El bot funciona 24/7?
Sí, el bot está alojado en un servidor dedicado y está configurado para estar siempre activo.

### ¿Cómo funcionan los recordatorios automáticos?
El bot revisa cada 30 minutos si hay carreras próximas y envía:
- **1 hora antes**: Recordatorio preventivo
- **Al inicio**: Alerta cuando la carrera está comenzando

### ¿Puedo tener canales separados para carreras y cumpleaños?
Sí, puedes configurar canales independientes:
- `!canal_recordatorios` para carreras
- `!canal_cumpleaños` para cumpleaños
- `!ver_canales` para verificar

### ¿Qué pasa si escribo mal el nombre de una liga?
El bot busca coincidencias parciales. Por ejemplo, `!info canalla` encontrará "Liga Canalla Prime".

### ¿Los datos se pierden si el bot se reinicia?
No, toda la información se guarda automáticamente y persiste entre reinicios.

### ¿Puedo ver solo las carreras del viernes?
Sí, usa `!viernes` para ver únicamente las carreras de ese día.

### ¿Cómo sé qué campos puedo configurar?
Usa `!campos` para ver la lista completa de campos disponibles con ejemplos.

### ¿Qué zona horaria usa el bot?
El bot usa la zona horaria de Chile (America/Santiago), incluyendo horario de verano automáticamente.

### ¿Puedo sugerir nuevas funciones?
Sí, contacta a los administradores del equipo con tus sugerencias.

---

## 🚀 Inicio Rápido

### Para usuarios:
```
!ayuda_bot          → Ver todos los comandos
!calendario         → Ver calendario completo
!hoy               → Carreras de hoy
!viernes           → Carreras del viernes
!proxima           → Próxima carrera
!info <nombre>     → Detalles de una liga
!cumples           → Ver cumpleaños
```

### Para administradores:
```
!canal_recordatorios           → Configurar notificaciones de carreras
!canal_cumpleaños             → Configurar notificaciones de cumpleaños
!ver_canales                  → Verificar configuración
!nuevo_torneo Dia Nombre      → Crear nueva liga
!actualizar Liga | campo: valor → Actualizar información
!campos                       → Ver campos disponibles
!añadir_cumple Nombre | DD/MM → Añadir cumpleaños
```

---

## 📞 Soporte

Si encuentras algún problema:

1. **Comandos:** Verifica el formato con `!ayuda_bot`
2. **Bot offline:** Verifica que el bot esté ONLINE (círculo verde)
3. **Permisos:** Solo admins pueden configurar
4. **Otros:** Contacta al equipo de JSQ

---

## 🏆 Créditos

**Desarrollado por:** JSQ_KADMOZ  
**Para:** JSQ ESPORTS  
**Versión:** 3.0  
**Última actualización:** 19 Enero 2026

---

¡Disfruta del bot y buenas carreras! 🏁🏎️
