import React from 'react';
import './InvoiceModal.css';

function InvoiceModal({ 
  selectedInvoice, 
  editData, 
  onClose, 
  onInputChange, 
  onSave, 
  onDelete 
}) {
  if (!selectedInvoice) return null;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        
        <div className="modal-header">
          <h2>Szczegóły Faktury</h2>
          <button className="close-btn" onClick={onClose}>✖</button>
        </div>

        <div className="modal-body">
          <div className="modal-image-container">
            <img 
              src={`http://127.0.0.1:8000/api/invoices/${selectedInvoice.id}/image/`} 
              alt="Podgląd faktury" 
              className="invoice-preview-img"
            />
          </div>

          <div className="modal-form-container">
            <form onSubmit={onSave} className="edit-form">
              <div className="form-group">
                <label>Numer faktury</label>
                <input type="text" name="invoice_number" value={editData.invoice_number || ''} onChange={onInputChange} />
              </div>
              <div className="form-group">
                <label>NIP Sprzedawcy</label>
                <input type="text" name="vendor_nip" value={editData.vendor_nip || ''} onChange={onInputChange} />
              </div>
              <div className="form-group">
                <label>NIP Nabywcy</label>
                <input type="text" name="buyer_nip" value={editData.buyer_nip || ''} onChange={onInputChange} />
              </div>
              <div className="form-group">
                <label>Kwota Brutto (PLN)</label>
                <input type="number" step="0.01" name="total_brutto" value={editData.total_brutto || ''} onChange={onInputChange} />
              </div>

              <div className="modal-actions">
                <button type="submit" className="save-btn">Zapisz poprawki</button>
                <button type="button" className="delete-btn" onClick={onDelete}>🗑 Usuń</button>
              </div>
            </form>
          </div>
        </div>

      </div>
    </div>
  );
}

export default InvoiceModal;