docker run -dit -p 8080:47334 -p 47335:47335 -e "MDB_CONFIG_CONTENT=$(<conf.json)" --name mindsdb mindsdb/mindsdb:latest
# Working run
docker run -it -p 8080:8080 -e MDB_CONFIG_CONTENT='{"api":{"http": {"host": "0.0.0.0","port": "8080"}}}' --name mindsdb mindsdb/mindsdb:latest