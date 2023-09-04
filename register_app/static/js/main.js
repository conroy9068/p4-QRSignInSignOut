//Function to create the new location 
function createLocation() {
    var name = $("#locationName").val();
    var address = $("#locationAddress").val();
    var description = $("#locationDescription").val();

    // AJAX post to Django view
    $.post("/create_location/", {name: name, address: address, description: description, csrfmiddlewaretoken: '{{ csrf_token }}'}, function(data){
        if (data.status === 'success') {
            location.reload();
        } else {
            alert("Error: " + data.errors);
        }
    });

    // Close the modal
    $("#createLocationModal").modal('hide');
}

