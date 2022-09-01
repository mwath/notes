# Build
Pour lancer l'application, il faut tout d'abord mettre en place le fichier `.env`. Un exemple de fichier existe sous le nom de `.env.example`.

Ensuite, à l'aide docker, on peut lancer les différents services:
```sh
docker-compose up -d
```
Une fois les services lancés, il est nécessaire d'effectuer la migration de la base de données pour qu'elle soit opérationnelle.
Pour cela, iil suffit d'exécuter le fichier `setup.sh`:
```sh
./setup.sh
```

# Production
La mise en production est similaire, mais il faut utilise un fichier `docker-compose` différent:
```sh
docker-compose -f docker-compose.prod.yaml up -d --build
```