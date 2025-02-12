import React, { useState } from 'react';
import { updateRoute } from '../../../api/rutasApi';

const UpdateRouteForm = ({ route, onClose, onRouteUpdated }) => {
    const [formData, setFormData] = useState(route);

    const handleInputChange = (event) => {
        const { name, value } = event.target;
        setFormData({ ...formData, [name]: value });
    };

    const handleSubmit = async (event) => {
        event.preventDefault();
        try {
            await updateRoute(formData);
            onRouteUpdated();
        } catch (err) {
            console.error('Error al actualizar la ruta:', err.message);
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <h2>Actualizar Ruta</h2>
            <label>
                Origen:
                <input type="text" name="origen" value={formData.origen} onChange={handleInputChange} />
            </label>
            <label>
                Destino:
                <input type="text" name="destino" value={formData.destino} onChange={handleInputChange} />
            </label>
            <label>
                Distancia:
                <input type="number" name="distancia" value={formData.distancia} onChange={handleInputChange} />
            </label>
            <button type="submit">Guardar</button>
            <button type="button" onClick={onClose}>Cancelar</button>
        </form>
    );
};

export default UpdateRouteForm;


