# strafe-twitch

Docker microservice for Twitch channel subscriptions

## Run project

```bash
docker-compose up -d --build
```

On the browser go to http://0.0.0.0:8081/graphiql

## Graphql - Start tracking a new channel

```graphql
mutation {
	trackChannel(channel: "<channel>")
}
```

## Graphql - Get messages per second/minute on subscribed channels

```graphql
subscription {
	messagesPerSecond(channel: "<channel>")
}

subscription {
	messagesPerMinute(channel: "<channel>")
}
```


## Graphql - Get Kappa per minute on subscribed channels

```graphql
subscription {
	kappaPerMinute(channel: "<channel>")
}
```
