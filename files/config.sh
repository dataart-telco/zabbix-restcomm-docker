#!/bin/bash

if [[ -n "$JUJU_PSWD" ]] && [[ -n "$JUJU_HOST" ]]; then
    cat > /usr/lib/zabbix/externalscripts/jujuapi.yaml <<EOL
juju-api:
  endpoint: "wss://"${JUJU_HOST}"/ws"
  admin-secret: $JUJU_PSWD
EOL

fi

if [[ -n "$JUJU_HOST" ]]; then
fi