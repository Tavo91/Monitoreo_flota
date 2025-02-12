import React from 'react';

const VehicleList = ({ vehicles, onDelete, onAssignOperator, onUpdate }) => (
  <table>
    <thead>
      <tr>
        <th>ID</th>
        <th>Placa</th>
        <th>Tipo</th>
        <th>Modelo</th>
        <th>Marca</th>
        <th>Año</th>
        <th>Kilometraje</th>
        <th>Estado</th>
        <th>Ubicación</th>
        <th>Último Mantenimiento</th>
        <th>Consumo Combustible</th>
        <th>Operario</th>
        <th>Acciones</th>
      </tr>
    </thead>
    <tbody>
      {vehicles.map((vehicle) => (
        <tr key={vehicle.id_vehiculo}>
          <td>{vehicle.id_vehiculo}</td>
          <td>{vehicle.placa}</td>
          <td>{vehicle.tipo}</td>
          <td>{vehicle.modelo}</td>
          <td>{vehicle.marca}</td>
          <td>{vehicle.año}</td>
          <td>{vehicle.kilometraje}</td>
          <td>{vehicle.estado}</td>
          <td>{vehicle.ubicacion}</td>
          <td>{vehicle.ultimo_mantenimiento}</td>
          <td>{vehicle.consumo_combustible}</td>
          <td>{vehicle.operario_asignado || 'N/A'}</td>
          <td>
            <button onClick={() => onDelete(vehicle.id_vehiculo)}>Eliminar</button>
            <button onClick={() => onAssignOperator(vehicle)}>Asignar Operario</button>
            <button onClick={() => onUpdate(vehicle)}>Actualizar</button>
          </td>
        </tr>
      ))}
    </tbody>
  </table>
);

export default VehicleList;
