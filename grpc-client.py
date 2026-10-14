
import grpc
import argparse
import random
import time
import base64
import lab6_pb2
import lab6_pb2_grpc


def doDotProduct(stub, debug=False):

    # Generate two random vectors
    a = [random.random() for _ in range(100)]
    b = [random.random() for _ in range(100)]

    # Create the gRPC request
    request = lab6_pb2.dotProductMsg(a=a, b=b)

    # Send request to the gRPC server
    response = stub.DotProduct(request)

    # Print response if debugging
    if debug:
        print("Dot Product:", response.dotproduct)


def doAdd(stub, debug=False):

    # Create a request to add 5 and 10
    request = lab6_pb2.addMsg(a=5, b=10)

    # Send the request to the gRPC server
    response = stub.Add(request)

    # Display the result when debugging
    if debug:
        print("Sum:", response.sum)

def doRawImage(stub, debug=False):

    # Read the image file as binary data
    with open('Flatirons_Winter_Sunrise_edit_2.jpg', 'rb') as file:
        image_bytes = file.read()

    # Create a Protobuf request
    request = lab6_pb2.rawImageMsg(img=image_bytes)

    # Send the image to the gRPC server
    response = stub.RawImage(request)

    # Print the dimensions if debugging
    if debug:
        print("Width:", response.width)
        print("Height:", response.height)

def doJsonImage(stub, debug=False):

    # Read the image file
    with open('Flatirons_Winter_Sunrise_edit_2.jpg', 'rb') as file:
        image_bytes = file.read()

    # Convert the image to a Base64 string
    encoded_image = base64.b64encode(image_bytes).decode('utf-8')

    # Create the Protobuf request
    request = lab6_pb2.jsonImageMsg(img=encoded_image)

    # Send the request to the gRPC server
    response = stub.JsonImage(request)

    # Display the image dimensions
    if debug:
        print("Width:", response.width)
        print("Height:", response.height)

# Read command-line arguments
parser = argparse.ArgumentParser()

parser.add_argument('host')
parser.add_argument('cmd', choices=['dotProduct', 'add', 'rawImage', 'jsonImage'])
parser.add_argument('reps', type=int)
parser.add_argument('--port', type=int, default=50051)
parser.add_argument('--debug', action='store_true')

args = parser.parse_args()

if args.reps <= 0:
    parser.error("reps must be a positive integer")

# Connect to the gRPC server
address = f"{args.host}:{args.port}"

channel = grpc.insecure_channel(address)
stub = lab6_pb2_grpc.Lab6ServiceStub(channel)

print(f"Running {args.reps} reps against {address}")

# Measure performance
start = time.perf_counter()



for _ in range(args.reps):
    if args.cmd == 'dotProduct':
        doDotProduct(stub, debug=args.debug)

    elif args.cmd == 'add':
        doAdd(stub, debug=args.debug)

    elif args.cmd == 'rawImage':
        doRawImage(stub, debug=args.debug)

    elif args.cmd == 'jsonImage':
        doJsonImage(stub, debug=args.debug)




elapsed = time.perf_counter() - start

average_ms = (elapsed / args.reps) * 1000

print("Took", average_ms, "ms per operation")

channel.close()
