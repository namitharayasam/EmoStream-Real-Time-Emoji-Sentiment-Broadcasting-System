# EmoStream: Real-Time Emoji Sentiment Broadcasting System

## Overview

EmoStream is a big data project that enables real-time sentiment analysis and visualization of emoji reactions during live events, such as sports matches. It processes billions of reactions with low latency using a scalable event-driven architecture powered by Apache Kafka and Apache Spark Streaming. The system efficiently aggregates and compresses reactions for streamlined real-time visualization.

## Key Features

- **Scalable Kafka-Based Event Processing**: Handles billions of emoji reactions per event with high throughput and low latency.
- **Real-Time Sentiment Aggregation**: Utilizes Apache Spark Streaming to process emoji reactions in 2-second micro-batches, ensuring near-instant updates.
- **High-Efficiency Data Compression**: Achieves a 1000:1 compression ratio, reducing storage and bandwidth overhead.
- **Event-Driven Architecture**: Leverages Kafka topics for efficient pub-sub messaging, ensuring seamless ingestion and processing.
- **Big Data Pipeline**: Integrates with distributed storage (HDFS) for historical analysis and machine learning-based insights.

## Tech Stack

- **Data Ingestion & Streaming**: Apache Kafka, Spark Streaming
- **Processing & Aggregation**: Apache Spark (PySpark), Kafka Streams
- **Storage**: HDFS

## System Architecture

1. **Emoji Reactions Producer**: Users send emoji reactions via the Client.py file
2. **Kafka Ingestion Layer**: Reactions are published to Kafka topics.
3. **Spark Streaming Pipeline**: Consumes Kafka topics, aggregates sentiment in 2-second micro-batches.
4. **Data Compression & Storage**: Compressed aggregated data is stored in HDFS for future analysis.

## Setup

### Prerequisites

- Apache Kafka & Zookeeper
- Apache Spark
- Python
- Docker (optional for containerized deployment)

## Project Demo Setup

- The demo environment consists of **2 clusters with 4 nodes each**.
- Username assignment is dynamic, and each client is assigned a username upon arrival.
- If the number of clients exceeds the available capacity, load balancing is managed by placing the client in a **waiting list** until another user leaves the system.

## Future Enhancements

- **Machine Learning Integration**: Predicting sentiment trends using deep learning on time-series data.
- **Cloud-Based Auto-Scaling**: Implementing Kubernetes-based dynamic resource allocation.
