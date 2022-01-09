from prometheus_client import start_http_server, Gauge, CollectorRegistry
import requests
import time

TEST_URLS = [
    "https://httpstat.us/503",
    "https://httpstat.us/200"
]

PORT = 8000


def main():
    # Setup Prometheus gauge
    registry = CollectorRegistry()
    service_status_gauge = Gauge('sample_external_url_up', 'Sample External URL UP', ['url'], registry=registry)
    service_latency_gauge = Gauge('sample_external_url_response_ms', 'Sample External URL Response MS', ['url'], registry=registry)

    start_http_server(PORT, registry=registry)
    print("[INFO] Server started at port {}".format(PORT))

    while True:
        for url in TEST_URLS:
            response = requests.get(url)
            # Set service status metric
            if (response.status_code == 200):
                service_status_gauge.labels(url=url).set(1)
            else:
                service_status_gauge.labels(url=url).set(0)
            
            # Set Service letency metric
            service_latency_gauge.labels(url=url).set(response.elapsed.total_seconds()*1000)

if __name__ == '__main__':
    main()
