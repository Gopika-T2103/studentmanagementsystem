// ----------- Login Validation --------------------
const loginEmail = document.getElementById("email");
const loginPassword = document.getElementById("password");
const loginRole = document.getElementById("role");
const loginBtn = document.getElementById("loginBtn");

function checkLoginFields() {
    if (
        loginEmail.value.trim() !== "" &&
        loginPassword.value.trim() !== "" &&
        loginRole.value.trim() !== ""
    ) {
        loginBtn.disabled = false;
        loginBtn.style.opacity = "1";
    } else {
        loginBtn.disabled = true;
        loginBtn.style.opacity = "0.5";
    }
}

loginEmail.addEventListener("input", checkLoginFields);
loginPassword.addEventListener("input", checkLoginFields);
loginRole.addEventListener("change", checkLoginFields);


// ----------- Signup Validation --------------------
const signupUsername = document.getElementById("signup_username");
const signupEmail = document.getElementById("signup_email");
const signupPassword = document.getElementById("signup_password");
const signupConfirm = document.getElementById("signup_confirmpassword");
const signupRole = document.getElementById("signup_role");
const signupBtn = document.getElementById("signupBtn");

function checkSignupFields() {
    if (
        signupUsername.value.trim() !== "" &&
        signupEmail.value.trim() !== "" &&
        signupPassword.value.trim() !== "" &&
        signupConfirm.value.trim() !== "" &&
        signupRole.value.trim() !== ""
    ) {
        signupBtn.disabled = false;
        signupBtn.style.opacity = "1";
    } else {
        signupBtn.disabled = true;
        signupBtn.style.opacity = "0.5";
    }
}

signupUsername.addEventListener("input", checkSignupFields);
signupEmail.addEventListener("input", checkSignupFields);
signupPassword.addEventListener("input", checkSignupFields);
signupConfirm.addEventListener("input", checkSignupFields);
signupRole.addEventListener("change", checkSignupFields);




// -----------------For Toggle between login and signup page--------------//

// get both forms
const loginForm=document.getElementById("loginForm");
const signupForm=document.getElementById("signupForm");

// get switching links
const showSignup=document.getElementById("showSignup");
const showLogin=document.getElementById("showLogin");

// show signup,hide login
if(showSignup){
    showSignup.addEventListener("click",function(){
        loginForm.style.display="none";
        signupForm.style.display="block";
    });
}

// show login,hide signup
if(showLogin){
    showLogin.addEventListener("click",function(){
        signupForm.style.display="none";
        loginForm.style.display="block";
    });
}

// After signup show login
const show = "{{ show }}";

if (show === "signup") {
    loginForm.style.display = "none";
    signupForm.style.display = "block";
} else {
    loginForm.style.display = "block";
    signupForm.style.display = "none";
}

