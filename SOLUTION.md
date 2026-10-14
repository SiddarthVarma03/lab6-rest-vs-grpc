# Lab 6 — REST vs. gRPC Performance Comparison

All latency values are in milliseconds per operation.

| Method | Local | Same-Zone | Different Region |
|---|---:|---:|---:|
| REST add | 3.917 | 4.660 | 334.417 |
| gRPC add | 0.962 | 1.280 | 183.833 |
| REST rawimg | 7.310 | 11.289 | 1402.761 |
| gRPC rawimg | 13.305 | 17.354 | 213.676 |
| REST dotproduct | 4.354 | 5.192 | 345.954 |
| gRPC dotproduct | 1.069 | 1.468 | 146.637 |
| REST jsonimg | 44.555 | 48.908 | 1552.651 |
| gRPC jsonimg | 40.865 | 40.955 | 254.521 |
| PING (average RTT) | 0.052 | 0.557 | 141.448 |

## Performance Observations

The experiment compared REST and gRPC for arithmetic and image processing operations under local, same-zone, and different-region network conditions.

In local and same-zone experiments, gRPC performed better for addition, dot product, and JSON image operations, whereas REST was faster for raw image processing. In the different-region experiment between Oregon and Frankfurt, gRPC outperformed REST for all four operations.

Network latency significantly affected communication performance. The average PING latency increased from 0.052 ms locally to 0.557 ms within the same zone and 141.448 ms between regions. In this implementation, REST creates a new TCP connection for each request, whereas gRPC reuses a connection across multiple requests. Connection reuse reduces communication overhead, particularly over high-latency networks.

The image-processing operations experienced higher response times because of their larger payloads. Overall, gRPC showed superior performance in the different-region experiments, highlighting the importance of network latency, payload size, and connection management in distributed systems.

## Testing Configuration

- Local: Client and server on the same VM in us-west1-a.
- Same-Zone: Client and server on separate VMs in us-west1-a.
- Different Region: Client in us-west1-a (Oregon), server in europe-west3-a (Frankfurt).
- Local and Same-Zone: 1000 repetitions for arithmetic operations and 100 for image operations.
- Different Region: 100 repetitions for each operation.
- All communication used internal IP addresses.
