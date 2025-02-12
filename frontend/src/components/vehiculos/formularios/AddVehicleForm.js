import React from 'react';

const AddVehicleForm = ({ formData, onChange, onSubmit }) => (
  <form onSubmit={onSubmit}>
    <input type="text" name="placa" placeholder="Placa" value={formData.placa} onChange={onChange} />
    <input type="text" name="tipo" placeholder="Tipo" value={formData.tipo} onChange={onChange} />
    <input type="text" name="modelo" placeholder="Modelo" value={formData.modelo} onChange={onChange} />
    <input type="text" name="marca" placeholder="Marca" value={formData.marca} onChange={onChange} />
    <input type="number" name="año" placeholder="Año" value={formData.año} onChange={onChange} />
    <input type="number" name="kilometraje" placeholder="Kilometraje" value={formData.kilometraje} onChange={onChange} />
    <button type="submit">Agregar</button>
  </form>
);

export default AddVehicleForm;
