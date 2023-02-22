![image](https://user-images.githubusercontent.com/62940341/210772427-b8b3db0f-659c-4190-a9cf-9918a25461e4.png)

<b>A minimalistic ElasticSearch + FastAPI + Svelte demo project to get you started developing with this stack.</b>


### Start
All three components are dockerized, i.e. you just need to start the docker containers defined in the [docker-compose.yml](https://github.com/jfreyberg/svelte-demo-searchbar/blob/main/docker-compose.yml), e.g. using the [start.sh](https://github.com/jfreyberg/svelte-demo-searchbar/blob/main/start.sh) script with `./start.sh` or `sudo ./start.sh`.

Make sure the ports for the three components are available on your machine:
* ElasticSearch: 9200
* FastAPI: 2999
* Webapp: 3000

After launching the containers you can check out the webapp on [localhost:3000](http://localhost:3000).

Note that it will take a few moments for the database to be initialized and the data to be indexed.

### Stop
You can stop the containers using the [stop.sh](https://github.com/jfreyberg/svelte-demo-searchbar/blob/main/stop.sh) script with `./stop.sh` or `sudo ./stop.sh`.

<b>Feel free to fork this project!</b>
