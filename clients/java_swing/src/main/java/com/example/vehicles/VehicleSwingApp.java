package com.example.vehicles;

import io.grpc.ManagedChannel;
import io.grpc.ManagedChannelBuilder;

import javax.swing.*;
import java.awt.*;

public class VehicleSwingApp extends JFrame {
    private final JTextField matricula = new JTextField();
    private final JTextField vin = new JTextField();
    private final JTextField modelo = new JTextField();
    private final JTextField marca = new JTextField();
    private final JTextField tipo = new JTextField();
    private final JTextArea output = new JTextArea();

    private final VehicleServiceGrpc.VehicleServiceBlockingStub stub;

    public VehicleSwingApp() {
        setTitle("Vehiculos - Swing");
        setSize(560, 420);
        setDefaultCloseOperation(EXIT_ON_CLOSE);
        setLocationRelativeTo(null);

        ManagedChannel channel = ManagedChannelBuilder.forAddress("localhost", 50051)
                .usePlaintext()
                .build();
        stub = VehicleServiceGrpc.newBlockingStub(channel);

        JPanel form = new JPanel(new GridLayout(5, 2, 8, 8));
        form.add(new JLabel("Matricula"));
        form.add(matricula);
        form.add(new JLabel("VIN"));
        form.add(vin);
        form.add(new JLabel("Modelo"));
        form.add(modelo);
        form.add(new JLabel("Marca"));
        form.add(marca);
        form.add(new JLabel("Tipo"));
        form.add(tipo);

        JPanel buttons = new JPanel(new FlowLayout(FlowLayout.LEFT));
        JButton btnCreate = new JButton("Crear");
        JButton btnGet = new JButton("Buscar");
        JButton btnList = new JButton("Listar");
        JButton btnDelete = new JButton("Eliminar");
        buttons.add(btnCreate);
        buttons.add(btnGet);
        buttons.add(btnList);
        buttons.add(btnDelete);

        output.setRows(6);
        output.setEditable(false);

        btnCreate.addActionListener(e -> createVehicle());
        btnGet.addActionListener(e -> getVehicle());
        btnList.addActionListener(e -> listVehicles());
        btnDelete.addActionListener(e -> deleteVehicle());

        JPanel main = new JPanel();
        main.setLayout(new BoxLayout(main, BoxLayout.Y_AXIS));
        main.add(form);
        main.add(buttons);
        main.add(new JScrollPane(output));
        add(main);
    }

    private void createVehicle() {
        Vehicle req = Vehicle.newBuilder()
                .setMatricula(matricula.getText().trim())
                .setVin(vin.getText().trim())
                .setModelo(modelo.getText().trim())
                .setMarca(marca.getText().trim())
                .setTipo(tipo.getText().trim())
                .build();
        OperationStatus res = stub.createVehicle(req);
        log(res.getMessage());
    }

    private void getVehicle() {
        String id = matricula.getText().trim();
        if (id.isEmpty()) {
            log("Matricula requerida");
            return;
        }
        try {
            Vehicle v = stub.getVehicle(VehicleId.newBuilder().setMatricula(id).build());
            vin.setText(v.getVin());
            modelo.setText(v.getModelo());
            marca.setText(v.getMarca());
            tipo.setText(v.getTipo());
            log("Encontrado");
        } catch (Exception ex) {
            log("Error: " + ex.getMessage());
        }
    }

    private void listVehicles() {
        VehicleList res = stub.listVehicles(Empty.newBuilder().build());
        if (res.getVehiclesCount() == 0) {
            log("Sin datos");
            return;
        }
        StringBuilder sb = new StringBuilder();
        for (Vehicle v : res.getVehiclesList()) {
            sb.append(v.getMatricula()).append(" | ")
              .append(v.getVin()).append(" | ")
              .append(v.getModelo()).append(" | ")
              .append(v.getMarca()).append(" | ")
              .append(v.getTipo()).append("\n");
        }
        log(sb.toString());
    }

    private void deleteVehicle() {
        String id = matricula.getText().trim();
        if (id.isEmpty()) {
            log("Matricula requerida");
            return;
        }
        OperationStatus res = stub.deleteVehicle(VehicleId.newBuilder().setMatricula(id).build());
        log(res.getMessage());
    }

    private void log(String text) {
        output.setText(text);
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> new VehicleSwingApp().setVisible(true));
    }
}
