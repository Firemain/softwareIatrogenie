
$(document).ready(function () {
    data = {
        indexPatient:2
    }

    $("#test").click(function(event){
        $.ajax({
            type: 'POST',
            url: '/requeteIatro',
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify(data),
            success: function(response) {
                console.log(response);
                alert(response.message);
            },
            error: function(error) {
                console.error(error);
                alert('Erreur lors de la requête.');
            }
        });
    })
    


})