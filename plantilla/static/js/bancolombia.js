document.addEventListener('DOMContentLoaded', function() {
    const selectPlataforma = document.getElementById('plataforma');
    const falabellaContent = document.getElementById('falabella-content');
    const bancolombiaContent = document.getElementById('bancolombia-content');
    const selectFalabellaCelulares = document.getElementById('falabella-celulares');
    const selectBancolombiaCelulares = document.getElementById('bancolombia-celulares');
    const listaSeleccionadosFalabella = document.getElementById('lista-seleccionados-falabella');
    const listaSeleccionadosBancolombia = document.getElementById('lista-seleccionados-bancolombia');
    const descargarFalabellaBtn = document.getElementById('descargar-falabella');
    const descargarBancolombiaBtn = document.getElementById('descargar-bancolombia');
    let selectedFalabellaItems = new Map();
    let selectedBancolombiaItems = new Map();

    if (selectPlataforma) {
        selectPlataforma.addEventListener('change', function() {
            if (this.value === 'falabella') {
                falabellaContent.style.display = 'block';
                bancolombiaContent.style.display = 'none';
            } else if (this.value === 'bancolombia') {
                falabellaContent.style.display = 'none';
                bancolombiaContent.style.display = 'block';
            } else {
                falabellaContent.style.display = 'none';
                bancolombiaContent.style.display = 'none';
            }
        });
    }

    if (selectFalabellaCelulares) {
        selectFalabellaCelulares.addEventListener('change', function() {
            handleSelectChange(this, selectedFalabellaItems, listaSeleccionadosFalabella);
        });
    }

    if (selectBancolombiaCelulares) {
        selectBancolombiaCelulares.addEventListener('change', function() {
            handleSelectChange(this, selectedBancolombiaItems, listaSeleccionadosBancolombia);
        });
    }

    function handleSelectChange(selectElement, selectedItems, listElement) {
        const selectedId = selectElement.value;
        if (selectedId) {
            const selectedOption = selectElement.options[selectElement.selectedIndex];
            const productName = selectedOption.text;
            if (!selectedItems.has(selectedId)) {
                selectedItems.set(selectedId, { id: selectedId, nombre: productName });
                updateSelectedList(selectedItems, listElement);
            }
        }
    }

    function updateSelectedList(selectedItems, listElement) {
        listElement.innerHTML = '';
        selectedItems.forEach(item => {
            const li = document.createElement('li');
            li.className = 'selected-item';

            const itemText = document.createElement('span');
            itemText.textContent = `${item.nombre} (ID: ${item.id})`;
            li.appendChild(itemText);

            const deleteBtn = document.createElement('button');
            deleteBtn.textContent = 'Eliminar';
            deleteBtn.className = 'delete-btn';
            deleteBtn.addEventListener('click', function() {
                selectedItems.delete(item.id);
                updateSelectedList(selectedItems, listElement);
            });
            li.appendChild(deleteBtn);

            listElement.appendChild(li);
        });
    }

    if (descargarFalabellaBtn) {
        descargarFalabellaBtn.addEventListener('click', function() {
            downloadSelectedItems(selectedFalabellaItems, '/descargar_falabella', 'productos_falabella_seleccionados.xlsx');
        });
    }

    if (descargarBancolombiaBtn) {
        descargarBancolombiaBtn.addEventListener('click', function() {
            downloadSelectedItems(selectedBancolombiaItems, '/descargar_bancolombia', 'productos_bancolombia_seleccionados.xlsx');
        });
    }

    function downloadSelectedItems(selectedItems, endpoint, filename) {
        console.log(`Iniciando descarga de productos seleccionados`);

        const selectedIds = Array.from(selectedItems.keys());

        fetch(endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ ids: selectedIds }),
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
            a.download = filename;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
        })
        .catch(error => {
            console.error('Error:', error);
            alert(`Hubo un error al descargar los productos seleccionados: ${error.message}`);
        });
    }
});