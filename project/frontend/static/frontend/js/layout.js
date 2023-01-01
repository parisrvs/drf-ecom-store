var prevent_default = false;
window.addEventListener('beforeunload', function (e) {
    if (prevent_default) {
        e.preventDefault();
        e.returnValue = 'Are you sure you want to cancel this process?';
    }
    return;
});


document.addEventListener("DOMContentLoaded", ()=>{
    check_authentication();

});


function check_authentication() {
    if (!localStorage.getItem("authentication")) {
        const details_template = Handlebars.compile(document.querySelector('#loginAuthenticationDivHandlebar').innerHTML);
        const details = details_template();
        document.querySelector("#navBarAuthenticationDiv").innerHTML = details;
    }
}


function displayLoginModal() {
    const details_template = Handlebars.compile(document.querySelector('#loginModalBodyFormHandlebar').innerHTML);
    const details = details_template();
    document.querySelector("#loginModalBody").innerHTML = details;
    document.querySelector("#loginModalBtn").click();
    autofocus_modal('loginModal', 'login_email_FormInput')
    return false;
}

function displayRecoverModal() {
    const details_template = Handlebars.compile(document.querySelector('#recoverModalBodyFormHandlebar').innerHTML);
    const details = details_template();
    document.querySelector("#recoverModalBody").innerHTML = details;
    document.querySelector("#recoverModalBtn").click();
    autofocus_modal('recoverModal', 'recover_email_FormInput')
    return false;
}

function displayRegisterModal() {
    const details_template = Handlebars.compile(document.querySelector('#registerModalBodyFormHandlebar').innerHTML);
    const details = details_template();
    document.querySelector("#registerModalBody").innerHTML = details;
    document.querySelector("#registerModalBtn").click();
    autofocus_modal('registerModal', 'register_first_name_FormInput')
    return false;
}

function login() {
    return false;
}

function register() {

    let FirstName = document.querySelector("#register_first_name_FormInput").value.replace(/^\s+|\s+$/g, '');
    let LastName = document.querySelector("#register_last_name_FormInput").value.replace(/^\s+|\s+$/g, '');
    let Email = document.querySelector("#register_email_FormInput").value.replace(/^\s+|\s+$/g, '');
    let Username = document.querySelector("#register_username_FormInput").value.replace(/^\s+|\s+$/g, '');
    let Password = document.querySelector("#register_password_FormInput").value.replace(/^\s+|\s+$/g, '');
    let RePassword = document.querySelector("#register_re_password_FormInput").value.replace(/^\s+|\s+$/g, '');

    if (checkForBlankValuesRegister(FirstName, LastName, Email, Username, Password, RePassword)) {
        document.querySelector("#registerFormErrorMessage").innerHTML = "Incomplete Form";
        return false;
    } else {
        document.querySelector("#registerFormErrorMessage").innerHTML = '';
    }

    if (Password != RePassword) {
        document.querySelector("#registerFormErrorMessage").innerHTML = "Passwords don't match.";
        document.querySelector("#register_password_FormInput").style.borderColor = 'red';
        document.querySelector("#register_re_password_FormInput").style.borderColor = 'red';
        return false;
    } else {
        document.querySelector("#register_password_FormInput").style.borderColor = '';
        document.querySelector("#register_re_password_FormInput").style.borderColor = '';
        document.querySelector("#registerFormErrorMessage").innerHTML = '';
    }

    const request = new XMLHttpRequest();
    request.open('POST', '/api/auth/users/');

    disable();
    prevent_default = true;

    request.onload = () => {
        enable();
        prevent_default = false;
        if (request.status === 400) {
            displayErrorMessagesRegister(JSON.parse(request.responseText));
        } else if (request.status === 201) {
            document.querySelector("#registerModalCloseBtn").click();
            document.querySelector("#registerSuccessModalBtn").click();
            // console.log(JSON.parse(request.responseText));
        }
    };

    const data = new FormData();
    data.append('email', Email);
    data.append('first_name', FirstName);
    data.append('last_name', LastName);
    data.append('username', Username);
    data.append('password', Password);
    request.send(data);
    return false;
}


function displayErrorMessagesRegister(obj) {

    document.querySelectorAll(".form-control").forEach(i => {
        i.style.borderColor = '';
    })

    document.querySelectorAll(".form-text").forEach(d => {
        d.innerHTML = '';
    })

    for (let key in obj) {
        document.querySelector(`#register_${key}_FormInput`).style.borderColor = 'red';
        document.querySelector(`#register_${key}_FormInputHelp`).innerHTML = obj[key];
    }
}


function checkForBlankValuesRegister(first_name, last_name, email, username, password, re_password) {
    let blank = false;

    if (!first_name) {
        document.querySelector("#register_first_name_FormInput").style.borderColor = 'red';
        blank = true;
    } else {
        document.querySelector("#register_first_name_FormInput").style.borderColor = '';
    }

    if (!last_name) {
        document.querySelector("#register_last_name_FormInput").style.borderColor = 'red';
        blank = true;
    } else {
        document.querySelector("#register_last_name_FormInput").style.borderColor = '';
    }

    if (!email) {
        document.querySelector("#register_email_FormInput").style.borderColor = 'red';
        blank = true;
    } else {
        document.querySelector("#register_email_FormInput").style.borderColor = '';
    }

    if (!username) {
        document.querySelector("#register_username_FormInput").style.borderColor = 'red';
        blank = true;
    } else {
        document.querySelector("#register_username_FormInput").style.borderColor = '';
    }

    if (!password) {
        document.querySelector("#register_password_FormInput").style.borderColor = 'red';
        blank = true;
    } else {
        document.querySelector("#register_password_FormInput").style.borderColor = '';
    }

    if (!re_password) {
        document.querySelector("#register_re_password_FormInput").style.borderColor = 'red';
        blank = true;
    } else {
        document.querySelector("#register_re_password_FormInput").style.borderColor = 'inherit';
    }

    return blank;
}

function recover() {
    return false;
}

function autofocus_modal(modal_id, input_id) {
    document.getElementById(modal_id).addEventListener('shown.bs.modal', () => {
        document.getElementById(input_id).focus()
    })
}


function disable() {
    document.querySelectorAll(".disable").forEach(b => {
        b.disabled = true;
    });

    document.querySelectorAll(".disableAnchorTag").forEach(a => {
        a.style.pointerEvents="none";
        a.style.cursor="default";
    });

    document.querySelectorAll(".spinner-border").forEach(s => {
        s.hidden = false;
    });
}


function enable() {
    document.querySelectorAll(".disable").forEach(b => {
        b.disabled = false;
    });

    document.querySelectorAll(".disableAnchorTag").forEach(a => {
        a.style.pointerEvents="auto";
        a.style.cursor="pointer";
    });

    document.querySelectorAll(".spinner-border").forEach(s => {
        s.hidden = true;
    });
}



