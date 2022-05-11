// See if counter is in storage, if not set counter = 0
if(!localStorage.getItem('counter')){
    localStorage.setItem('counter', 0);
}
// Timer function
function timer() {
    let counter = localStorage.getItem('counter');
    counter++;
    document.querySelector('#timer').innerHTML = `${counter}`; // template literal
    localStorage.setItem('counter', counter);
}

// Fixes issue where user refreshes page and timer momentarily is 0
// document.querySelector('DOMContentLoaded', function() {
//     document.querySelector('#timer').innerHTML = localStorage.getItem('counter');
// })


// Listening to keypresses and restricting UI, try implementing it with forEach! 
document.addEventListener('DOMContentLoaded', function(){
    document.querySelector('#number1').onkeyup = function() {
        if(this.value.length > 1){
            this.value = this.value.slice(0,1);
        }
        document.querySelector('#timer').innerHTML = localStorage.getItem('counter');
        setInterval(timer, 1000);
    }
    document.querySelector('#number2').onkeyup = function() {
        if(this.value.length > 1){
            this.value = this.value.slice(0,1);
        }
    }
    document.querySelector('#number3').onkeyup = function() {
        if(this.value.length > 1){
            this.value = this.value.slice(0,1);
        }
    }
    document.querySelector('#number4').onkeyup = function() {
        setInterval(timer, 1000);
        
        if(document.querySelector('#number4').value.length > 0){
            document.querySelector('#timer_button').disabled = false;
            this.value = this.value.slice(0,1);
        }
        else{
            document.querySelector('#timer_button').disabled = true;
        }
    }
});

// Clock Pacific Time
// setInterval(function, milliseconds) 1000ms == 1 second
setInterval(myClock, 1000);

function myClock() {
const d = new Date();
document.getElementById("clock").innerHTML = d.toLocaleTimeString() + '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;';
}


// Fetching Number from RANDOM's API using JS
// JSON, exchange of information in terms of objects
// AJAX, asynchronous requests
document.addEventListener('DOMContentLoaded', function() {
    // fetch gives back to us a promise, which means its not immediately
    fetch('https://www.random.org/integers/?num=4&min=0&max=7&col=4&base=10&format=plain&rnd=new')
    // when the promise comes back because it's asynchronous
    .then(response => {
        return response.text()
    })
    // then once we have the data
    .then(data => {
        console.log(data);
        const num1 = data[0]
        if(num1 != undefined){
            console.log(data[0]);
        }
        console.log(data[2]);
        console.log(data[4]);
        console.log(data[6]);
    })

    // if something goes awry :(
    .catch(error => {
        console.log('Error:', error);
    });
})