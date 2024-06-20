//Prepa Objet BDD verif ID

const btnVerifID = document.getElementById("logInBtn");
if (btnVerifID != null) {
    btnVerifID.addEventListener('click', () => {
        const usernameVal = document.getElementById("username");
        const passwordVal = document.getElementById("password");

    var _myrec = {
        username: usernameVal.value,
        password : passwordVal.value,
    };

    console.log("*** debug :", _myrec)
    ipcMain.send("VerifID", _myrec)

    })
}