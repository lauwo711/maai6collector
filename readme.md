# **Herlab**:handbag:

## Intro<br>
A service to monitor new items from https://www.hermes.com/. New item details will be sent to a Telegram channel.

## Infra<br>
Image pushed from local to Docker Hub. Then deploy it on AWS ECS using a public subnet and internet gateway (NAT gateway
is expensive). AWS secret manager stores the token, which are then injected to the container as environment 
variables.

## Packages used<br>
poetry - manage dependency<br>
tenacity - retry http request<br>
fake_useragent - prevent getting block by Hermes :running: <br>
random sleep time and referrers - prevent getting block by Hermes :running:

# Todo
add validator to handle failed request<br>
use asyncio for larger page size<br>
use threading for sending tg message<br>
provide arg parse for scraping different categories of product