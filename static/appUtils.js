function delete_item(id){
    fetch("/items/"+id,{
        method:'DELETE',})
    .then(function (response){
        if (response.status == 202) {
            window.location = "/items"
            }
        })
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
    fetch("/items/add", options)
    .then(function (response){
    if (response.status == 201) {
        window.location = "/items"
        }
    })
}

function update_item(){
    const todoForm = document.getElementById("todoAdd");
    const formData = new FormData(todoForm);
    const data = new URLSearchParams();
    for (const pair of formData) {
        data.append(pair[0], pair[1]);
    }
    alert("data="+ data)
    let options = {
            method: 'POST',
            headers: {
                'Content-Type':
                    'application/x-www-form-urlencoded; charset=UTF-8'
            },
            body: data
        }
    fetch("/items/add", options)
    .then(function (response){
    if (response.status == 201) {
        window.location = "/items"
        }
    })
}