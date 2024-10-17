# vizcabtest
vizcabtest

Pour lancer le projet à partir de Docker:

0) cd vizcab_project
1) docker build -t vizcab_app .  # générer l'image docker
2) docker run --name vizcab_container -d -p 8000:8000 vizcab_app # générer le conteneur
3) docker exec -it vizcab_container python manage.py migrate  # appliquer les migrations sur le conteneur

Réponses aux questions:

1) Mettre en place les urls d'API correspondant aux endpoints implémentés:

Les urls ont été mis en place, par exemple pour bâtiment avec id==2:

http://localhost:8000/api/buildings/2/carbon-footprint/
http://localhost:8000/api/buildings/2/usage/
http://localhost:8000/api/buildings/2/surface/

2) Quel serait l'outil que vous utiliseriez pour documenter l'API

J'utilise généralement swagger

3) Ecrire un fichier de configuration Docker pour déployer cette API

Le fichier en question est disponible, je n'ai pas utilisé de docker-compose par soucis de simplicité mais il serait adéquat.
J'ai laissé la configuration de base avec sqlite par simplicité également.

4) Pourquoi avoir utilisé Django

Honnêtement j'aurais utilisé fastAPI à la place car beaucoup plus adapté, mais c'était juste pour démontrer que je sais comment ça marche.