import grpc
from concurrent import futures
import cube_pb2
import cube_pb2_grpc

class CubeServiceServicer(cube_pb2_grpc.CubeServiceServicer):
    def GetCube(self, request, context):
        number = request.number
        cube = number ** 3
        return cube_pb2.CubeResponse(cube=cube)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    cube_pb2_grpc.add_CubeServiceServicer_to_server(CubeServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
