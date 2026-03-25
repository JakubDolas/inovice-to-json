import { useState, useEffect } from 'react'
import axios from 'axios'
import './App.css'

import InvoiceModal from "./components/InvoiceModal"

function App() {
  const [invoices, setInvoices] = useState([])
  const [selectedFile, setSelectedFile] = useState(null)
  const [isUploading, setIsUploading] = useState(false)
  
  const [selectedInvoice, setSelectedInvoice] = useState(null)
  const [editData, setEditData] = useState({})

  const fetchInvoices = () => {
    axios.get('http://127.0.0.1:8000/api/invoices/')
      .then(response => setInvoices(response.data))
      .catch(error => console.error("Błąd podczas pobierania danych:", error))
  }

  useEffect(() => {
    fetchInvoices()
  }, [])

  const handleFileChange = (event) => setSelectedFile(event.target.files[0])

  const handleUpload = async (event) => {
    event.preventDefault()
    if (!selectedFile) {
      alert("Proszę najpierw wybrać plik faktury!")
      return
    }
    const formData = new FormData()
    formData.append('invoice_image', selectedFile)
    setIsUploading(true)

    try {
      await axios.post('http://127.0.0.1:8000/api/process-invoice/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })
      setSelectedFile(null)
      fetchInvoices()
    } catch (error) {
      console.error("Błąd wysyłania:", error)
      alert("Wystąpił błąd podczas przetwarzania faktury.")
    } finally {
      setIsUploading(false)
    }
  }

  const openDetails = (invoice) => {
    setSelectedInvoice(invoice)
    setEditData(invoice)
  }

  const closeDetails = () => setSelectedInvoice(null)

  const handleInputChange = (e) => {
    const { name, value } = e.target
    setEditData({ ...editData, [name]: value })
  }

  const handleSaveChanges = async (e) => {
    e.preventDefault()
    try {
      await axios.put(`http://127.0.0.1:8000/api/invoices/${selectedInvoice.id}/`, editData)
      fetchInvoices()
      closeDetails()
    } catch (error) {
      console.error("Błąd aktualizacji:", error)
      alert("Nie udało się zaktualizować faktury.")
    }
  }

  const handleDelete = async () => {
    if (window.confirm("Czy na pewno chcesz usunąć tę fakturę bezpowrotnie?")) {
      try {
        await axios.delete(`http://127.0.0.1:8000/api/invoices/${selectedInvoice.id}/`)
        fetchInvoices()
        closeDetails()
      } catch (error) {
        console.error("Błąd usuwania:", error)
        alert("Nie udało się usunąć faktury.")
      }
    }
  }

  return (
    <div className="dashboard">
      <header className="header">
        <h1>InvoiceLens</h1>
      </header>

      <main className="main-content">
        <section className="upload-section card">
          <h2>Wgraj nową fakturę</h2>
          <form onSubmit={handleUpload} className="upload-form">
            <input type="file" accept="image/*" onChange={handleFileChange} className="file-input" />
            <button type="submit" className="upload-btn" disabled={isUploading}>
              {isUploading ? "Analizowanie..." : "Przetwórz fakturę"}
            </button>
          </form>
        </section>

        <section className="invoices-section">
          <h2>Przetworzone dokumenty</h2>
          <div className="invoice-grid">
            {invoices.length === 0 ? (
              <p className="no-data">Brak faktur w bazie.</p>
            ) : (
              invoices.map((invoice) => (
                <div key={invoice.id} className="invoice-card">
                  <div className="invoice-header">
                    <h3>{invoice.invoice_number || "Brak numeru"}</h3>
                    <span className="badge">Przetworzono</span>
                  </div>
                  <div className="invoice-body">
                    <p><strong>NIP Sprzedawcy:</strong> {invoice.vendor_nip || "Nie wykryto"}</p>
                    <p><strong>Kwota:</strong> {invoice.total_brutto} PLN</p>
                  </div>
                  <div className="invoice-footer">
                    <button className="details-btn" onClick={() => openDetails(invoice)}>
                      Podgląd i Edycja
                    </button>
                  </div>
                </div>
              ))
            )}
          </div>
        </section>
      </main>

      <InvoiceModal 
        selectedInvoice={selectedInvoice}
        editData={editData}
        onClose={closeDetails}
        onInputChange={handleInputChange}
        onSave={handleSaveChanges}
        onDelete={handleDelete}
      />
      
    </div>
  )
}

export default App