/**import React, { useEffect, useState } from 'react';
import {
  fetchVehicles,
  addVehicle,
  deleteVehicle,
  assignOperator,
  updateVehicle,
  assignRoute,
} from './api';
const Vehiculos = () => {
  const [vehicles, setVehicles] = useState([]);
  const [formData, setFormData] = useState({
    placa: '',
    tipo: '',
    modelo: '',
    marca: '',
    año: '',
    kilometraje: '',
    estado: 'disponible',
    ubicacion: '0.000000,0.000000',
    operario_asignado: '',
    consumo_combustible: null,
    ultimo_mantenimiento: null,
  });
  const [routeData, setRouteData] = useState({ id_vehiculo: '', id_ruta: '' });
  const [error, setError] = useState(null);
  const [showUpdateForm, setShowUpdateForm] = useState(false);
  const [showAssignOperatorForm, setShowAssignOperatorForm] = useState(false);
  const [updatedVehicle, setUpdatedVehicle] = useState({});
  const [assignOperatorData, setAssignOperatorData] = useState({
    id_vehiculo: '',
    operario: '',
  });

  useEffect(() => {
    const loadVehicles = async () => {
      try {
        const data = await fetchVehicles();
        setVehicles(data);
      } catch (err) {
        setError(err.message);
      }
    };
    loadVehicles();
  }, []);

  const handleInputChange = (event) => {
    const { name, value } = event.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleRouteChange = (event) => {
    const { name, value } = event.target;
    setRouteData({ ...routeData, [name]: value });
  };

  const handleAddVehicle = async () => {
    try {
      await addVehicle(formData);
      const updatedVehicles = await fetchVehicles();
      setVehicles(updatedVehicles);
    } catch (err) {
      setError(err.message);
    }
  };

  const handleDeleteVehicle = async (id_vehiculo) => {
    try {
      await deleteVehicle(id_vehiculo);
      const updatedVehicles = await fetchVehicles();
      setVehicles(updatedVehicles);
    } catch (err) {
      setError(err.message);
    }
  };

  const handleAssignOperator = async (id_vehiculo) => {
    try {
      await assignOperator(id_vehiculo); // Llama a la API para asignar el operario
      const updatedVehicles = await fetchVehicles(); // Obtiene la lista actualizada
      setVehicles(updatedVehicles); // Actualiza la lista de vehículos en el estado
    } catch (err) {
      setError(err.message);
    }
  };

  const handleUpdateVehicle = async (id_vehiculo, updatedData) => {
    try {
      await updateVehicle(id_vehiculo, updatedData);
      const updatedVehicles = await fetchVehicles();
      setVehicles(updatedVehicles);
      setShowUpdateForm(false);
    } catch (err) {
      setError(err.message);
    }
  };

  const handleAssignRoute = async () => {
    try {
      await assignRoute(routeData);
      const updatedVehicles = await fetchVehicles();
      setVehicles(updatedVehicles);
    } catch (err) {
      setError(err.message);
    }
  };

  const handleUpdateClick = (vehicle) => {
    setUpdatedVehicle(vehicle);  // Cargar todos los campos del vehículo en el formulario
    setShowUpdateForm(true);
  };

  const handleUpdateFormChange = (event) => {
    const { name, value } = event.target;
    setUpdatedVehicle({ ...updatedVehicle, [name]: value });
  };

  const handleUpdateFormSubmit = async (event) => {
    event.preventDefault();
    const updatedData = {
        ...updatedVehicle, // Incluye todos los campos actuales del vehículo
        operario_asignado: updatedVehicle.operario_asignado || null, // Asegura que el operario sea enviado
    };
    await handleUpdateVehicle(updatedVehicle.id_vehiculo, updatedData);
};

  const handleCancelUpdate = () => {
    setShowUpdateForm(false);
    setUpdatedVehicle({});
  };

  const handleShowAssignOperatorForm = () => {
    setShowAssignOperatorForm(true);
  };

  const handleAssignOperatorFormChange = (event) => {
    const { name, value } = event.target;
    setAssignOperatorData({ ...assignOperatorData, [name]: value });
  };

  const handleAssignOperatorFormSubmit = async (event) => {
    event.preventDefault(); // Previene el comportamiento predeterminado del formulario
    try {
        // Llama a la función assignOperator con los datos del formulario
        await assignOperator(assignOperatorData.id_vehiculo, assignOperatorData.operario);
        const updatedVehicles = await fetchVehicles(); // Actualiza la lista de vehículos
        setVehicles(updatedVehicles); // Actualiza el estado con los vehículos actualizados
        setAssignOperatorData({ id_vehiculo: '', operario: '' }); // Limpia el formulario
        setShowAssignOperatorForm(false); // Cierra el formulario
    } catch (err) {
        console.error("Error assigning operator:", err.message);
        setError(err.message); // Muestra el error si ocurre
    }
};




  const handleCancelAssignOperator = () => {
    setAssignOperatorData({ id_vehiculo: '', operario: '' }); // Reiniciar campos del formulario
    setShowAssignOperatorForm(false); // Ocultar formulario
  };

  const assignOperator = async (id_vehiculo, operario_asignado) => {
    // Construir la URL con el parámetro query
    const response = await fetch(
      `/api/gestion/vehiculos/${id_vehiculo}/asignar_operario/?operario=${encodeURIComponent(operario_asignado)}`,
      {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
      }
    );

    if (!response.ok) {
      const errorDetails = await response.json();
      console.error('Error de la API: ', errorDetails);
      throw new Error(errorDetails.message || 'Error al asignar el operario');
    }

    return await response.json();
  };

  if (error) {
    return <div>Error loading vehicles: {error}</div>;
  }
  return (
    <div>
      <h1>Gestión de Vehículos</h1>
      <h2>Lista de Vehículos</h2>
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
                <button
                  onClick={() => handleDeleteVehicle(vehicle.id_vehiculo)}
                >
                  Eliminar
                </button>
                <button onClick={() => handleShowAssignOperatorForm(vehicle.id_vehiculo)}>
    Asignar Operario
</button>


                <button onClick={() => handleUpdateClick(vehicle)}>
                  Actualizar
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {showAssignOperatorForm && (
        <form onSubmit={handleAssignOperatorFormSubmit}>
          <h2>Asignar Operario</h2>
          <label>
            ID Vehículo:
            <input
              type="text"
              name="id_vehiculo"
              value={assignOperatorData.id_vehiculo}
              onChange={handleAssignOperatorFormChange}
            />
          </label>
          <label>
            Nombre del Operario:
            <input
              type="text"
              name="operario"
              value={assignOperatorData.operario}
              onChange={handleAssignOperatorFormChange}
            />
          </label>
          <button type="button" onClick={handleCancelAssignOperator}>
            Cancelar
          </button>
          <button type="submit">Asignar</button>
        </form>
      )}

      {showUpdateForm && (
        <form onSubmit={handleUpdateFormSubmit}>
          <h2>Actualizar Vehículo</h2>
          <label>
            Placa:
            <input
              type="text"
              name="placa"
              value={updatedVehicle.placa}
              onChange={handleUpdateFormChange}
            />
          </label>
          <label>
            Tipo:
            <input
              type="text"
              name="tipo"
              value={updatedVehicle.tipo}
              onChange={handleUpdateFormChange}
            />
          </label>
          <label>
            Modelo:
            <input
              type="text"
              name="modelo"
              value={updatedVehicle.modelo}
              onChange={handleUpdateFormChange}
            />
          </label>
          <label>
            Marca:
            <input
              type="text"
              name="marca"
              value={updatedVehicle.marca}
              onChange={handleUpdateFormChange}
            />
          </label>
          <label>
            Año:
            <input
              type="number"
              name="año"
              value={updatedVehicle.año}
              onChange={handleUpdateFormChange}
            />
          </label>
          <label>
            Kilometraje:
            <input
              type="number"
              name="kilometraje"
              value={updatedVehicle.kilometraje}
              onChange={handleUpdateFormChange}
            />
          </label>
          <label>
            Estado:
            <input
              type="text"
              name="estado"
              value={updatedVehicle.estado}
              onChange={handleUpdateFormChange}
            />
          </label>
          <button type="button" onClick={handleCancelUpdate}>
            Cancelar
          </button>
          <button type="submit">Guardar</button>
        </form>
      )}

      <h2>Agregar Vehículo</h2>
      <form>
        <input
          type="text"
          name="placa"
          placeholder="Placa"
          value={formData.placa}
          onChange={handleInputChange}
        />
        <input
          type="text"
          name="tipo"
          placeholder="Tipo"
          value={formData.tipo}
          onChange={handleInputChange}
        />
        <input
          type="text"
          name="modelo"
          placeholder="Modelo"
          value={formData.modelo}
          onChange={handleInputChange}
        />
        <input
          type="text"
          name="marca"
          placeholder="Marca"
          value={formData.marca}
          onChange={handleInputChange}
        />
        <input
          type="number"
          name="año"
          placeholder="Año"
          value={formData.año}
          onChange={handleInputChange}
        />
        <input
          type="number"
          name="kilometraje"
          placeholder="Kilometraje"
          value={formData.kilometraje}
          onChange={handleInputChange}
        />
        <button type="button" onClick={handleAddVehicle}>
          Agregar
        </button>
      </form>
      <h2>Asignar Ruta</h2>
      <form>
        <input
          type="number"
          name="id_vehiculo"
          placeholder="ID Vehículo"
          value={routeData.id_vehiculo}
          onChange={handleRouteChange}
        />
        <input
          type="text"
          name="origen"
          placeholder="Origen"
          value={routeData.origen}
          onChange={handleRouteChange}
        />
        <input
          type="text"
          name="destino"
          placeholder="Destino"
          value={routeData.destino}
          onChange={handleRouteChange}
        />
        <button type="button" onClick={handleAssignRoute}>
          Asignar Ruta
        </button>
      </form>
    </div>
  );
};

export default Vehiculos;
*/