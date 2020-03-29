docker-clean: ##
	## clean up docker leftover
	# docker images
	docker rm $(docker ps -q -f 'status=exited')
	docker rmi $( docker images --filter "dangling=true" -q --no-trunc)
	# docker images | grep "none"
	docker rmi $( docker images | grep "none" | awk '/ / { print $3 }')
	docker volume rm $( docker volume ls -qf dangling=true)


up: 
	docker-compose up --build --remove-orphans

upd: # up --daemon
	docker-compose up --build --remove-orphans -d

updt: upd test
	
down:
	docker-compose down