from prometheus_client import CollectorRegistry, Counter, Histogram, generate_latest


class PrometheusMetrics(object):
    def __init__(self):
        self.registry = CollectorRegistry()
        self.requests_metric = Counter("http_requests", "Counter of HTTP requests", ["method", "path", "status"], registry=self.registry)
        self.request_histogram_metric = Histogram("request_latency_seconds", "Histogram of request latency", ["method", "path", "status"], registry=self.registry)

    def get(self):
        return generate_latest(self.registry)


metrics = PrometheusMetrics()
