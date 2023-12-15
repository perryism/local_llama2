# Model

Copy the model to /data


# Build and run

<pre>
make build
make run
</pre>

# Give it a try

<pre>
curl -X POST 'http://localhost:9999/generate' -d '{"query": "What is in John 3:16?"}' -H Content-Type: application/json
</pre>
