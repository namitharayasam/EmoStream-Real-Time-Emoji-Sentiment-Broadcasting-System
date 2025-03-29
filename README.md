# EmoStream: Real-Time Emoji Sentiment Broadcasting System

## Overview

SentimentStream is a big data project that enables real-time sentiment analysis and visualization of emoji reactions during live events, such as sports matches. It processes billions of reactions with low latency using a scalable event-driven architecture powered by Apache Kafka and Apache Spark Streaming. The system efficiently aggregates and compresses reactions for streamlined real-time visualization.

## Key Features

- **Scalable Kafka-Based Event Processing**: Handles billions of emoji reactions per event with high throughput and low latency.
- **Real-Time Sentiment Aggregation**: Utilizes Apache Spark Streaming to process emoji reactions in 2-second micro-batches, ensuring near-instant updates.
- **High-Efficiency Data Compression**: Achieves a 1000:1 compression ratio, reducing storage and bandwidth overhead.
- **Event-Driven Architecture**: Leverages Kafka topics for efficient pub-sub messaging, ensuring seamless ingestion and processing.
- **Big Data Pipeline**: Integrates with distributed storage (HDFS/S3) for historical analysis and machine learning-based insights.
- **Scalable Visualization**: Aggregated sentiment scores are visualized in real-time using WebSockets and a React-based dashboard.

## Tech Stack

- **Data Ingestion & Streaming**: Apache Kafka, Spark Streaming
- **Processing & Aggregation**: Apache Spark (PySpark/Scala), Kafka Streams
- **Storage**: HDFS / Amazon S3 / PostgreSQL (optional for metadata)
- **Visualization**: React.js, WebSockets, D3.js
- **Deployment**: Docker, Kubernetes, AWS/GCP (for cloud-based scaling)

## System Architecture

1. **Emoji Reactions Producer**: Users send emoji reactions via a front-end app.
2. **Kafka Ingestion Layer**: Reactions are published to Kafka topics.
3. **Spark Streaming Pipeline**: Consumes Kafka topics, aggregates sentiment in 2-second micro-batches.
4. **Data Compression & Storage**: Compressed aggregated data is stored in HDFS/S3 for future analysis.
5. **WebSockets-Based Visualization**: A React.js dashboard fetches real-time sentiment trends for viewers.

## Setup & Installation

### Prerequisites

- Apache Kafka & Zookeeper
- Apache Spark
- Python 3.8+ / Scala (for Spark processing)
- Node.js (for front-end visualization)
- Docker (optional for containerized deployment)

### Steps to Run

1. **Start Kafka & Zookeeper:**
   ```sh
   zookeeper-server-start.sh config/zookeeper.properties &
   kafka-server-start.sh config/server.properties &
   ```

2. **Start Kafka Producer** (Simulated emoji reaction events):
   ```sh
   python producer.py  # Generates emoji reaction events
   ```

3. **Run Spark Streaming Job:**
   ```sh
   spark-submit --master local[2] spark_streaming.py
   ```

4. **Start WebSocket Server & React Dashboard:**
   ```sh
   cd frontend
   npm install && npm start
   ```

5. **View Live Sentiment Analytics** on `http://localhost:3000`

## Future Enhancements

- **Machine Learning Integration**: Predicting sentiment trends using deep learning on time-series data.
- **Multi-Event Support**: Scaling to handle concurrent live events.
- **Cloud-Based Auto-Scaling**: Implementing Kubernetes-based dynamic resource allocation.
- **Integration with Social Media Feeds**: Extending emoji sentiment tracking beyond sports events.

## Contributors

- **Namitha Rayasam** ([GitHub](https://github.com/your_github))

## License

This project is licensed under the **MIT License**.
