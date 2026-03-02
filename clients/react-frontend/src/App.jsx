import { useState, useEffect } from 'react'
import axios from 'axios'
import './App.css'

const API_URL = 'http://localhost:8000'

function App() {
  const [vehicles, setVehicles] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [showForm, setShowForm] = useState(false)
  const [formData, setFormData] = useState({
    matricula: '',
    vin: '',
    modelo: '',
    marca: '',
    tipo: ''
  })

  useEffect(() => {
    fetchVehicles()
  }, [])

  const fetchVehicles = async () => {
    setLoading(true)
    setError(null)
    try {
      const response = await axios.get(`${API_URL}/vehicles`)
      setVehicles(response.data)
    } catch (err) {
      setError('Error al cargar vehículos: ' + err.message)
    } finally {
      setLoading(false)
    }
  }

  const handleInputChange = (e) => {
    const { name, value } = e.target
    setFormData({ ...formData, [name]: value })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    try {
      await axios.post(`${API_URL}/vehicles`, formData)
      setFormData({
        matricula: '',
        vin: '',
        modelo: '',
        marca: '',
        tipo: ''
      })
      setShowForm(false)
      fetchVehicles()
    } catch (err) {
      setError('Error al crear vehículo: ' + (err.response?.data?.detail || err.message))
    } finally {
      setLoading(false)
    }
  }

  const handleDelete = async (matricula) => {
    if (!confirm(`¿Eliminar vehículo ${matricula}?`)) return
    setLoading(true)
    setError(null)
    try {
      await axios.delete(`${API_URL}/vehicles/${matricula}`)
      fetchVehicles()
    } catch (err) {
      setError('Error al eliminar vehículo: ' + (err.response?.data?.detail || err.message))
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app">
      <header className="header">
        <h1>Sistema de Gestión de Vehículos</h1>
        <p className="subtitle">Administración de flota vehicular</p>
      </header>

      <main className="main-content">
        <div className="actions-bar">
          <button
            className="btn btn-primary"
            onClick={() => setShowForm(!showForm)}
            disabled={loading}
          >
            {showForm ? '✕ Cancelar' : '+ Nuevo Vehículo'}
          </button>
          <button
            className="btn btn-secondary"
            onClick={fetchVehicles}
            disabled={loading}
          >
            🔄 Actualizar
          </button>
        </div>

        {error && (
          <div className="alert alert-error">
            <strong>⚠️ Error:</strong> {error}
            <button className="alert-close" onClick={() => setError(null)}>✕</button>
          </div>
        )}

        {showForm && (
          <div className="form-container">
            <h2>Registrar Nuevo Vehículo</h2>
            <form onSubmit={handleSubmit} className="vehicle-form">
              <div className="form-row">
                <div className="form-group">
                  <label htmlFor="matricula">Matrícula *</label>
                  <input
                    type="text"
                    id="matricula"
                    name="matricula"
                    value={formData.matricula}
                    onChange={handleInputChange}
                    required
                    placeholder="ABC-123"
                  />
                </div>
                <div className="form-group">
                  <label htmlFor="vin">VIN *</label>
                  <input
                    type="text"
                    id="vin"
                    name="vin"
                    value={formData.vin}
                    onChange={handleInputChange}
                    required
                    placeholder="1HGBH41JXMN109186"
                  />
                </div>
              </div>
              <div className="form-row">
                <div className="form-group">
                  <label htmlFor="marca">Marca *</label>
                  <input
                    type="text"
                    id="marca"
                    name="marca"
                    value={formData.marca}
                    onChange={handleInputChange}
                    required
                    placeholder="Toyota"
                  />
                </div>
                <div className="form-group">
                  <label htmlFor="modelo">Modelo *</label>
                  <input
                    type="text"
                    id="modelo"
                    name="modelo"
                    value={formData.modelo}
                    onChange={handleInputChange}
                    required
                    placeholder="Corolla 2024"
                  />
                </div>
              </div>
              <div className="form-group">
                <label htmlFor="tipo">Tipo *</label>
                <select
                  id="tipo"
                  name="tipo"
                  value={formData.tipo}
                  onChange={handleInputChange}
                  required
                >
                  <option value="">Seleccionar tipo...</option>
                  <option value="Sedán">Sedán</option>
                  <option value="SUV">SUV</option>
                  <option value="Pickup">Pickup</option>
                  <option value="Hatchback">Hatchback</option>
                  <option value="Deportivo">Deportivo</option>
                  <option value="Camioneta">Camioneta</option>
                </select>
              </div>
              <div className="form-actions">
                <button type="submit" className="btn btn-success" disabled={loading}>
                  {loading ? '⏳ Guardando...' : '✓ Guardar Vehículo'}
                </button>
              </div>
            </form>
          </div>
        )}

        <div className="vehicles-section">
          <h2>Lista de Vehículos ({vehicles.length})</h2>
          {loading && <div className="loading">⏳ Cargando...</div>}

          {!loading && vehicles.length === 0 && (
            <div className="empty-state">
              <p>No hay vehículos registrados</p>
              <p className="empty-hint">Haz clic en "Nuevo Vehículo" para agregar uno</p>
            </div>
          )}

          {!loading && vehicles.length > 0 && (
            <div className="table-container">
              <table className="vehicles-table">
                <thead>
                  <tr>
                    <th>Matrícula</th>
                    <th>VIN</th>
                    <th>Marca</th>
                    <th>Modelo</th>
                    <th>Tipo</th>
                    <th>Acciones</th>
                  </tr>
                </thead>
                <tbody>
                  {vehicles.map((vehicle) => (
                    <tr key={vehicle.matricula}>
                      <td><strong>{vehicle.matricula}</strong></td>
                      <td className="vin-cell">{vehicle.vin}</td>
                      <td>{vehicle.marca}</td>
                      <td>{vehicle.modelo}</td>
                      <td><span className="badge">{vehicle.tipo}</span></td>
                      <td>
                        <button
                          className="btn btn-danger btn-sm"
                          onClick={() => handleDelete(vehicle.matricula)}
                          disabled={loading}
                        >
                          🗑️ Eliminar
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </main>

    </div>
  )
}

export default App
