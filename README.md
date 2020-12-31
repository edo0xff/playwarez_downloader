
# playwarez download script

Script para descargar series de [playwarez.cc](playwarez.cc)

## Instalación

Requiere python > 3.x

### Clonar repositorio

	git clone https://github.com/edo0xff/playwarez_downloader.git
	cd playwarez_downloader

### Instalar dependencias

	python3 -m pip install -l requirements.txt

## Modo de uso

### Obtener enlaces de descarga

	python3 main.py scrap https://playwarez.cc/series/juego-de-tronos-gratis-a/ > urls.txt

### Descargar

	python3 main.py download urls.txt

## ToDo

- Hacer que funcione con más páginas

## Contributors

- [edo0xff]([https://github.com/edo0xff](https://github.com/edo0xff))
