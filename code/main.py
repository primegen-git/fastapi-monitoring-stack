from fastapi import FastAPI, Request
import time
import logging
from prometheus_client import Counter, Histogram, generate_latest
from starlette.responses import Response

from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

# Enable debug logging (optional but useful for testing)
logging.basicConfig(level=logging.INFO)

# Define service resource
resource = Resource(attributes={"service.name": "fastapi_app"})

# Create tracer provider
tracer_provider = TracerProvider(resource=resource)

# Configure OTLP exporter (to Jaeger in docker-compose)
otlp_exporter = OTLPSpanExporter(
    endpoint="http://jaeger:4317",
    insecure=True,
)

# Add span processor
span_processor = BatchSpanProcessor(otlp_exporter)
tracer_provider.add_span_processor(span_processor)

# Set the global tracer provider
trace.set_tracer_provider(tracer_provider)

# FastAPI app
app = FastAPI()

# Instrument FastAPI with OpenTelemetry
FastAPIInstrumentor.instrument_app(app, tracer_provider=tracer_provider)

# Prometheus metrics
REQUEST_COUNT = Counter("request_count", "Total request count")
REQUEST_LATENCY = Histogram("request_latency_seconds", "Request latency in seconds")


@app.middleware("http")
async def add_metrics(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    REQUEST_COUNT.inc()
    REQUEST_LATENCY.observe(process_time)
    return response


@app.get("/")
async def greet():
    tracer = trace.get_tracer(__name__)
    with tracer.start_as_current_span("greeting_logic"):
        time.sleep(0.05)  # simulate some work
        return {"message": "welcome to vibe monitor"}


@app.get("/metrics")
async def get_metrics():
    return Response(generate_latest(), media_type="text/plain")
