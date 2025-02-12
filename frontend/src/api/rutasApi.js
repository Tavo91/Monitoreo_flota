const API_URL = process.env.REACT_APP_API_URL;

///////////////////////////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////////////
// FUNCIONES PARA LAS RUTAS
///////////////////////////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////////////

/**
 * Función para obtener todas las rutas
 */
export const fetchRoutes = async () => {
    const response = await fetch('/api/rutas/', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    });

    if (!response.ok) {
        throw new Error(`Error al obtener las rutas: ${response.status}`);
    }

    return await response.json();
};


/**
 * Función para agregar una nueva ruta
 */
export const addRoute = async (routeData) => {
    console.log("Enviando datos al backend:", routeData); // Depuración
    const response = await fetch('/api/rutas/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(routeData),
    });

    if (!response.ok) {
        const errorDetails = await response.json();
        console.error("Error del backend:", errorDetails); // Depuración
        throw new Error(errorDetails.detail || 'Error al agregar la ruta');
    }

    return await response.json();
};




/**
 * Función para actualizar una ruta existente
 */
export const updateRoute = async (routeData) => {
    const response = await fetch(`${API_URL}/api/gestion/rutas/${routeData.id}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(routeData),
    });

    if (!response.ok) {
        throw new Error('Error al actualizar la ruta');
    }

    return await response.json();
};

/**
 * Función para eliminar una ruta existente
 */
export const deleteRoute = async (id_ruta) => {
    const response = await fetch(`/api/rutas/${id_ruta}`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
        },
    });

    if (!response.ok) {
        const errorDetails = await response.json();
        console.error("Error del servidor:", errorDetails);
        throw new Error(errorDetails.message || 'Error al eliminar la ruta');
    }

    return await response.json();
};


