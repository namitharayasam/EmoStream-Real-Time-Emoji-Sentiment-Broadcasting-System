#!/bin/bash

# List of Python files to run, excluding sparkjob.py
FILES=(
    "Cluster_publisher1.py"
    "Cluster_publisher2.py"
    "Main_publisher.py"
    "Main_consumer.py"
    "Subscriber1.py"
    "Subscriber2.py"
    "Subscriber3.py"
    "Subscriber4.py"
)


# source /path/to/your/venv/bin/activate

# Run each file in a new background process
for file in "${FILES[@]}"; do
    echo "Running $file..."
    python3 "$file" &
done

wait
echo "All scripts have finished execution."

