function delete_item(id){
    fetch("/items/"+id,{
        method:'DELETE',})
    .then(function (response){
        if (response.status == 202) {
            window.location = "/items"
            }
        })
}

function view_item(id){
    window.location = "/items/"+id
}

function add_item(){
    const todoForm = document.getElementById("todoAdd");
    const formData = new FormData(todoForm);
    var object = {};
    formData.forEach(function(value, key){
        object[key] = value;
    });
    var jsonData = JSON.stringify(object);
    let options = {
            method: 'POST',
            headers: {
                'Content-Type':
                    'application/json'
            },
            body: jsonData
        }
    fetch("/items/add-update", options)
    .then(function (response){
    if (response.status == 201) {
        window.location = "/items"
        }
    })
}

function update_item(id){
    const todoForm = document.getElementById("todoAdd");
    const formData = new FormData(todoForm);
    var object = {};
    formData.forEach(function(value, key){
        object[key] = value;
    });
    var jsonData = JSON.stringify(object);
    let options = {
            method: 'PATCH',
            headers: {
                'Content-Type':
                    'application/json'
            },
            body: jsonData
        }
    fetch("/items/"+id, options)
    .then(function (response){
    if (response.status == 200) {
        window.location = "/items"
        }
    })
}

function redirectUrl(url){
    window.location = url
}