Tool to add Mods to your Project Zomboid Server
usage: zomboid.py [-h] [-d | -n] config modlist

Project Zomboid Mod Adding Thing

positional arguments:
  config        Server config location
  modlist       Modlist text file location

options:
  -h, --help    show this help message and exit
  -d, --docker  for a docker compose thing (default: False)
  -n, --native  for native hosting or editing existing container i think (default: False)