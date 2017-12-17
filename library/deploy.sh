#!/bin/bash

changed=false
msg=""
stdout=""

source $1

if [ -z "$context" ]; then
  echo '{"failed": true, "msg": "Missing required argument url"}'
  exit 1
fi
if [ -z "$war" ]; then
  echo '{"failed": true, "msg": "Missing required argument war"}'
  exit 1
fi
if [ -z "$username" ]; then
  echo '{"failed": true, "msg": "Missing required argument username"}'
  exit 1
fi
if [ -z "$password" ]; then
  echo '{"failed": true, "msg": "Missing required argument password"}'
  exit 1
fi
if [ ! -f $war ]; then
  echo '{"failed": true, "msg": "File '$war' doesnt exist"}'
  exit 1
fi

stdout=$(tar -Oxzf $war | curl -s --upload-file - "http://$username:$password@localhost:8080/manager/text/deploy?path=$context&update=true")
if echo $stdout | grep -oP 'OK' > /dev/null 2>&1; then 
  changed=true
  vagrant ssh -c "sudo mkdir /var/lib/tomcat/webapps/ -p; sudo chmod 777 /var/lib/tomcat/webapps/;
  echo 'Deploy_time: '$(date) > /var/lib/tomcat/webapps/deploy-info.txt;
  echo 'Deploy_user: Igor_Lakhtenkov' >> /var/lib/tomcat/webapps/deploy-info.txt;
  echo 'Deploy_job: ..." > /dev/null 2>&1
fi

echo '{"changed": '$changed',"msg": "'$msg'","stdout": "'$stdout'"}'



