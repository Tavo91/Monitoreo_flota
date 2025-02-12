import React from 'react';
import DeleteRouteButton from './DeleteRouteButton';

const RutasList = ({ routes, onRoutesUpdated }) => {
    return (
        <div>
            <h2>Lista de Rutas</h2>
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Origen</th>
                        <th>Destino</th>
                        <th>Distancia</th>
                        <th>Acciones</th>
                    </tr>
                </thead>
                <tbody>
                    {routes.map((route) => (
                        <tr key={route.id_ruta}>
                            <td>{route.id_ruta}</td>
                            <td>{route.origen}</td>
                            <td>{route.destino}</td>
                            <td>{route.distancia} km</td>
                            <td>
                                <button onClick={() => console.log('Editar', route.id_ruta)}>
                                    Editar
                                </button>
                                <DeleteRouteButton
                                    routeId={route.id_ruta}
                                    onRouteDeleted={onRoutesUpdated}
                                />
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default RutasList;







