async function addRulePOST(interactionDetails) {
    try {
        const response = await fetch('http://127.0.0.1:5000/addRule', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ interactionDetails }),
        });
        

        const data = await response.json();
        console.log("It says:", data);
    } catch (error) {
        console.error(error);
    }
}

function getPatientPOST() {
    return fetch('http://127.0.0.1:5000/getPatient', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
    }).then(response => response.json())
      .then(data => {
          console.log("It says:", data);
          return data; // Retourne les données récupérées
      })
      .catch(error => {
          console.error(error);
          throw error; // Rejette la promesse en cas d'erreur
      });
}

function getAlertesPOST() {
    return fetch('http://127.0.0.1:5000/getAlertes', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
    }).then(response => response.json())
      .then(data => {
          console.log("It says alertes:", data);
          return data; // Retourne les données récupérées
      })
      .catch(error => {
          console.error(error);
          throw error; // Rejette la promesse en cas d'erreur
      });
}



function getRulesPOST() {
    return fetch('http://127.0.0.1:5000/getRules', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
    }).then(response => response.json())
      .then(data => {
          console.log("It says:", data);
          return data; // Retourne les données récupérées
      })
      .catch(error => {
          console.error(error);
          throw error; // Rejette la promesse en cas d'erreur
      });
}

async function addPatientPOST(PatientsDetails) {
    try {
        const response = await fetch('http://127.0.0.1:5000/addPatient', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({PatientsDetails}),
        });
        const data = await response.json();
        console.log("it says:", data);
    } catch (error) {
        console.error("Error:", error);
    }
}

async function addTraitementPOST(TraitementDetails) {
    console.log("APi request");
    console.log(TraitementDetails);
    try {
        const response = await fetch('http://127.0.0.1:5000/addTraitement', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({TraitementDetails : TraitementDetails}),
        });
        const data = await response.json();
        console.log("it says:", data);
    } catch (error) {
        console.error("Error:", error);
    }
}

// async function getTraitementsPatientPOST(TraitementDetails) {
//         console.log("gettraitement data received:", TraitementDetails);
//     try {
//         const response = await fetch('http://127.0.0.1:5000/getTraitements', {
//             method: 'POST',
//             headers: {
//                 'Content-Type': 'application/json',
//             },
//             body: JSON.stringify({TraitementDetails}),
//         });
//         const data = await response.json();
//         console.log("it says about getTraitements:", data);
//     } catch (error) {
//         console.error("Error:", error);
//     }
// }

function getTraitementsPatientPOST(TraitementDetails) {
    return fetch('http://127.0.0.1:5000/getTraitements', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({TraitementDetails}),
    }).then(response => response.json())
      .then(data => {
          console.log("It says gettraitement:", data);
          return data; // Retourne les données récupérées
      })
      .catch(error => {
          console.error(error);
          throw error; // Rejette la promesse en cas d'erreur
      });
}

getMedecinsPOST()


function getMedecinsPOST() {
    return fetch('http://127.0.0.1:5000/getMedecins', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
    }).then(response => response.json())
      .then(data => {
          console.log("It says gettraitement:", data);
          return data; // Retourne les données récupérées
      })
      .catch(error => {
          console.error(error);
          throw error; // Rejette la promesse en cas d'erreur
      });
}