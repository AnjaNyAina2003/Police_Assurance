(() => {
    const API_BASE_URL = 'http://127.0.0.1:8000/api';

    document.addEventListener('DOMContentLoaded', () => {
        const container = document.querySelector('.container');
        const registerBtn = document.querySelector('.register-btn');
        const loginBtn = document.querySelector('.login-btn');

        if (registerBtn && loginBtn && container) {
            registerBtn.addEventListener('click', () => container.classList.add('active'));
            loginBtn.addEventListener('click', () => container.classList.remove('active'));
        }

        setupUser();
        setupLogout();
        setupBranch();
        setupAgence();
        setupClient();
        setupClientSearch();
        setupPoliceAssurance();
        setupTogglePassword();
        setupModifProfil();

        document.getElementById("user-menu").addEventListener("click", function () {
            document.getElementById("dropdown-menu").classList.toggle("show");
        });
        document.getElementById("dropdown-menu").addEventListener("click", function (event) {
            event.stopPropagation(); 
        });
    });

    function alertPerso(type, message) {
        const notification = document.createElement("div");
        notification.classList.add("custom-notification", `custom-${type}`);
        
        const icon = type === 'success' ? 'fa-check' : 
                     type === 'error' ? 'fa-triangle-exclamation' : 'fa-comment';
        const title = type === 'success' ? 'Succès' : 
                      type === 'error' ? 'Erreur' : 'Info';
        
        notification.innerHTML = `
            <div class="custom-div-notif">
                <span class="custom-icon">
                    <i class="fa-solid ${icon}"></i>
                </span>
                <div>
                    <h3>${title}</h3>
                    <p>${message}</p>
                </div>
                <span class="custom-close-btn">
                    <i class="fa-solid fa-xmark"></i>
                </span>
            </div>
        `;
        
        document.body.insertBefore(notification, document.body.firstChild);
        
        setTimeout(() => {
            notification.classList.add("custom-fade-out");
        }, 5000);

        const closeBtn = notification.querySelector(".custom-close-btn");
        closeBtn.addEventListener("click", () => {
            notification.classList.add("custom-fade-out");
        });
        
        notification.addEventListener("animationend", () => {
            if (notification.classList.contains("custom-fade-out")) {
                notification.remove();
            }
        });
    }

    function setupTogglePassword() {
        document.querySelectorAll('.toggle-password').forEach(item => {
            item.addEventListener('click', function () {
                const passwordField = document.getElementById(this.dataset.target);
                if (passwordField.type === 'password') {
                    passwordField.type = 'text';
                    this.classList.remove('fa-eye-slash');
                    this.classList.add('fa-eye');
                } else {
                    passwordField.type = 'password';
                    this.classList.remove('fa-eye');
                    this.classList.add('fa-eye-slash');
                }
            });
        });
    }

    document.addEventListener('click', (event) => {
        const target = event.target;

        if (target.classList.contains('btn-del')) {
            console.log("Bouton suppression cliqué !");
            document.getElementById('PopupDel').style.display = 'flex';
        }

        if (target.id === 'logoutButton') {
            console.log("Bouton déconnexion cliqué !");
            const logoutPopup = document.getElementById('PopupLogout');
            if (logoutPopup) {
                document.getElementById('PopupLogout').style.display = 'flex';   
            }else{
                console.error("Erreur: PopupLogout introuvable.");
            }
        }

        if (target.id === 'ajout_sect') {
            console.log("Ajout Branche cliqué !");
            document.getElementById('PopupAddBranche').style.display = 'flex';
        }

        if (target.classList.contains('btn-modif-sect')) {
            console.log("Bouton modification branche cliqué !");
            document.getElementById('PopupModifBranche').style.display = 'flex';

            document.getElementById('nom_branche_updt').value = target.dataset.nom_branche;
            document.getElementById('prefixe_updt').value = target.dataset.prefixe;
            document.getElementById('IdBranche').value = target.dataset.id;
        }

        if (target.classList.contains('btn-del-sect')) {
            console.log("Bouton suppression branche cliqué !");
            document.getElementById('PopupDelBranche').style.display = 'flex';
        }

        if (target.id === 'ajout_client') {
            console.log("Ajout Client cliqué !");
            document.getElementById('PopupAddClient').style.display = 'flex';
        }

        if (target.classList.contains('close')) {
            const modal = target.closest('.modal') || target.closest('.modalConf') || target.closest('.modalClient');
            if (modal) {
                modal.style.display = 'none';
            }
        }

        if (target.id === 'cancelDelete') {
            console.log("Annulation suppression utilisateur");
            document.getElementById('PopupDel').style.display = 'none';
        }

        if (target.id === 'cancelLogout') {
            console.log("Annulation déconnexion");
            document.getElementById('PopupLogout').style.display = 'none';
        }

        if (target.id === 'cancelAddBranche') {
            console.log("Annulation ajout branche");
            document.getElementById('PopupAddBranche').style.display = 'none';
        }

        if (target.id === 'cancelDelBranche') {
            console.log("Annulation suppression branche");
            document.getElementById('PopupDelBranche').style.display = 'none';
        }

        if (target.id === 'cancelAddClient') {
            console.log("Annulation Ajout client");
            document.getElementById('PopupAddClient').style.display = 'none';
        }

        if (target.id === 'cancelModifClient') {
            console.log("Annulation modification client");
            document.getElementById('PopupModifClient').style.display = 'none';
        }

        if (target.id === 'cancelDelClient') {
            console.log("Annulation suppression client");
            document.getElementById('PopupDelClient').style.display = 'none';
        }

        if (target.id === 'cancelAddagence') {
            console.log("Annulation ajout agence");
            document.getElementById('PopupAddagence').style.display = 'none';
        }
    
        if (target.id === 'cancelModifAgence') {
            console.log("Annulation modification agence");
            document.getElementById('PopupModifAgence').style.display = 'none';
        }
    
        if (target.id === 'cancelDelAgence') {
            console.log("Annulation suppression agence");
            document.getElementById('PopupDelAgence').style.display = 'none';
        }

        if (target.id === 'ajout_agence') {
            console.log("Ajout Agence cliqué !");
            document.getElementById('PopupAddagence').style.display = 'flex';
        }

        if (target.classList.contains('btn-modif-agence')) {
            console.log("Bouton modification agence cliqué !");
            document.getElementById('PopupModifAgence').style.display = 'flex';
    
            document.getElementById('nom_agence_updt').value = target.dataset.nom_agence;
            document.getElementById('ville_updt').value = target.dataset.ville;
            document.getElementById('IdAgence').value = target.dataset.id;
        }
    
        if (target.classList.contains('btn-del-agence')) {
            console.log("Bouton suppression agence cliqué !");
            document.getElementById('PopupDelAgence').style.display = 'flex';
        }
    });

    function setupUser() {
        let IdUser = null;
        const popups = {
            PopupModif: document.getElementById('PopupModif'),
            PopupDel: document.getElementById('PopupDel'),
        };

        document.querySelectorAll('.btn-modif').forEach(button => {
            button.addEventListener('click', () => {
                IdUser = button.dataset.id;
                console.log(IdUser);
                document.getElementById('email').value = button.dataset.email;
                document.getElementById('username').value = button.dataset.username;
                const agenceSelect = document.getElementById('agence');
                const agenceId = button.dataset.agenceId;

                if (agenceSelect && agenceId) {
                    agenceSelect.value = agenceId;
                }

                popups.PopupModif.style.display = 'flex';
            });
        });

        document.getElementById('modifForm')?.addEventListener('submit', async (event) => {
            event.preventDefault();
            if (!IdUser) return alert("ID utilisateur manquant");

            const email = document.getElementById('email').value;
            const username = document.getElementById('username').value;
            const agence = document.getElementById('agence').value;

            try {
                const response = await fetch(`${API_BASE_URL}/auth/user/${IdUser}`, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCSRFToken()
                    },
                    body: JSON.stringify({ email, username, agence_id: agence })
                });

                if (!response.ok) throw new Error("Erreur lors de la modification.");
                location.reload();
                alertPerso("success", "Utilisateur modifié avec succès.");
            } catch (error) {
                console.error(error);
                alertPerso("error", error.message);
            }
        });

        document.getElementById('cancelModif')?.addEventListener('click', () => {
            popups.PopupModif.style.display = 'none';
        });

        let IdUserToDelete = null;
        document.querySelectorAll('.btn-del').forEach(button => {
            button.addEventListener('click', () => {
                IdUserToDelete = button.dataset.id;
                popups.PopupDel.style.display = 'flex';
            });
        });

        document.getElementById('confirmDelete')?.addEventListener('click', async () => {
            if (!IdUserToDelete) return alert("Aucun utilisateur sélectionné");

            try {
                const response = await fetch(`${API_BASE_URL}/auth/user/${IdUserToDelete}`, {
                    method: 'DELETE',
                    headers: { 'X-CSRFToken': getCSRFToken() }
                });

                if (!response.ok) throw new Error("Erreur lors de la suppression.");
                alertPerso("success", "Utilisateur supprimé avec succès.");
                location.reload();
            } catch (error) {
                console.error(error);
                alertPerso("error", error.message);
            }
        });

        document.getElementById('cancelDelete')?.addEventListener('click', () => {
            popups.PopupDel.style.display = 'none';
        });
    }

    function setupLogout() {
        const logoutPopup = document.getElementById('PopupLogout');
        if(!logoutPopup) return;

        document.getElementById('confirmLogout')?.addEventListener('click', () => {
            localStorage.setItem("activeMenu", "dashboard");
            window.location.href = '/web/logout';
        });

        document.getElementById('cancelLogout')?.addEventListener('click',() => {
            logoutPopup.style.display = 'none';
        });
    }

    function setupBranch() {
        let id_brancheToDel = null;
        document.getElementById('PopupAddBranche')?.addEventListener('submit', async (event) => {
            event.preventDefault();

            const nom_branche = document.getElementById('nom_branche').value;
            const prefixe = document.getElementById('prefixe').value;

            try {
                const response = await fetch(`${API_BASE_URL}/branchType/branch`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCSRFToken()
                    },
                    body: JSON.stringify({ nom_branche, prefixe })
                });

                if (!response.ok) throw new Error("Erreur lors de l'ajout.");
                alertPerso("success","Branche ajoutée avec succès.");
                location.reload();
            } catch (error) {
                console.error(error);
                alertPerso("error",error.message);
            }
        });

        document.getElementById('PopupModifBranche')?.addEventListener('submit', async (event) => {
            event.preventDefault();

            const id_branche = document.getElementById('IdBranche').value;
            const nom_branche = document.getElementById('nom_branche_updt').value;
            const prefixe = document.getElementById('prefixe_updt').value;

            try {
                const response = await fetch(`${API_BASE_URL}/branchType/branch/${id_branche}`, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCSRFToken()
                    },
                    body: JSON.stringify({ nom_branche, prefixe })
                });

                if (!response.ok) throw new Error("Erreur lors de la modification.");
                alertPerso("success","Branche modifiée avec succès.");
                location.reload();
            } catch (error) {
                console.error(error);
                alertPerso("error",error.message);
            }
        });

        document.querySelectorAll('.btn-del-sect').forEach(button => {
            button.addEventListener('click', () => {
                id_branche_to_delete = button.dataset.id;
                document.getElementById('PopupDelBranche').style.display = 'flex';
            });
        });

        document.getElementById('confirmDelBranche')?.addEventListener('click', async () => {
            if (id_brancheToDel) {
                try {
                    const response = await fetch(`${API_BASE_URL}/branchType/branch/${id_branche_to_delete}`, {
                        method: 'DELETE',
                        headers: {
                            'X-CSRFToken': getCSRFToken()
                        }
                    });
    
                    if (!response.ok) throw new Error("Erreur lors de la suppression.");
                    alertPerso("success","Branche supprimée avec succès.");
                    location.reload();
                } catch (error) {
                    console.error(error);
                    alertPerso("error",error.message);
                }
            }
        });
    }

    function setupAgence() {
        let id_agenceToUpdate = null;
        let id_agenceToDelete = null;

        document.getElementById('addAgenceForm')?.addEventListener('submit', async (event) => {
            event.preventDefault();
    
            const nom_agence = document.getElementById('nom_agence').value;
            const ville = document.getElementById('ville').value;
    
            try {
                const response = await fetch(`${API_BASE_URL}/agence/agenceLieu`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCSRFToken()
                    },
                    body: JSON.stringify({ nom_agence, ville })
                });
    
                if (!response.ok) throw new Error("Erreur lors de l'ajout.");
                alertPerso("success","Agence ajoutée avec succès.");
                location.reload();
            } catch (error) {
                console.error(error);
                alertPerso("error",error.message);
            }
        });

        document.querySelectorAll('.btn-modif-agence').forEach(button => {
            button.addEventListener('click', () => {
                id_agenceToUpdate = button.dataset.id;
                document.getElementById('nom_agence_updt').value = button.dataset.nom_agence;
                document.getElementById('ville_updt').value = button.dataset.ville;
                document.getElementById('IdAgence').value = button.dataset.id;
                document.getElementById('PopupModifAgence').style.display = 'flex';
            });
        });
    
        document.getElementById('modifAgenceForm')?.addEventListener('submit', async (event) => {
            event.preventDefault();
    
            const id_agence = document.getElementById('IdAgence').value;
            const nom_agence = document.getElementById('nom_agence_updt').value;
            const ville = document.getElementById('ville_updt').value;
    
            try {
                const response = await fetch(`${API_BASE_URL}/agence/agenceLieu/${id_agence}`, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCSRFToken()
                    },
                    body: JSON.stringify({ nom_agence, ville })
                });
    
                if (!response.ok) throw new Error("Erreur lors de la modification.");
                alertPerso("success","Agence modifiée avec succès.");
                location.reload();
            } catch (error) {
                console.error(error);
                alertPerso("error",error.message);
            }
        });

        document.querySelectorAll('.btn-del-agence').forEach(button => {
            button.addEventListener('click', () => {
                id_agenceToDelete = button.dataset.id;
                document.getElementById('PopupDelAgence').style.display = 'flex';
            });
        });
    
        document.getElementById('confirmDelAgence')?.addEventListener('click', async () => {
            if (id_agenceToDelete) {
                try {
                    const response = await fetch(`${API_BASE_URL}/agence/agenceLieu/${id_agenceToDelete}`, {
                        method: 'DELETE',
                        headers: {
                            'X-CSRFToken': getCSRFToken()
                        }
                    });
    
                    if (!response.ok) throw new Error("Erreur lors de la suppression.");
                    alertPerso("success","Agence supprimée avec succès.");
                    location.reload();
                } catch (error) {
                    console.error(error);
                    alertPerso("error",error.message);
                }
            }
        });
    }

    function setupClient() {
        let IdClientToUpdate = null;
        let IdClientToDelete = null;
    
        document.getElementById('addClientForm')?.addEventListener('submit', async (event) => {
            event.preventDefault();
    
            const nom_client = document.getElementById('nom_client').value;
            const prenom_client = document.getElementById('prenom_client').value;
            const telephone = document.getElementById('telephone').value;
            const adresse = document.getElementById('adresse').value;
    
            try {
                const response = await fetch(`${API_BASE_URL}/souscripteur/clients`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCSRFToken()
                    },
                    body: JSON.stringify({ nom_client, prenom_client, telephone, adresse })
                });
    
                if (!response.ok) throw new Error("Erreur lors de l'ajout.");
                alertPerso("success","Client ajouté avec succès.");
                location.reload();
            } catch (error) {
                console.error(error);
                alertPerso("error",error.message);
            }
        });
    
        document.querySelectorAll('.btn-modif-client').forEach(button => {
            button.addEventListener('click', () => {
                IdClientToUpdate = button.dataset.id;
                document.getElementById('nom_client_updt').value = button.dataset.nom_client;
                document.getElementById('prenom_client_updt').value = button.dataset.prenom_client;
                document.getElementById('telephone_updt').value = button.dataset.phone;
                document.getElementById('adresse_updt').value = button.dataset.adresse;
                document.getElementById('PopupModifClient').style.display = 'flex';
            });
        });
    
        document.getElementById('modifClientForm')?.addEventListener('submit', async (event) => {
            event.preventDefault();
    
            const id_client = IdClientToUpdate;
            const nom_client = document.getElementById('nom_client_updt').value;
            const prenom_client = document.getElementById('prenom_client_updt').value;
            const telephone = document.getElementById('telephone_updt').value;
            const adresse = document.getElementById('adresse_updt').value;
    
            try {
                const response = await fetch(`${API_BASE_URL}/souscripteur/clients/${id_client}`, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCSRFToken()
                    },
                    body: JSON.stringify({ nom_client, prenom_client, telephone, adresse })
                });
    
                if (!response.ok) throw new Error("Erreur lors de la modification.");
                alertPerso("success","Client modifié avec succès.");
                location.reload();
            } catch (error) {
                console.error(error);
                alertPerso("error",error.message);
            }
        });
    
        document.querySelectorAll('.btn-del-client').forEach(button => {
            button.addEventListener('click', () => {
                IdClientToDelete = button.dataset.id;
                document.getElementById('PopupDelClient').style.display = 'flex';
            });
        });
    
        document.getElementById('confirmDelClient')?.addEventListener('click', async () => {
            if (IdClientToDelete) {
                try {
                    const response = await fetch(`${API_BASE_URL}/souscripteur/clients/${IdClientToDelete}`, {
                        method: 'DELETE',
                        headers: {
                            'X-CSRFToken': getCSRFToken()
                        }
                    });
    
                    if (!response.ok) throw new Error("Erreur lors de la suppression.");
                    alertPerso("success","Client supprimé avec succès.");
                    location.reload();
                } catch (error) {
                    console.error(error);
                    alertPerso("error",error.message);
                }
            }
        });
    }

    function showClientDetails(client) {
        const popup = document.getElementById('PopupClientDetails');
        
        document.getElementById('detail-num-compte').textContent = client.num_compte_client || 'N/A';
        document.getElementById('detail-nom').textContent = client.nom_client || 'N/A';
        document.getElementById('detail-prenom').textContent = client.prenom_client || 'N/A';
        document.getElementById('detail-telephone').textContent = client.telephone || 'N/A';
        document.getElementById('detail-adresse').textContent = client.adresse || 'N/A';
        document.getElementById('detail-date').textContent = client.date_creation || 'N/A';
        
        popup.style.display = 'flex';
    }

    function setupClientSearch() {
        const clientDetailsModal = document.getElementById('PopupClientDetails');
        const closeButton = clientDetailsModal?.querySelector('.close');
        
        // Gestion de la fermeture de la modal
        if (closeButton) {
            closeButton.addEventListener('click', () => {
                clientDetailsModal.style.display = 'none';
            });
        }
    
        // Gestion du clic à l'extérieur pour fermer
        window.addEventListener('click', (event) => {
            if (event.target === clientDetailsModal) {
                clientDetailsModal.style.display = 'none';
            }
        });
    
        // Interception du formulaire de recherche
        const searchForm = document.getElementById('search-bar');
        if (searchForm) {
            searchForm.addEventListener('submit', async (e) => {
                e.preventDefault();
                const searchInput = searchForm.querySelector('input[name="q"]').value.trim();
                
                if (!searchInput) {
                    alertPerso("info", "Veuillez entrer un numéro de compte à rechercher");
                    return;
                }
    
                try {
                    const response = await fetch(`/web/searchClient?q=${encodeURIComponent(searchInput)}`, {
                        headers: { 
                            'X-CSRFToken': getCSRFToken(),
                            'Accept': 'application/json'
                        }
                    });
    
                    if (!response.ok) throw new Error("Erreur lors de la recherche");
                    
                    const data = await response.json();
                    
                    if (data.length > 0) {
                        showClientDetails(data[0]); // Affiche le premier résultat
                    } else {
                        alertPerso("info", "Aucun client trouvé avec ce numéro de compte.");
                    }
                } catch (error) {
                    console.error(error);
                    alertPerso("error", error.message);
                }
            });
        }
    }

    function setupPoliceAssurance() {
        document.getElementById('genere_police')?.addEventListener('click', () => {
            document.getElementById('PopupAddPolice').style.display = 'flex';
        });
    
        document.getElementById('cancelAddPolice')?.addEventListener('click', () => {
            document.getElementById('PopupAddPolice').style.display = 'none';
        });
    
        document.getElementById('addPoliceForm')?.addEventListener('submit', async (event) => {
            event.preventDefault();
    
            const num_compte_client = document.getElementById('num_compte_client').value;
            const branche = document.getElementById('branche').value;
            const duree_couverture = document.getElementById('duree_couverture').value;
    
            try {
                const response = await fetch(`${API_BASE_URL}/police/generePolice`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCSRFToken()
                    },
                    body: JSON.stringify({ num_compte_client, branche_id: branche, duree_couverture: parseInt(duree_couverture) })
                });
    
                if (!response.ok) throw new Error("Erreur lors de la génération de la police d'assurance.");
                alertPerso("success","Police d'assurance générée avec succès.");
                location.reload();
            } catch (error) {
                console.error(error);
                alertPerso("error",error.message);
            }
        });

        document.querySelectorAll('.btn-view-police').forEach(button => {
            button.addEventListener('click', function() {
                PoliceDetails(this);
            });
        });

        document.querySelector('#PopupDetailsPolice .close')?.addEventListener('click', () => {
            document.getElementById('PopupDetailsPolice').style.display = 'none';
        });
    }

    function PoliceDetails(button) {
        const popup = document.getElementById('PopupDetailsPolice');

        document.getElementById('detail-num-police').textContent = button.dataset.numPolice || 'N/A';
        document.getElementById('detail-num-compte').textContent = button.dataset.numCompte || 'N/A';
        document.getElementById('detail-souscripteur').textContent = 
            `${button.dataset.clientNom || ''} ${button.dataset.clientPrenom || ''}`.trim() || 'N/A';
        document.getElementById('detail-branche').textContent = button.dataset.branche || 'N/A';
        document.getElementById('detail-agence').textContent = button.dataset.agence || 'N/A';
        document.getElementById('detail-duree').textContent = 
            button.dataset.duree ? `${button.dataset.duree} mois` : 'N/A';
        document.getElementById('detail-date-gen').textContent = button.dataset.dateGen || 'N/A';
        document.getElementById('detail-date-exp').textContent = button.dataset.dateExp || 'N/A';
        document.getElementById('detail-status').textContent = button.dataset.status || 'N/A';
        
        popup.style.display = 'flex';
    }

    function setupModifProfil() {
        const modifProfilButton = document.querySelector('.request');
        const modifProfilPopup = document.getElementById('PopupModifProfil');
        const cancelModifProfilButton = document.getElementById('cancelModifProfil');
    
        if (modifProfilButton && modifProfilPopup) {
            modifProfilButton.addEventListener('click', () => {
                modifProfilPopup.style.display = 'flex';
            });
        }
    
        if (cancelModifProfilButton) {
            cancelModifProfilButton.addEventListener('click', () => {
                modifProfilPopup.style.display = 'none';
            });
        }
    
        // Gestion de la soumission du formulaire de modification du profil
        const modifProfilForm = document.getElementById('modifProfilForm');
        if (modifProfilForm) {
            modifProfilForm.addEventListener('submit', async (event) => {
                event.preventDefault();
    
                const formData = new FormData(modifProfilForm);
                const userId = document.getElementById("modifProfilForm").dataset.userId;
                console.log("User ID récupéré:", userId);
    
                try {
                    const response = await fetch(`${API_BASE_URL}/auth/user/${userId}/upload_photo`, {
                        method: 'POST',
                        body: formData,
                        headers: {
                            'X-CSRFToken': getCSRFToken(),
                        },
                    });
    
                    if (!response.ok) throw new Error("Erreur lors de la modification du profil.");
                    const data = await response.json();
                    if (data.status === 'success') {
                        alertPerso("success","Profil modifié avec succès.");
                        modifProfilPopup.style.display = 'none';
                        location.reload();
                    } else {
                        alertPerso("error",data.message || "Erreur lors de la modification du profil.");
                    }
                } catch (error) {
                    console.error(error);
                    alertPerso("error",error.message);
                }
            });
        }
    }    
    
    function getCSRFToken() {
        return document.querySelector('input[name="csrfmiddlewaretoken"]')?.value || '';
    }  
})();