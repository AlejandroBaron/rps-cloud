# RPS bot

This project consists on a basic complete stack that for any Machine Learning project to be built locally. It uses:

- PostgreSQL database to store metrics and model information
- PyWebIO as the web serving and interface building
- Markov chains as the model structure
- Docker compose to host the forementioned items

Run docker-boot-clean.sh and you are good to go! Open localhost:80 and there you'll be able to play

If you want to drop/reset the tables, there are some scripts to do so under `src/dockerscripts` or `src/utils/sql`
