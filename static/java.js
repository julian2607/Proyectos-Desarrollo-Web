
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
            fetch('/get_contador')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('Juego1').textContent = data.contador[0];                       
                    document.getElementById('Juego2').textContent = data.contador[1];
                    document.getElementById('Turno').textContent = data.contador[3];
                    document.getElementById('Turno2').textContent = data.contador[3];
                    if(data.contador[2]=='True'){
                        document.getElementById('j1').textContent = 'Ganador';
                        document.getElementById('j2').textContent = 'Perdedor';
                        $scope.control=true;                        
                    }else{
                        document.getElementById('j1').textContent = 'Perdedor';
                        document.getElementById('j2').textContent = 'Ganador';
                    }
                    
                });                        
        }
        setInterval(actualizarContador, 1000);
});

//Redirigir a nueva magian con botor
// document.getElementById("Iniciar").addEventListener("click", function() {
//     // Redirigir a otra página
//     window.location.href = "http://127.0.0.1:5000/Pagina";
// });
