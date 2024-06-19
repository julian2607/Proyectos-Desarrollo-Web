
// Alertas
const alertPlaceholder = document.getElementById('liveAlertPlaceholder')
const appendAlert = (message, type) => {
const wrapper = document.createElement('div')
wrapper.innerHTML = [
    `<div class="alert alert-${type} alert-dismissible" role="alert">`,
    `   <div>${message}</div>`,
    '   <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>',
    '</div>'
].join('')

alertPlaceholder.append(wrapper)
}

const alertTrigger = document.getElementById('liveAlertBtn')
if (alertTrigger) {
alertTrigger.addEventListener('click', () => {
    appendAlert('Nice, you triggered this alert message!', 'success')
})
}

angular.module('myApp', [])
        .controller('myCtrl', function ($scope, $http, $timeout) {
            $scope.control=true;            
        // Actualizar Front
        function actualizarContador() {  
            $scope.control=false;      
            fetch('/get_Informacion')
                .then(response => response.json())
                .then(data => {
                    var tablaHtml = data.contador;
                    document.getElementById('TablaInfo').innerHTML = tablaHtml;                                                                                 
                });                        
        }
        setInterval(actualizarContador, 1000);
});

//Redirigir a nueva magian con botor
document.getElementById("Iniciar").addEventListener("click", function() {
    // Redirigir a otra página
    window.location.href = "http://127.0.0.1:5000/PaginaIniciar";
});

// PDF
document.getElementById("PDF").addEventListener("click", function() {
    // Redirigir a otra página
    window.location.href = "http://127.0.0.1:5000/PDF";
});

//EXCEL
document.getElementById("EXCEL").addEventListener("click", function() {
    // Redirigir a otra página
    window.location.href = "http://127.0.0.1:5000/EXCEL";
});
