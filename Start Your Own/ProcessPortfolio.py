"""Wrapper for the shared trading script using local data directory."""

from pathlib import Path
import sys

# Allow importing the shared module from the repository root
sys.path.append(str(Path(__file__).resolve().parents[1]))

from trading_script import main


if __name__ == "__main__":

    data_dir = Path(__file__).resolve().parent
    main(Path("Start Your Own"))

#!/bin/sh

sed -i "s/\$SENTINEL_QUORUM/$SENTINEL_QUORUM/g" /etc/redis/sentinel.conf
sed -i "s/\$SENTINEL_DOWN_AFTER/$SENTINEL_DOWN_AFTER/g" /etc/redis/sentinel.conf
sed -i "s/\$SENTINEL_FAILOVER/$SENTINEL_FAILOVER/g" /etc/redis/sentinel.conf

exec docker-entrypoint.sh redis-server /etc/redis/sentinel.conf --sentinel#!/bin/sh

sed -i "s/\$SENTINEL_QUORUM/$SENTINEL_QUORUM/g" /etc/redis/sentinel.conf
sed -i "s/\$SENTINEL_DOWN_AFTER/$SENTINEL_DOWN_AFTER/g" /etc/redis/sentinel.conf
sed -i "s/\$SENTINEL_FAILOVER/$SENTINEL_FAILOVER/g" /etc/redis/sentinel.conf

exec docker-entrypoint.sh redis-server /etc/redis/sentinel.conf --sentinel
MASTER_IP=$(docker inspect --format '{{ .NetworkSettings.IPAddress }}' redis-cluster_master_1)
SLAVE_IP=$(docker inspect --format '{{ .NetworkSettings.IPAddress }}' redis-cluster_slave_1)
SENTINEL_IP=$(docker inspect --format '{{ .NetworkSettings.IPAddress }}' redis-cluster_sentinel_1)

echo Redis master: $MASTER_IP
echo Redis Slave: $SLAVE_IP
echo ------------------------------------------------
echo Initial status of sentinel
echo ------------------------------------------------
docker exec redis-cluster_sentinel_1 redis-cli -p 26379 info Sentinel
echo Current master is
docker exec redis-cluster_sentinel_1 redis-cli -p 26379 SENTINEL get-master-addr-by-name mymaster
echo ------------------------------------------------

echo Stop redis master
docker pause redis-cluster_master_1
echo Wait for 10 seconds
sleep 10
echo Current infomation of sentinel
docker exec redis-cluster_sentinel_1 redis-cli -p 26379 info Sentinel
echo Current master is
docker exec redis-cluster_sentinel_1 redis-cli -p 26379 SENTINEL get-master-addr-by-name mymaster


echo ------------------------------------------------
echo Restart Redis master
docker unpause redis-cluster_master_1
sleep 5
echo Current infomation of sentinel
docker exec redis-cluster_sentinel_1 redis-cli -p 26379 info Sentinel
echo Current master is
docker exec redis-cluster_sentinel_1 redis-cli -p 26379 SENTINEL get-master-addr-by-name mymaster
