import React from 'react';

const AssignOperatorForm = ({ assignOperatorData, onChange, onSubmit, onCancel }) => (
  <form onSubmit={onSubmit}>
    <input
      type="text"
      name="id_vehiculo"
      placeholder="ID Vehículo"
      value={assignOperatorData.id_vehiculo}
      onChange={onChange}
    />
    <input
      type="text"
      name="operario"
      placeholder="Operario"
      value={assignOperatorData.operario}
      onChange={onChange}
    />
    <button type="button" onClick={onCancel}>Cancelar</button>
    <button type="submit">Asignar</button>
  </form>
);

export default AssignOperatorForm;
