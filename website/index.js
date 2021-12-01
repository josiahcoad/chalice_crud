const api_endpoint = 'https://yli9sla9ie.execute-api.us-west-2.amazonaws.com/api/';

const showConfirmation = () => {
    document.getElementById('confirmation-section').innerText = 'Success!!';
}

const submitData = () => {
    // Get the data from each element on the form.
    const name = document.getElementById('txtName');
    const email = document.getElementById('txtEmail');
    const phone = document.getElementById('txtPhone');
    const pulocation = document.getElementById('txtPULoc');
    const msg = document.getElementById('msg');

    // This variable stores all the data.
    let data = {
        name: name.value,
        email: email.value,
        phone: phone.value,
        location: pulocation.value,
        message: msg.value
    }

    fetch(api_endpoint + 'items', {
        method: 'POST',
        body: JSON.stringify(data),
        headers: {
            'Content-Type': 'application/json'
        },
    })
        .then(response => response.json())
        .then(data => console.log(data));
    
    showConfirmation();
}

const showData = (payload) => {
    document.getElementById('data-dump').innerText = JSON.stringify(payload);
    console.log(payload);
}

const getData = () => {
    fetch(api_endpoint + 'items')
        .then(response => response.json())
        .then(showData);
}