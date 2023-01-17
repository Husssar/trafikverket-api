
VERSION=1.1
TAGNAME="trafikverket-halmstad"
CONTAINER_NAME="$TAGNAME-$VERSION"
echo $CONTAINER_NAME
DOCKERNAME_HASH=$(docker ps -q --filter name=$TAGNAME)
echo $DOCKERNAME_HASH
if [ -n $DOCKERNAME_HASH ]; then 
	docker stop $DOCKERNAME_HASH
	docker rm $DOCKERNAME_HASH
fi


pipreqs --force .
docker build --tag $TAGNAME .

docker run -d --network="host" --restart unless-stopped --name $CONTAINER_NAME $TAGNAME

