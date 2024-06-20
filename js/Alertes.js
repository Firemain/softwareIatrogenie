console.log("alertes.js chargé");
const tableBody = document.getElementById("rulesTableBody");
    const searchInput = document.getElementById("searchInput");
var listeAlertes = [];
var listeAlertesJSON = [];
var liste_medecins = [];

getMedecinsPOST().then(data => {;

    liste_medecins= data["medecins"];

    console.log("liste medecin:", liste_medecins);

});

getAlertesPOST().then(data => {
    console.log("alertes data:",data);
  liste_alertes = data["alertes"]; // Mettez à jour la variable globale

  console.log("liste des alertes :", liste_alertes);

  // Parcourir chaque sous-tableau
  for (let i = 0; i < liste_alertes.length; i++) {
      const item = liste_alertes[i];
      // Assurez-vous que l'élément a la structure attendue
      if (Object.keys(item).length === 8) {
          const alerteJSON = {
                "id_patient": item[1],
              "nom_patient": item[2],
              "age_patient": item[3],
              "sexe_patient": item[4],
              "code_iatrogenique": item[5],
              "date": item[6],
              "gestion": item[7],
          };
          listeAlertesJSON.push(alerteJSON);

      } else {
          console.error("Structure de données invalide :", item);
          // Vous pouvez décider de gérer les cas où la structure est invalide
      }
  }

  console.log("Liste des salertes ", listeAlertesJSON)

  // Appeler la fonction mettreAJourTableau après avoir récupéré les données
  mettreAJourTableau();
  // Faites quelque chose avec les données récupérées
}).catch(error => {
  console.error("Erreur lors de la récupération des alertes :", error);
});


  document.addEventListener("DOMContentLoaded", function() {
    // Récupérez le tableau du corps du tableau
    const tableBody = document.getElementById("tablebody");

    // Récupérez le champ de recherche
    const searchInput = document.getElementById("searchInput");

    // Ajoutez un gestionnaire d'événements pour l'événement "input"
    searchInput.addEventListener("input", function() {
    // Récupérez la valeur du champ de recherche
    const rechercheNom = searchInput.value.toLowerCase();

    // Parcourez les lignes du tableau
    for (let i = 0; i < tableBody.rows.length; i++) {
        const row = tableBody.rows[i];
        const nomCell = row.cells[0].textContent.toLowerCase(); // Assurez-vous d'ajuster l'index en fonction de votre structure de tableau

        // Vérifiez si le nom du patient correspond à la recherche
        if (nomCell.includes(rechercheNom)) {
        // Affichez la ligne si la recherche correspond
        row.style.display = "";
        } else {
        // Masquez la ligne si la recherche ne correspond pas
        row.style.display = "none";
        }
    }
    });
})



function mettreAJourTableau() {
    // Effacez le tableau
    alertTableBody.innerHTML = "";

    // Récupérez le terme de recherche
    const termeRecherche = searchInput.value.toLowerCase();

    // Filtrer les alertes en fonction du terme de recherche sur le nom du patient
    const alertesFiltrees = listeAlertesJSON.filter(function (alerte) {
        // Assurez-vous que la propriété utilisée est définie avant d'appliquer toLowerCase
        const nom = alerte.nom_patient ? alerte.nom_patient.toLowerCase() : "";

        return nom.includes(termeRecherche);
    });

        // Afficher les alertes filtrées dans le tableau
        alertesFiltrees.forEach(function (alerte) {
            const row = document.createElement("tr");
            row.setAttribute("data-id-patient", alerte.id_patient); // Utilisez "data-id-patient" pour stocker l'id_patient

            // Ajoutez les autres cellules au tableau
            row.innerHTML += `
                <td>${alerte.nom_patient}</td>
                <td>${alerte.sexe_patient}</td>
                <td>${alerte.age_patient}</td>
                <td>${alerte.date}</td>
                <td>${alerte.code_iatrogenique}</td>
            `;

            const cellGestion = document.createElement("td");
if (alerte.gestion === null) {
    // Si la variable "gestion" est null, affichez un menu déroulant
    const select = document.createElement("select");
    select.className = "form-select";

    // Ajout de l'option par défaut
    select.innerHTML = `<option value="aGérer">À gérer</option>`;

    // Parcourir la liste des médecins et les ajouter au menu déroulant
    liste_medecins.forEach(medecin => {
        // medecin[1] est le nom de famille, medecin[2] est le prénom
        const optionMedecin = document.createElement("option");
        optionMedecin.value = `medecin${medecin[0]}`; // medecin[0] est l'ID du médecin
        optionMedecin.textContent = `${medecin[2]} ${medecin[1]}`; // Prénom Nom
        select.appendChild(optionMedecin);
    });

    cellGestion.appendChild(select);
} else {
    // Sinon, affichez le nom du médecin
    cellGestion.textContent = alerte.gestion;
}

            row.appendChild(cellGestion);

            alertTableBody.appendChild(row);

        // Ajoutez un gestionnaire d'événements à chaque élément de la ligne
        row.addEventListener("click", function (event) {
            // Vérifiez si la cible du clic est la cellule de gestion
            if (!event.target.closest("td").querySelector("select")) {
                const idPatient = row.getAttribute("data-id-patient"); // Récupérez l'id_patient depuis l'attribut data

                console.log("id patient :", idPatient);
                // Récupérez la liste des traitements pour le patient sélectionné

                const idPatientJSON= {
                    "id_patient":idPatient
                };


                getTraitementsPatientPOST(idPatientJSON).then(data => {
                    console.log("datatraitement:", data);
                    const traitementsPatient = data["alertes"];
                
                    // Affichez la liste des traitements dans la modal
                    const listeTraitements = document.getElementById("listeTraitements");
                    listeTraitements.innerHTML = "";  // Effacez le contenu existant
                
                    if (Array.isArray(traitementsPatient) && traitementsPatient.length > 0) {
                        const table = document.createElement("table");
                        table.classList.add("table"); // Ajoutez des classes Bootstrap pour styliser le tableau
                
                        // Créez la première ligne d'en-tête du tableau
                        const thead = document.createElement("thead");
                        const headerRow = document.createElement("tr");
                        headerRow.innerHTML = `
                            <th>Code du traitement</th>
                            <th>Date de début</th>
                            <th>Date de fin</th>
                            <th>Dose</th>
                        `;
                        thead.appendChild(headerRow);
                        table.appendChild(thead);
                
                        // Créez le corps du tableau
                        const tbody = document.createElement("tbody");
                
                        traitementsPatient.forEach(function (traitement) {
                            const row = document.createElement("tr");
                            row.innerHTML = `
                                <td>${traitement.code_traitement}</td>
                                <td>${traitement.date_debut}</td>
                                <td>${traitement.date_fin}</td>
                                <td>${traitement.dose}</td>

                            `;
                            tbody.appendChild(row);
                        });
                
                        table.appendChild(tbody);
                        listeTraitements.appendChild(table);
                    } else {
                        // Traitements non trouvés ou tableau vide
                        const p = document.createElement("p");
                        p.textContent = "Aucun traitement trouvé.";
                        listeTraitements.appendChild(p);
                    }
                
                    // Affichez la modal
                    const traitementModal = new bootstrap.Modal(document.getElementById("traitementModal"));
                    traitementModal.show();
                });
                

            }
        });
    });
}



// Appel initial pour mettre à jour le tableau avec toutes les alertes
mettreAJourTableau();

// Ajout de l'écouteur d'événements sur l'input de recherche
searchInput.addEventListener("input", mettreAJourTableau);


