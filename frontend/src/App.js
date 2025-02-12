import React from 'react';
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Navbar from './components/compartido/Navbar'; // Importar Navbar
import Vehiculos from './components/vehiculos/Vehiculos';
import UbicacionScreen from './components/ubicacion/MapaUbicacion';
import Rutas from './components/rutas/Rutas';
import MapaUbicacion from './components/ubicacion/MapaUbicacion';

const App = () => {
  return (
    <Router>
      <Navbar /> {/* Coloca la barra de navegación aquí */}
      <Routes>
        <Route path="/" element={<h1>Bienvenido al Sistema de Gestión</h1>} />
        <Route path="/vehiculos" element={<Vehiculos />} />
        <Route path="/rutas" element={<Rutas />} />
        <Route path="/ubicacion" element={<MapaUbicacion />} />
        <Route path="/ubicacion/:idVehiculo" element={<MapaUbicacion  />} />
        <Route path="/ubicacion" element={<MapaUbicacion  />} />
      </Routes>
    </Router>
  );
};

export default App;


