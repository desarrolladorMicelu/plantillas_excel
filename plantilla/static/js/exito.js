document.addEventListener('DOMContentLoaded', function() {
    const selectPlataforma = document.getElementById('plataforma');
    const exitoContent = document.getElementById('exito-content');
    const selectExitoCelulares = document.getElementById('exito-celulares');
    const listaSeleccionadosExito = document.getElementById('lista-seleccionados-exito');
    const descargarExitoBtn = document.getElementById('descargar-exito');
    let selectedExitoItems = new Map();

    if (selectPlataforma) {
        selectPlataforma.addEventListener('change', function() {
            if (this.value === 'exito') {
                exitoContent.style.display = 'block';
                document.getElementById('micelu-content').style.display = 'none';
                document.getElementById('falabella-content').style.display = 'none';
                document.getElementById('bancolombia-content').style.display = 'none';
            } else {
                exitoContent.style.display = 'none';
            }
        });
    }

    if (selectExitoCelulares) {
        selectExitoCelulares.addEventListener('change', function() {
            const selectedEan = this.value;
            if (selectedEan) {
                const selectedOption = this.options[this.selectedIndex];
                const productName = selectedOption.text;
                if (!selectedExitoItems.has(selectedEan)) {
                    selectedExitoItems.set(selectedEan, { ean: selectedEan, nombre: productName });
                    updateSelectedExitoList();
                }
            }
        });
    }

    function updateSelectedExitoList() {
        listaSeleccionadosExito.innerHTML = '';
        selectedExitoItems.forEach(item => {
            const li = document.createElement('li');
            li.className = 'selected-item';

            const itemText = document.createElement('span');
            itemText.textContent = `${item.nombre} (EAN: ${item.ean})`;
            li.appendChild(itemText);

            const deleteBtn = document.createElement('button');
            deleteBtn.textContent = 'Eliminar';
            deleteBtn.className = 'delete-btn';
            deleteBtn.addEventListener('click', function() {
                selectedExitoItems.delete(item.ean);
                updateSelectedExitoList();
            });
            li.appendChild(deleteBtn);

            listaSeleccionadosExito.appendChild(li);
        });
    }

    if (descargarExitoBtn) {
        descargarExitoBtn.addEventListener('click', function() {
            console.log('Iniciando descarga de productos Éxito seleccionados');

            const selectedEans = Array.from(selectedExitoItems.keys());

            fetch('/descargar_exito', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ eans: selectedEans }),
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
                a.download = 'productos_exito_seleccionados.xlsx';
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Hubo un error al descargar los productos seleccionados de Éxito: ' + error.message);
            });
        });
    }
});