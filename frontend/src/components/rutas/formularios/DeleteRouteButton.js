import React, { useState } from 'react';
import { deleteRoute } from '../../../api/rutasApi';

const DeleteRouteButton = ({ routeId, onRouteDeleted }) => {
    const [confirming, setConfirming] = useState(false);

    const handleDelete = async () => {
        try {
            await deleteRoute(routeId);
            onRouteDeleted(); // Llamada para actualizar la lista de rutas
            setConfirming(false);
        } catch (err) {
            console.error('Error al eliminar la ruta:', err.message);
        }
    };

    return (
        <div>
            {confirming ? (
                <>
                    <button onClick={handleDelete}>Confirmar</button>
                    <button onClick={() => setConfirming(false)}>Cancelar</button>
                </>
            ) : (
                <button onClick={() => setConfirming(true)}>Eliminar</button>
            )}
        </div>
    );
};

export default DeleteRouteButton;


