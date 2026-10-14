
# Lab 6 — REST vs. gRPC Performance Comparison

All latency values are in milliseconds per operation.

| Method | Local | Same-Zone | Different Region |
|---|---:|---:|---:|
| REST add | 3.917 | 4.660 | 170.661 |
| gRPC add | 0.962 | 1.280 | 82.757 |
| REST rawimg | 7.310 | 11.289 | 646.652 |
| gRPC rawimg | 13.305 | 17.354 | 163.850 |
| REST dotproduct | 4.354 | 5.192 | 169.589 |
| gRPC dotproduct | 1.069 | 1.468 | 72.000 |
| REST jsonimg | 44.555 | 48.908 | 754.089 |
| gRPC jsonimg | 40.865 | 40.955 | 223.917 |
| PING (average RTT) | 0.052 | 0.557 | 65.269 |

## Performance Observations

The experiment compares the performance of REST and gRPC for arithmetic operations and image processing under different network conditions.

For local communication, gRPC performed better for addition, dot product, and JSON image operations, while REST was faster for raw image processing. Similar results were observed for same-zone communication.

For different-region communication, gRPC outperformed REST in all four operations. Network latency significantly affected performance, with average PING latency increasing from 0.052 ms locally to 65.269 ms across regions.

REST establishes a new TCP connection for each request in this implementation, adding connection overhead. In contrast, gRPC reuses a single TCP connection across multiple requests. This reduces communication overhead and provides significant performance improvements over higher-latency networks.

Overall, gRPC demonstrated better performance for most operations, especially across regions. The results show that network latency and connection reuse are important factors when selecting communication protocols for distributed systems.

## Testing Configuration

- Local: Client and server on the same VM.
- Same-Zone: Client and server on separate VMs within us-west1-a.
- Different Region: Client in us-east1-b and server in us-west1-a.
- Local and Same-Zone: 1000 repetitions for arithmetic operations and 100 for image operations.
- Different Region: 30 repetitions for arithmetic operations and 10 for image operations.

The different-region results are preliminary measurements using reduced repetition counts.
  
