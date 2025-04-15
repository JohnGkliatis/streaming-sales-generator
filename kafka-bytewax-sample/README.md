## Build Custom Python Container

```shell
export TAG=1.0.0
docker build \
  --no-cache \
  -f docker/Dockerfile \
  -t vvanag/bytewax-kafka-demo:${TAG} .
```