import tkinter as tk
from tkinter import messagebox
import grpc

import vehicle_pb2
import vehicle_pb2_grpc


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Vehiculos - Tkinter")
        self.geometry("500x360")

        self.channel = grpc.insecure_channel("localhost:50051")
        self.stub = vehicle_pb2_grpc.VehicleServiceStub(self.channel)

        self.entries = {}
        for idx, field in enumerate(["matricula", "vin", "modelo", "marca", "tipo"]):
            tk.Label(self, text=field.capitalize()).place(x=20, y=20 + idx * 35)
            entry = tk.Entry(self, width=40)
            entry.place(x=120, y=20 + idx * 35)
            self.entries[field] = entry

        tk.Button(self, text="Crear", width=12, command=self.create).place(x=20, y=210)
        tk.Button(self, text="Buscar", width=12, command=self.get).place(x=150, y=210)
        tk.Button(self, text="Listar", width=12, command=self.list_all).place(x=280, y=210)
        tk.Button(self, text="Eliminar", width=12, command=self.delete).place(x=380, y=210)

        self.output = tk.Text(self, height=6, width=58)
        self.output.place(x=20, y=250)

    def _get_input(self):
        return {k: v.get().strip() for k, v in self.entries.items()}

    def create(self):
        data = self._get_input()
        req = vehicle_pb2.Vehicle(**data)
        res = self.stub.CreateVehicle(req)
        self._log(res.message)

    def get(self):
        matricula = self.entries["matricula"].get().strip()
        if not matricula:
            messagebox.showerror("Error", "Matricula requerida")
            return
        try:
            v = self.stub.GetVehicle(vehicle_pb2.VehicleId(matricula=matricula))
            for k in self.entries:
                self.entries[k].delete(0, tk.END)
                self.entries[k].insert(0, getattr(v, k))
            self._log("Encontrado")
        except grpc.RpcError as e:
            self._log(f"Error: {e.details()}")

    def list_all(self):
        res = self.stub.ListVehicles(vehicle_pb2.Empty())
        lines = [f"{v.matricula} | {v.vin} | {v.modelo} | {v.marca} | {v.tipo}" for v in res.vehicles]
        self._log("\n".join(lines) if lines else "Sin datos")

    def delete(self):
        matricula = self.entries["matricula"].get().strip()
        if not matricula:
            messagebox.showerror("Error", "Matricula requerida")
            return
        res = self.stub.DeleteVehicle(vehicle_pb2.VehicleId(matricula=matricula))
        self._log(res.message)

    def _log(self, text):
        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, text)


if __name__ == "__main__":
    app = App()
    app.mainloop()
