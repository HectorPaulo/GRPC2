import grpc
from concurrent import futures

from . import db
from . import vehicle_pb2
from . import vehicle_pb2_grpc


class VehicleService(vehicle_pb2_grpc.VehicleServiceServicer):
    def CreateVehicle(self, request, context):
        try:
            db.create_vehicle({
                "matricula": request.matricula,
                "vin": request.vin,
                "modelo": request.modelo,
                "marca": request.marca,
                "tipo": request.tipo,
            })
            return vehicle_pb2.OperationStatus(ok=True, message="Creado")
        except Exception as exc:
            return vehicle_pb2.OperationStatus(ok=False, message=str(exc))

    def GetVehicle(self, request, context):
        v = db.get_vehicle(request.matricula)
        if not v:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("No encontrado")
            return vehicle_pb2.Vehicle()
        return vehicle_pb2.Vehicle(**v)

    def ListVehicles(self, request, context):
        items = db.list_vehicles()
        return vehicle_pb2.VehicleList(vehicles=[vehicle_pb2.Vehicle(**v) for v in items])

    def DeleteVehicle(self, request, context):
        ok = db.delete_vehicle(request.matricula)
        if ok:
            return vehicle_pb2.OperationStatus(ok=True, message="Eliminado")
        return vehicle_pb2.OperationStatus(ok=False, message="No encontrado")


def serve(port=50051):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    vehicle_pb2_grpc.add_VehicleServiceServicer_to_server(VehicleService(), server)
    server.add_insecure_port(f"[::]:{port}")
    server.start()
    print(f"gRPC escuchando en {port}")
    return server
