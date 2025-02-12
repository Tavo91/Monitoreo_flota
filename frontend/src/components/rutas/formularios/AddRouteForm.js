import React, { useState } from 'react';
import { addRoute } from '../../../api/rutasApi';

const AddRouteForm = ({ onRouteAdded, onCancel }) => {
    const [formData, setFormData] = useState({
        origen: '',
        destino: '',
        distancia: '',
    });
    const [error, setError] = useState(null);

    const handleInputChange = (event) => {
        const { name, value } = event.target;
        setFormData({ ...formData, [name]: value });
    };

    const handleSubmit = async (event) => {
        event.preventDefault();
        setError(null);

        try {
            const addedRoute = await addRoute(formData);
            console.log('Ruta agregada:', addedRoute);
            onRouteAdded();
            setFormData({ origen: '', destino: '', distancia: '' });
        } catch (err) {
            console.error('Error al agregar la ruta:', err.message);
            setError(err.message);
        }
    };

    const handleCancel = () => {
        setFormData({ origen: '', destino: '', distancia: '' });
        setError(null);
        onCancel();
    };

    return (
        <form onSubmit={handleSubmit}>
            <h2>Agregar Ruta</h2>
            <label>
                Origen:
                <input
                    type="text"
                    name="origen"
                    value={formData.origen}
                    onChange={handleInputChange}
                />
            </label>
            <label>
                Destino:
                <input
                    type="text"
                    name="destino"
                    value={formData.destino}
                    onChange={handleInputChange}
                />
            </label>
            <label>
                Distancia:
                <input
                    type="number"
                    name="distancia"
                    value={formData.distancia}
                    onChange={handleInputChange}
                />
            </label>
            <div>
                <button type="submit">Agregar</button>
                <button type="button" onClick={handleCancel}>
                    Cancelar
                </button>
            </div>
            {error && <p style={{ color: 'red' }}>{error}</p>}
        </form>
    );
};

export default AddRouteForm;

