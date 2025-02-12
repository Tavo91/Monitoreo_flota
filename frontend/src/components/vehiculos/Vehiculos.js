import React, { useEffect, useState } from 'react';
import VehicleList from './formularios/VehicleList';
import AddVehicleForm from './formularios/AddVehicleForm';
import UpdateVehicleForm from './formularios/UpdateVehicleForm';
import AssignOperatorForm from './formularios/AssignOperatorForm';
import AssignRouteForm from './formularios/AssignRouteForm';
import { fetchVehicles, addVehicle, deleteVehicle, assignOperator, updateVehicle, assignRoute } from '../../api';


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
      <VehicleList
        vehicles={vehicles}
        onDelete={handleDeleteVehicle}
        onAssignOperator={handleShowAssignOperatorForm}
        onUpdate={handleUpdateClick}
      />
      <AddVehicleForm formData={formData} onChange={handleInputChange} onSubmit={handleAddVehicle} />
      {showUpdateForm && (
        <UpdateVehicleForm
          updatedVehicle={updatedVehicle}
          onChange={handleUpdateFormChange}
          onSubmit={handleUpdateFormSubmit}
          onCancel={handleCancelUpdate}
        />
      )}
      {showAssignOperatorForm && (
        <AssignOperatorForm
          assignOperatorData={assignOperatorData}
          onChange={handleAssignOperatorFormChange}
          onSubmit={handleAssignOperatorFormSubmit}
          onCancel={handleCancelAssignOperator}
        />
      )}
      <AssignRouteForm
        routeData={routeData}
        onChange={handleRouteChange}
        onSubmit={handleAssignRoute}
      />
    </div>
  );
};

export default Vehiculos;
