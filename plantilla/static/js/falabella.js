document.addEventListener('DOMContentLoaded', function() {
    const selectPlataforma = document.getElementById('plataforma');
    const falabellaContent = document.getElementById('falabella-content');
    const selectFalabellaCelulares = document.getElementById('falabella-celulares');
    const listaSeleccionadosFalabella = document.getElementById('lista-seleccionados-falabella');
    const descargarFalabellaBtn = document.getElementById('descargar-falabella');
    let selectedFalabellaItems = new Map();

    if (selectPlataforma) {
        selectPlataforma.addEventListener('change', function() {
            if (this.value === 'falabella') {
                falabellaContent.style.display = 'block';
                document.getElementById('micelu-content').style.display = 'none';
            } else if (this.value === 'micelu') {
                falabellaContent.style.display = 'none';
                document.getElementById('micelu-content').style.display = 'block';
            } else {
                falabellaContent.style.display = 'none';
                document.getElementById('micelu-content').style.display = 'none';
            }
        });
    }

    if (selectFalabellaCelulares) {
        selectFalabellaCelulares.addEventListener('change', function() {
            const selectedSku = this.value;
            if (selectedSku) {
                const selectedOption = this.options[this.selectedIndex];
                const productName = selectedOption.text;
                if (!selectedFalabellaItems.has(selectedSku)) {
                    selectedFalabellaItems.set(selectedSku, { sku: selectedSku, nombre: productName });
                    updateSelectedFalabellaList();
                }
            }
        });
    }

    function updateSelectedFalabellaList() {
        listaSeleccionadosFalabella.innerHTML = '';
        selectedFalabellaItems.forEach(item => {
            const li = document.createElement('li');
            li.className = 'selected-item';

            const itemText = document.createElement('span');
            itemText.textContent = `${item.nombre} (SKU: ${item.sku})`;
            li.appendChild(itemText);

            const deleteBtn = document.createElement('button');
            deleteBtn.textContent = 'Eliminar';
            deleteBtn.className = 'delete-btn';
            deleteBtn.addEventListener('click', function() {
                selectedFalabellaItems.delete(item.sku);
                updateSelectedFalabellaList();
            });
            li.appendChild(deleteBtn);

            listaSeleccionadosFalabella.appendChild(li);
        });
    }

    if (descargarFalabellaBtn) {
        descargarFalabellaBtn.addEventListener('click', function() {
            console.log('Iniciando descarga de productos Falabella seleccionados');

            // Convert the Map to an array of SKUs
            const selectedSkus = Array.from(selectedFalabellaItems.keys());

            fetch('/descargar_falabella', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ skus: selectedSkus }),
            })
            .then(response => {
                if (!response.ok) {
                    return response.json().then(errData => {
                        throw new Error(errData.error || 'Error desconocido en la descarga');
                    });
                }
                return response.blob();
            })
            .then(blob => {
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.style.display = 'none';
                a.href = url;
                a.download = 'productos_falabella_seleccionados.xlsx';
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Hubo un error al descargar los productos seleccionados de Falabella: ' + error.message);
            });
        });
    }
});