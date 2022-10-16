#!/bin/sh

# shellcheck disable=SC1073
cat <<EOF> "$CONFIG"
{
  "token_hmac_secret_key": "$JWT_SECRET_KEY",
  "api_key": "$API_CENTRIFUGO_API_KEY",
  "admin_password": "$API_CENTRIFUGO_ADMIN_PASSWORD",
  "admin_secret": "$API_CENTRIFUGO_API_KEY",
  "admin": true,
  "protected": true,

  "allowed_origins": ["*"],
  "presence": true,

  "history_size": 2,
  "history_ttl": "60s",

  "join_leave": false,

  "proxy_http_headers": [
    "Origin",
    "User-Agent",
    "Cookie",
    "Authorization",
    "X-Real-Ip",
    "X-Forwarded-For",
    "X-Request-Id"
  ],

  "namespaces": [
    {
      "name": "some_namespaces",
      "history_recover": true,
      "history_size": 1,
      "history_ttl": "720h",
      "position": true,
      "recover": true,
      "publish": true
    }
  ],
  "prometheus": true,
  "engine": "redis",
  "redis_address": "$REDIS_HOST:$REDIS_PORT",
  "redis_password": "$REDIS_PASSWORD"
}
EOF

exec centrifugo -c config.json