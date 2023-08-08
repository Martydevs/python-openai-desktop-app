# Inteligencia Artificial

### Python, TKinter y OpenAI

### Cómo iniciar el proyecto?

1. Crear entorno virtual

```console
python -m venv environment
```

2. Activar entorno virtual

Ubicate en la raíz (inicio) de la carpeta

```console
./environment/Scripts/activate.ps1
```

3. Instalar módulos para el proyecto

```console
pip install -r requirements.txt
```

4. Crear archivo de variables de entorno (Powershell)

```console
New-Item .env
```

5. Crear variable de entorno e insertar clave de OpenAI (dentro de .env, escribes lo siguiente)

```console
OPENAI_API_KEY='TU CLAVE DE OPENAI'
```

6. Arrancar aplicación

```console
python ChatBot.py
```

cada comando lo corres en la terminal
