import React from 'react';

const UpdateVehicleForm = ({ updatedVehicle, onChange, onSubmit, onCancel }) => (
  <form onSubmit={onSubmit}>
    <input type="text" name="placa" value={updatedVehicle.placa} onChange={onChange} />
    <input type="text" name="tipo" value={updatedVehicle.tipo} onChange={onChange} />
    <input type="text" name="modelo" value={updatedVehicle.modelo} onChange={onChange} />
    <input type="text" name="marca" value={updatedVehicle.marca} onChange={onChange} />
    <input type="number" name="año" value={updatedVehicle.año} onChange={onChange} />
    <input type="number" name="kilometraje" value={updatedVehicle.kilometraje} onChange={onChange} />
    <button type="button" onClick={onCancel}>Cancelar</button>
    <button type="submit">Guardar</button>
  </form>
);

export default UpdateVehicleForm;
