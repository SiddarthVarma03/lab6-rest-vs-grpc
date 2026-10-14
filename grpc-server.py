
import grpc
from concurrent import futures
import argparse
import io
from PIL import Image
import base64

import lab6_pb2
import lab6_pb2_grpc


# Implement the gRPC service
class Lab6Service(lab6_pb2_grpc.Lab6ServiceServicer):

    def DotProduct(self, request, context):

        # Retrieve the two vectors
        a = request.a
        b = request.b

        # Check whether vectors have equal lengths
        if len(a) != len(b):
            context.abort(
                grpc.StatusCode.INVALID_ARGUMENT,
                "Vectors must have the same length"
            )

        # Calculate the dot product
        result = sum(x * y for x, y in zip(a, b))

        # Return the result
        return lab6_pb2.dotProductReply(
            dotproduct=result
        )


    def Add(self, request, context):

        # Read the two numbers from the client
        a = request.a
        b = request.b

        # Calculate their sum
        result = a + b

        # Send the result back to the client
        return lab6_pb2.addReply(sum=result)

    def RawImage(self, request, context):

        # Receive image bytes from the client
        image_bytes = request.img

        # Open the image using Pillow
        img = Image.open(io.BytesIO(image_bytes))

        # Get the image dimensions
        width, height = img.size

        # Return the dimensions to the client
        return lab6_pb2.imageReply(
            width=width,
            height=height
        )

    def JsonImage(self, request, context):

        # Receive the Base64 image string
        encoded_image = request.img

        # Decode Base64 into binary image data
        image_bytes = base64.b64decode(encoded_image)

        # Open the image using Pillow
        img = Image.open(io.BytesIO(image_bytes))

        # Get image dimensions
        width, height = img.size

        # Return width and height
        return lab6_pb2.imageReply(
            width=width,
            height=height
        )

def serve(port):
    # Create the gRPC server
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10)
    )

    # Register our service
    lab6_pb2_grpc.add_Lab6ServiceServicer_to_server(
        Lab6Service(), server
    )

    # Configure server port
    server.add_insecure_port(f'[::]:{port}')

    # Start the server
    server.start()

    print(f"gRPC server running on port {port}")

    # Keep the server running
    server.wait_for_termination()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--port',
        type=int,
        default=50051
    )

    args = parser.parse_args()

    serve(args.port)
