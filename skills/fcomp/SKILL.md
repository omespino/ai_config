---
name: fcomp
description: Comprime archivos .mov a .mp4 usando ffmpeg con H.265/HEVC. Usar cuando el usuario quiera comprimir, convertir o reducir el tamaño de un video .mov.
---

Comprime el archivo .mov indicado a .mp4 usando H.265 con buena compatibilidad (hvc1 tag para macOS/iOS).

## Comando

```bash
ffmpeg -i "INPUT.mov" -vcodec libx265 -pix_fmt yuv420p -tag:v hvc1 -crf 28 -preset slow -acodec aac -b:a 128k "OUTPUT.mp4"
```

## Parámetros

- `-vcodec libx265` — codec H.265/HEVC (mejor compresión que H.264)
- `-pix_fmt yuv420p` — compatibilidad máxima con reproductores
- `-tag:v hvc1` — tag necesario para reproducción en macOS/iOS/QuickTime
- `-crf 28` — calidad (menor = mejor calidad, mayor archivo; rango útil 24–32)
- `-preset slow` — mejor compresión a costa de más tiempo de encoding
- `-acodec aac -b:a 128k` — audio AAC a 128 kbps

## Uso

1. Si el usuario da un archivo o ruta, construir el output como el mismo nombre con extensión `.mp4`.

2. **Antes de ejecutar, preguntar siempre:** *"¿Hay alguna región con información sensible que censurar (IDs, documentos, datos personales)?"*

3. **Si responde No** — ejecutar directamente:
```bash
ffmpeg -i "INPUT.mov" -vcodec libx265 -pix_fmt yuv420p -tag:v hvc1 -crf 28 -preset slow -acodec aac -b:a 128k "OUTPUT.mp4"
```

4. **Si responde Sí** — seguir este proceso:
   - Extraer un frame del rango indicado para analizar las coordenadas:
     ```bash
     ffmpeg -ss HH:MM:SS -i "INPUT.mov" -vframes 1 /tmp/frame_check.png -y
     ```
   - Leer la imagen con Read tool para identificar visualmente el área sensible
   - Estimar x, y, w, h escalando desde el thumbnail al tamaño real del video
   - Aplicar blur sobre esa región solo durante el rango de tiempo indicado:
     ```bash
     ffmpeg -i "INPUT.mov" \
       -filter_complex "[0:v]split[main][blur_in];[blur_in]crop=W:H:X:Y,boxblur=20:5[blurred];[main][blurred]overlay=X:Y:enable='between(t,T_START,T_END)'[out]" \
       -map "[out]" \
       -vcodec libx265 -pix_fmt yuv420p -tag:v hvc1 -crf 28 -preset slow \
       -acodec aac -b:a 128k "OUTPUT.mp4" -y
     ```
   - Extraer un frame del resultado para verificar que el blur quedó correcto antes de reportar como listo

Si el usuario quiere ajustar calidad: bajar crf para mejor calidad (ej. 24), subir para más compresión (ej. 32).
