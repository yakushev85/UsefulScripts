# Scripts for daily usage


## Git
- update branch from develop
```
git checkout develop
git pull
git checkout feature/$1
git merge develop 
git push
```

- create new branch
```
git checkout -b [name_of_your_new_branch]
```

- rename branch
```
git branch -m old_branch new_branch
git push origin :old_branch new_branch
git push origin -u new_branch
```

- to apply commit id to your current branch
```
git cherry-pick commit_id
```

- reset to some previous commit
```
git reset --hard previous-sha1-commit-id
git push origin HEAD --force
```


## Docker
- build container
```
docker-compose build
```

- create and up container
```
docker-compose up
```

- run container locally with bash console
```
docker-compose run --rm app bash
```

- connect to a container via ssh
```
docker exec -it container_name /bin/bash
```

- list of active docker containers
```
docker container ls
```


## SLS
- to start api locally after container is up
```
sls offline
sls offline --stage local
```

- testing from container
```
sls invoke local -f version
sls invoke local --function create --stage development --region us-east-1 --path src/create/event.json
```

- deploying
```
serverless deploy --function sign-in --stage development --region us-east-1
serverless deploy --stage development --region us-east-1
serverless deploy --stage testing
```

- creds
```
serverless config credentials --provider aws --key keyvalue --secret secretvalue
```

- flyway
```
flyway migrate -url=jdbc:postgresql://localhost:2345/test -user=test -password=password -locations=filesystem:/Users/test/Documents/sql

flyway repair -url=jdbc:postgresql://dev.test.us-east-1.rds.amazonaws.com:5432/test -user=test -password=test -locations=filesystem:/Users/test/Documents/sql
```

## Curl
- POST multipart/form-data
```
echo "test\ntest\ntest\n" > 1.log && zip logs.zip 1.log
curl -F crash_identifier=Atest1324 -F file_name=logs.zip -F identifier=test.android.development -F device=SM-G930T1 -F os=7.0 -F version=1.5.0 -F build=258 -F file=@logs.zip -X POST https://test.com/v1/log-file-upload
```

- with encoded body to base64
```
echo "test!test!test!" > 1.log && zip logs.zip 1.log
openssl base64 -in logs.zip -out logs_ready.zip
curl -F crash_identifier=Atest1324 -F file_name=logs_ready.zip -F identifier=test.android.development -F device=SM-G930T1 -F os=7.0 -F version=1.5.0 -F build=258 -F file=@logs_ready.zip -X POST https://test.com/v1/log-file-upload
```

## SCP and SSH
- connect via certificate
```
scp -i ~/.ssh/test.pem ./test.py ubuntu@0.0.0.0:~/backend
scp -i ~/.ssh/test.pem ubuntu@0.0.0.0:~/backend/test.sql ~/Documents
ssh -i ~/.ssh/test.pem ubuntu@0.0.0.0
```

- find all files in ~/ with size bigger than 1Gb
```
find -x ~/ -type f -size +1G
```

- sdk calls
```
curl -v https://test.com/rest/ValidationService?token=88qlmNTC1
```

