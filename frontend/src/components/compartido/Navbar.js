import React from 'react';
import { Link } from 'react-router-dom';

const Navbar = () => {
  return (
    <nav style={styles.navbar}>
      <ul style={styles.navList}>
        <li style={styles.navItem}>
          <Link to="/" style={styles.navLink}>Inicio</Link>
        </li>
        <li style={styles.navItem}>
          <Link to="/vehiculos" style={styles.navLink}>Gestión de Vehículos</Link>
        </li>
        <li style={styles.navItem}>
          <Link to="/rutas" style={styles.navLink}>Gestión de Rutas</Link>
        </li>
      </ul>
    </nav>
  );
};

const styles = {
  navbar: {
    backgroundColor: '#333',
    padding: '1rem',
    textAlign: 'center',
  },
  navList: {
    listStyle: 'none',
    margin: 0,
    padding: 0,
    display: 'flex',
    justifyContent: 'center',
  },
  navItem: {
    margin: '0 1rem',
  },
  navLink: {
    color: '#fff',
    textDecoration: 'none',
    fontSize: '1.2rem',
  },
};

export default Navbar;
