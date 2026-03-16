package handlers

import (
	"encoding/json"
	"net/http"
	"strconv"

	"github.com/Godofin/anderson-api-v1/internal/config"
	"github.com/Godofin/anderson-api-v1/internal/models"
	"github.com/gorilla/mux"
)

func ListClients(w http.ResponseWriter, r *http.Request) {
	tenantID := GetTenantID(r)
	var clients []models.Client
	
	query := config.DB.Where("tenant_id = ?", tenantID)
	
	// Busca rápida por nome ou CPF
	if search := r.URL.Query().Get("search"); search != "" {
		query = query.Where("name LIKE ? OR cpf LIKE ?", "%"+search+"%", "%"+search+"%")
	}

	if err := query.Find(&clients).Error; err != nil {
		http.Error(w, "Erro ao buscar clientes", http.StatusInternalServerError)
		return
	}

	json.NewEncoder(w).Encode(clients)
}

func GetClientHistory(w http.ResponseWriter, r *http.Request) {
	tenantID := GetTenantID(r)
	vars := mux.Vars(r)
	clientID, _ := strconv.Atoi(vars["id"])

	var bookings []models.Booking
	if err := config.DB.Where("client_id = ? AND tenant_id = ?", clientID, tenantID).Find(&bookings).Error; err != nil {
		http.Error(w, "Erro ao buscar histórico", http.StatusInternalServerError)
		return
	}

	var totalSpent float64
	for _, b := range bookings {
		totalSpent += b.DepositValue
	}

	response := map[string]interface{}{
		"bookings":    bookings,
		"total_spent": totalSpent,
	}

	json.NewEncoder(w).Encode(response)
}
