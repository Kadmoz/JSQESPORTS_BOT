# JSQESPORTS_BOT
Bot para manejo de ligas de JSQ ESPORTS en discord

---

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Comandos para Usuarios](#-comandos-para-usuarios)
- [Comandos para Administradores](#️-comandos-para-administradores)
- [Campos Configurables](#-campos-configurables)
- [Ejemplos de Uso](#-ejemplos-de-uso)
- [Preguntas Frecuentes](#-preguntas-frecuentes)

---

## ✨ Características

- 📅 **Calendario semanal** de todas las ligas y torneos
- ⏰ **Recordatorios automáticos** 1 hora antes de cada carrera
- 📺 **Enlaces directos** a streams de cada liga
- 📞 **Información de contacto** completa (teléfono, Instagram, Twitter, Discord)
- 🎮 **Detalles técnicos** (plataforma, tipo de competencia)
- 🔄 **100% configurable** desde Discord sin tocar código
- 💾 **Persistencia de datos** - Toda la información se guarda automáticamente

---

## 👥 Comandos para Usuarios

Estos comandos pueden ser usados por **cualquier miembro** del servidor:

### `!calendario` o `!cal`
Muestra el calendario completo de la semana con todas las ligas organizadas por día.

**Ejemplo:**
```
!calendario
```

**Resultado:**
- Muestra todas las ligas de Lunes a Domingo
- Incluye hora, admin y periodo de actividad si están configurados

---

### `!hoy`
Muestra únicamente las carreras programadas para el día actual.

**Ejemplo:**
```
!hoy
```

**Resultado:**
- Lista de carreras del día
- Hora de inicio
- Administrador
- Enlace al stream (si está disponible)

---

### `!proxima` o `!pc`
Muestra la próxima carrera que se disputará (con horario más cercano).

**Ejemplo:**
```
!proxima
```

**Resultado:**
- Nombre de la liga
- Día y hora
- Administrador y stream

---

### `!info <Nombre de la Liga>`
Muestra toda la información detallada de una liga específica.

**Ejemplo:**
```
!info Liga Canalla Prime
```

**Resultado:**
- Día y hora de carrera
- Administrador y organizador
- Stream
- Redes sociales (Instagram, Twitter, Discord)
- Teléfono de contacto
- Plataforma y tipo de competencia
- Periodo de actividad
- Notas adicionales

---

### `!campos`
Muestra todos los campos disponibles que se pueden configurar para cada liga.

**Ejemplo:**
```
!campos
```

---

### `!ayuda_bot`
Muestra un resumen de todos los comandos disponibles.

**Ejemplo:**
```
!ayuda_bot
```

---

## ⚙️ Comandos para Administradores

Estos comandos solo pueden ser usados por miembros con **permisos de administrador** en el servidor:

### `!actualizar <Nombre Liga> | campo: valor | campo2: valor2`
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
!actualizar TSL División 2 | hora: 21:00 | admin: Carlos Pérez | stream: twitch.tv/tsl_chile
```

Ejemplo completo con todos los campos:
```
!actualizar Liga Canalla Prime | hora: 20:30 | admin: Juan Pérez | organizador: Canalla Racing | stream: twitch.tv/canalla | telefono: +56912345678 | instagram: @ligacanalla | twitter: @ligacanalla | discord_liga: discord.gg/canalla | plataforma: PC | tipo_competencia: Campeonato | notas: Requiere registro previo en la web
```

---

### `!nuevo_torneo <Día> <Nombre de la Liga>`
Añade una nueva liga al calendario.

**Sintaxis:**
```
!nuevo_torneo <Día> <Nombre de la Liga>
```

**Días válidos:** Lunes, Martes, Miércoles, Jueves, Viernes, Sábado, Domingo

**Ejemplos:**
```
!nuevo_torneo Sábado Liga Nocturna F1
```

```
!nuevo_torneo Miércoles Campeonato Endurance
```

**Nota:** Después de crear la liga, usa `!actualizar` para añadir más información.

---

### `!eliminar_torneo <Nombre de la Liga>`
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

### `!borrar_campo <"Nombre Liga"> <campo>`
Elimina un campo específico de una liga (por ejemplo, si quieres borrar el teléfono pero mantener todo lo demás).

**Sintaxis:**
```
!borrar_campo "<Nombre de la Liga>" <campo>
```

**Ejemplos:**
```
!borrar_campo "Liga Canalla Prime" telefono
```

```
!borrar_campo "TSL División 2" instagram
```

---

### `!canal_recordatorios`
Configura el canal actual para recibir notificaciones automáticas 1 hora antes de cada carrera.

**Uso:**
1. Ve al canal donde quieres recibir las notificaciones
2. Escribe:
```
!canal_recordatorios
```

**Resultado:**
- El bot enviará recordatorios automáticos en ese canal
- Los recordatorios se envían 1 hora antes de cada carrera con horario configurado
- Solo puede haber un canal de recordatorios activo a la vez

---

## 📝 Campos Configurables

Estos son todos los campos que puedes configurar para cada liga:

| Campo | Descripción | Ejemplo |
|-------|-------------|---------|
| `dia` | Día de la semana | `Lunes`, `Martes`, etc. |
| `hora` | Hora de inicio (formato 24h) | `20:30`, `21:00` |
| `admin` | Nombre del administrador | `Juan Pérez` |
| `organizador` | Nombre del organizador/empresa | `Canalla Racing` |
| `stream` | Enlace al stream | `twitch.tv/canal` o `youtube.com/watch?v=...` |
| `telefono` | Teléfono de contacto | `+56912345678` |
| `instagram` | Usuario o enlace de Instagram | `@ligacanalla` o `instagram.com/ligacanalla` |
| `twitter` | Usuario o enlace de Twitter | `@ligacanalla` o `twitter.com/ligacanalla` |
| `discord_liga` | Enlace al Discord de la liga | `discord.gg/invitacion` |
| `plataforma` | Plataforma de juego | `PC`, `PS5`, `Xbox`, `Crossplay` |
| `tipo_competencia` | Tipo de carrera | `Sprint`, `Carrera larga`, `Campeonato`, `Endurance` |
| `activo_desde` | Mes desde cuando está activo | `marzo`, `abril 2025` |
| `activo_hasta` | Mes hasta cuando está activo | `febrero`, `diciembre 2025` |
| `notas` | Notas adicionales | Cualquier información extra importante |

---

## 💡 Ejemplos de Uso

### Ejemplo 1: Configurar una liga nueva desde cero

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

### Ejemplo 2: Actualizar información de una liga existente

```
Cambió el administrador:
!actualizar TSL División 2 | admin: Carlos Rodríguez

Cambió la hora y el stream:
!actualizar TSL División 2 | hora: 21:30 | stream: youtube.com/watch?v=nuevo_link

Añadir el Discord de la liga:
!actualizar TSL División 2 | discord_liga: discord.gg/tsl
```

---

### Ejemplo 3: Gestionar ligas temporales

```
Liga que termina en febrero:
!actualizar EDR Summer | activo_hasta: febrero

Liga que empieza en marzo:
!actualizar EDR División F1 Nitro | activo_desde: marzo

Liga con periodo específico:
!actualizar MRS Summer | activo_desde: enero | activo_hasta: febrero
```

---

### Ejemplo 4: Workflow diario de un miembro

```
1. Al levantarse, revisar qué hay hoy:
!hoy

2. Antes de la carrera, ver detalles:
!info Liga Canalla Prime

3. Durante la semana, planificar:
!calendario
```

---

## ❓ Preguntas Frecuentes

### ¿El bot funciona 24/7?
Sí, el bot está alojado en Replit y configurado para estar activo las 24 horas del día, los 7 días de la semana.

### ¿Cómo funcionan los recordatorios automáticos?
El bot revisa cada 30 minutos si hay alguna carrera en la próxima hora. Si encuentra una, envía un recordatorio al canal configurado con `!canal_recordatorios`.

### ¿Puedo cambiar el canal de recordatorios?
Sí, simplemente usa `!canal_recordatorios` en el nuevo canal que quieras usar. Solo puede haber un canal activo a la vez.

### ¿Qué pasa si escribo mal el nombre de una liga?
El bot busca coincidencias parciales. Por ejemplo, si escribes `!info Canalla`, encontrará "Liga Canalla Prime". No necesitas escribir el nombre completo exacto.

### ¿Se puede cambiar el prefijo de los comandos?
Actualmente el prefijo es `!`. Si quieres cambiarlo, necesitas modificar el código en Replit (línea que dice `command_prefix='!'`).

### ¿Los datos se pierden si el bot se reinicia?
No, todos los datos se guardan automáticamente en un archivo `torneos.json`. Incluso si el bot se reinicia, toda la información se mantiene.

### ¿Puedo añadir más campos personalizados?
Sí, pero requiere modificar el código. Los campos actuales cubren la mayoría de necesidades. Si necesitas algo específico, contacta al desarrollador del bot.

### ¿Cómo elimino información incorrecta?
Puedes usar `!borrar_campo "Nombre Liga" campo` para eliminar un campo específico, o `!actualizar` con el valor correcto para sobreescribirlo.

### ¿El bot guarda historial de carreras?
No, el bot está diseñado para gestionar el calendario actual. No guarda resultados ni historial de carreras pasadas.

---

## 🔧 Soporte Técnico

Si encuentras algún problema o tienes sugerencias:

1. **Errores del bot:** Verifica que estés usando el formato correcto de comandos
2. **El bot no responde:** Asegúrate de que el bot esté ONLINE (círculo verde en Discord)
3. **Problemas de permisos:** Solo los administradores pueden usar comandos de configuración
4. **Otros problemas:** Contacta al administrador del equipo

---

## 📜 Licencia y Créditos

Bot desarrollado para equipos de simracing F1 25.
Desarrollado con discord.py y alojado en Replit.

**Versión:** 2.0  
**Última actualización:** Enero 2025

---

## 🚀 Inicio Rápido

**Para usuarios nuevos:**
1. Escribe `!ayuda_bot` para ver todos los comandos
2. Usa `!calendario` para ver las ligas de la semana
3. Usa `!info <nombre>` para ver detalles de una liga específica

**Para administradores nuevos:**
1. Configura el canal de notificaciones: `!canal_recordatorios`
2. Actualiza las ligas con información: `!actualizar <liga> | campo: valor`
3. Usa `!campos` para ver todos los campos disponibles

---

¡Disfruta del bot y buenas carreras! 🏁
