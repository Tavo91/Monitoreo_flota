const API_URL = process.env.REACT_APP_API_URL || "http://127.0.0.1:8000/api";

export const fetchVehicles = async () => {
  const response = await fetch(`${API_URL}/gestion/vehiculos/`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
    },
  });

  if (!response.ok) {
    throw new Error(`HTTP error! Status: ${response.status}`);
  }

  return await response.json();
};

export const addVehicle = async (vehicleData) => {
  try {
    const response = await fetch(`${API_URL}/gestion/vehiculos/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(vehicleData),
    });
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error('Error adding vehicle:', error);
    throw error;
  }
};

export const deleteVehicle = async (id) => {
  try {
    const response = await fetch(`${API_URL}/gestion/vehiculos/${id}`, {
      method: 'DELETE',
    });
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error('Error deleting vehicle:', error);
    throw error;
  }
};

export const assignOperator = async (id_vehiculo, operario_asignado) => {
  const response = await fetch(
      `${process.env.REACT_APP_API_URL}/gestion/vehiculos/${id_vehiculo}/asignar_operario/?operario=${encodeURIComponent(operario_asignado)}`,
      {
          method: 'PUT',
          headers: {
              'Content-Type': 'application/json',
          },
      }
  );
  console.log("Datos del formulario:", operario_asignado);
  if (!response.ok) {
      const errorDetails = await response.json();
      console.error('Error de la API: ', errorDetails);
      throw new Error(errorDetails.message || 'Error al asignar el operario');
  }

  return await response.json();
};



export const updateVehicle = async (id, updatedData) => {
  try {
    const response = await fetch(`${API_URL}/gestion/vehiculos/${id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(updatedData),
    });
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error('Error updating vehicle:', error);
    throw error;
  }
};

export const assignRoute = async (routeData) => {
  await fetch(`${API_URL}/gestion/asignar/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(routeData),
  });
};
