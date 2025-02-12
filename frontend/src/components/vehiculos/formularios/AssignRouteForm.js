import React from 'react';

const AssignRouteForm = ({ routeData, onChange, onSubmit }) => (
  <form onSubmit={onSubmit}>
    <input type="text" name="id_vehiculo" placeholder="ID Vehículo" value={routeData.id_vehiculo} onChange={onChange} />
    <input type="text" name="origen" placeholder="Origen" value={routeData.origen} onChange={onChange} />
    <input type="text" name="destino" placeholder="Destino" value={routeData.destino} onChange={onChange} />
    <button type="submit">Asignar Ruta</button>
  </form>
);

export default AssignRouteForm;
