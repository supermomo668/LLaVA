#!/bin/bash
usage()
{
  echo "Usage: Require 8GB RAM and 20GB storage"
  echo "Positional arguments:"
  echo "  POSITIONAL_ARG     Description of the positional argument."
  echo "configuration file (default: '.env/config-default.json')"
  echo "Optional arguments:"
  echo "  -a, --arg1 ARG     Description of the first optional argument."
  echo ""
  echo "Other options:"
  echo "  -h, --help         Display this help message and exit."
}
# start in mindsdb 
default_conf_file="mindsdb/.env/config-default.json"
config_file="${1:-$default_conf_file}"
echo "Using configuration from: $config_file."
docker run -dit -e "MDB_CONFIG_CONTENT=$(jq -c . $config_file)" -e MKL_SERVICE_FORCE_INTEL=1 -p 47334:47334 -p 47335:47335 --name mindsdb mindsdb/mindsdb:latest
# wait for server to load (takes some time)
sleep 7
ngrok http 47334