import React, { useState, useEffect } from 'react';
import { fetchRoutes } from '../../api/rutasApi';
import AddRouteForm from './formularios/AddRouteForm';
import RutasList from './formularios/RutasList';

const Rutas = () => {
    const [routes, setRoutes] = useState([]);
    const [showAddRouteForm, setShowAddRouteForm] = useState(false);
    const [error, setError] = useState(null);

    // Cargar las rutas al montar el componente
    useEffect(() => {
        const loadRoutes = async () => {
            try {
                const data = await fetchRoutes();
                setRoutes(data);
            } catch (err) {
                setError(err.message);
            }
        };
        loadRoutes();
    }, []);

    // Manejar la apertura del formulario de agregar ruta
    const handleShowAddRouteForm = () => {
        setShowAddRouteForm(true);
    };

    // Manejar la cancelación del formulario de agregar ruta
    const handleCancelAddRouteForm = () => {
        setShowAddRouteForm(false);
    };

    // Manejar la actualización de rutas después de una operación (por ejemplo, eliminar o agregar)
    const handleRoutesUpdated = async () => {
        try {
            const updatedRoutes = await fetchRoutes();
            setRoutes(updatedRoutes);
        } catch (err) {
            console.error('Error al actualizar la lista de rutas:', err.message);
        }
    };

    return (
        <div>
            <h1>Gestión de Rutas</h1>
            <button onClick={handleShowAddRouteForm}>Agregar Ruta</button>
            {error && <p style={{ color: 'red' }}>{error}</p>}

            {/* Mostrar el formulario de agregar ruta si está habilitado */}
            {showAddRouteForm && (
                <AddRouteForm
                    onRouteAdded={() => {
                        // Recargar las rutas después de agregar una nueva
                        handleRoutesUpdated();
                        setShowAddRouteForm(false); // Ocultar el formulario
                    }}
                    onCancel={handleCancelAddRouteForm}
                />
            )}

            {/* Mostrar la lista de rutas */}
            <RutasList routes={routes} onRoutesUpdated={handleRoutesUpdated} />
        </div>
    );
};

export default Rutas;


