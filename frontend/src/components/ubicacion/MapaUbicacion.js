import React, { useEffect, useState, useRef } from "react";
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import L from "leaflet";

// 📌 Ícono personalizado para los vehículos
import carIconUrl from "../../assets/car-icon.png";

const customIcon = new L.Icon({
    iconUrl: carIconUrl,
    iconSize: [32, 32],
    iconAnchor: [16, 32],
    popupAnchor: [0, -32],
});

// 🚨 URL del WebSocket
const WS_URL = "ws://127.0.0.1:8000/api/ws/ubicacion";

const MapaUbicacion = () => {
    const [vehiculos, setVehiculos] = useState([]);
    const wsRef = useRef(null);
    const reconexionTimeout = useRef(null);
    const isConnected = useRef(false);

    useEffect(() => {
        const connectWebSocket = () => {
            if (wsRef.current && isConnected.current) {
                console.log("⚠️ WebSocket ya está conectado, evitando duplicaciones.");
                return;
            }

            wsRef.current = new WebSocket(WS_URL);

            wsRef.current.onopen = () => {
                console.log("🟢 Conectado al WebSocket de ubicación.");
                isConnected.current = true;
            };

            wsRef.current.onmessage = (event) => {
                try {
                    const data = JSON.parse(event.data);
                    console.log("📡 Datos recibidos del WebSocket:", data);

                    if (data.status === "WebSocket activo") return;

                    if (!Array.isArray(data)) return;

                    setVehiculos(data);
                } catch (error) {
                    console.error("❌ Error procesando los datos del WebSocket:", error);
                }
            };

            wsRef.current.onclose = () => {
                console.warn("🔴 WebSocket desconectado.");
                isConnected.current = false;
                attemptReconnect();
            };
        };

        const attemptReconnect = () => {
            if (!reconexionTimeout.current) {
                reconexionTimeout.current = setTimeout(connectWebSocket, 5000);
            }
        };

        connectWebSocket();

        return () => {
            if (wsRef.current) wsRef.current.close();
        };
    }, []);

    return (
        <MapContainer center={[6.2518, -75.5636]} zoom={12} style={{ height: "500px", width: "100%" }}>
            <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
            {vehiculos.map((vehiculo, index) => {
                const [lat, lon] = vehiculo.ubicacion.split(",").map(Number);
                return (
                    <Marker key={index} position={[lat, lon]} icon={customIcon}>
                        <Popup>{vehiculo.placa}</Popup>
                    </Marker>
                );
            })}
        </MapContainer>
    );
};

export default MapaUbicacion;









