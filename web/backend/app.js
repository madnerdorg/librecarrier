/*
Name:        LocalStorage Manager
Author:      Remi Sarrailh
Version:     0.3
Licence:     MIT
Description: Manage your localStorage variable using a web interface
URL: 
*/

/*
    Get Parameters
*/

hidepassword = true;

function get() {
    let prmstr = window.location.search.substr(1);
    return prmstr != null && prmstr != "" ? transformToAssocArray(prmstr) : {};
}

function transformToAssocArray( prmstr ) {
    let params = {};
    let prmarr = prmstr.split("&");
    for ( let i = 0; i < prmarr.length; i++) {
        let tmparr = prmarr[i].split("=");
        params[tmparr[0]] = tmparr[1];
    }
    return params;
}

function analyseGet(){
    parameters = get();
    console.log(parameters);
    
    if (typeof parameters.showpassword !== "undefined"){
        if(parameters.showpassword !== "false"){
            hidepassword = false;
        }
    }
    
    if (typeof parameters.name !== "undefined" && typeof parameters.value !== "undefined"){
        console.log(`Add ${name} : ${value}`);
        localStorage.setItem(parameters.name,parameters.value);
    }
    
    if (typeof parameters.goback !== "undefined") {
        window.location.href = parameters.goback;
    }
}

/*

    LocalStorage Management

*/

function save(){
    let filename = document.getElementsByName("saveFilename")[0].value;
    let backup = {};
    for (i = 0; i < localStorage.length; i++) {
        let key = localStorage.key(i);
        let value = localStorage.getItem(key);
        backup[key] = escape(encodeURIComponent(value));
    }
    let json = JSON.stringify(backup);
    let base = btoa(unescape(encodeURIComponent(json)));
    let href = 'data:text/javascript;charset=utf-8;base64,' + base;
    let link = document.createElement('a');
    link.setAttribute('download', filename);
    link.setAttribute('href', href);
    document.querySelector('body').appendChild(link);
    link.click();
    link.remove();
}

function load(f){
    if (f) {
        var reader = new FileReader();
        reader.onload = function(e) {
            fileLoaded = true;
            var text = e.target.result;
            var backup = "";
            try {
                backup = JSON.parse(text);
            }
            catch(event) {
                fileLoaded = false;
                alert("Failed to load file");
            }
            
            for (var key in backup){
                var value = decodeURIComponent(unescape(backup[key]));
                window.localStorage.setItem(key, value);
            }
            if(fileLoaded){
                location.reload();
            }
        };
        reader.readAsText(f);
        
    } else {
        alert('Failed to load file');
    }
}

function getItems(){
    for (var i = 0; i < localStorage.length; i++){
        console.log("Load localstorage...");
        addField(localStorage.key(i),localStorage.getItem(localStorage.key(i)));
    }
}

function saveItem(name){
    let value = document.getElementById(name).children[1].value;
    localStorage.setItem(name,value);
    console.log(`Add ${name} : ${value}`);
}

function removeItem(name){
    localStorage.removeItem(name);
    let field = document.getElementById(name);
    field.parentNode.removeChild(field);
    console.log(`Removed ${name}`);
}

function addItem(){
    let name = window.prompt("Enter variable name","name");
    addField(name);
}

function addField(name = "name",value = "value"){
    let storage = document.getElementById("storage");
    let type = "unknown";
    if (name.search("_url") !== -1){
        type = "url";
    }
    
    if (name.search("_password") !== -1){
        if(hidepassword){
            type = "password";
        }
    }
    
    //console.log(type);
    
    switch (type) {
        case "url":
        let value_href = value;
        value_href = value_href.replace("wss://","https://");
        value_href = value_href.replace("ws://","http://");
        
        code = `
        ${storage.innerHTML} 
        <div id=${name}>
        <a target="_blank" href="${value_href}">${name}</a>
        <input type="text" placeholder="data" value=${value}> 
        <button onclick="saveItem('${name}')">O</button> 
        <button onclick="removeItem('${name}')">X</button>
        </div>
        `;
        break;
        
        case "password":
        code = `
        ${storage.innerHTML} 
        <div id=${name}>
        <label style="color:red" for="${name}">${name}</label>
        <input type="password" placeholder="data" value=${value}> 
        <button onclick="saveItem('${name}')">O</button> 
        <button onclick="removeItem('${name}')">X</button>
        </div>
        `;
        break;
        
        default:
        code = `
        ${storage.innerHTML} 
        <div id=${name}>
        <label for="${name}">${name}</label>
        <input type="text" placeholder="data" value=${value}> 
        <button onclick="saveItem('${name}')">O</button> 
        <button onclick="removeItem('${name}')">X</button>
        </div>
        `;
        break;
    }
    
    storage.innerHTML = code;
    console.log(`Field -> ${name} : ${value}`);
}

/*
    Encryption / Decryption
*/

// CryptoJS Source: https://github.com/brix/crypto-js
function encrypt(){
    key = document.getElementById("secretPass").value;
    
    all_inputs = document.getElementById("storage").children;
    for (let index = 0; index < all_inputs.length; index++) {
        var element = all_inputs[index];
        value = element.children[1].value;
        encrypted_text = CryptoJS.AES.encrypt(value, key).toString();
        element.children[1].value = encrypted_text;            
        localStorage.setItem(element.id,encrypted_text);
        localStorage.setItem("encrypted","true");
    }
}

function decrypt(){
    key = document.getElementById("secretPass").value;
    
    all_inputs = document.getElementById("storage").children;
    for (let index = 0; index < all_inputs.length; index++) {
        var element = all_inputs[index];
        value = element.children[1].value;
        value = CryptoJS.AES.decrypt(value, key).toString(CryptoJS.enc.Utf8);
        if(value !== ""){
            element.children[1].value = value;
            localStorage.setItem(element.id,value);
            localStorage.removeItem("encrypted");
        } else {
        }
    }
}
