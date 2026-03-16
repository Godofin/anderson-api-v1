package handlers

import (
	"encoding/json"
	"net/http"
	"strconv"

	"github.com/Godofin/anderson-api-v1/internal/config"
	"github.com/Godofin/anderson-api-v1/internal/models"
	"github.com/Godofin/anderson-api-v1/internal/repository"
	"github.com/gorilla/mux"
)

func CreateExcursion(w http.ResponseWriter, r *http.Request) {
	tenantID := GetTenantID(r)
	
	// Validação de limite do plano
	if err := repository.CheckExcursionLimit(tenantID); err != nil {
		if err == repository.ErrPlanLimitExceeded {
			http.Error(w, "Limite de excursões do plano atingido", http.StatusForbidden)
			return
		}
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	var excursion models.Excursion
	if err := json.NewDecoder(r.Body).Decode(&excursion); err != nil {
		http.Error(w, "Payload inválido", http.StatusBadRequest)
		return
	}

	excursion.TenantID = tenantID
	if err := config.DB.Create(&excursion).Error; err != nil {
		http.Error(w, "Erro ao salvar excursão", http.StatusInternalServerError)
		return
	}

	w.WriteHeader(http.StatusCreated)
	json.NewEncoder(w).Encode(excursion)
}

func ListExcursions(w http.ResponseWriter, r *http.Request) {
	tenantID := GetTenantID(r)
	var excursions []models.Excursion
	
	// Filtro por tenant (Isolamento de Dados)
	query := config.DB.Where("tenant_id = ?", tenantID)

	// Filtros adicionais (Ex: destino)
	if dest := r.URL.Query().Get("destination"); dest != "" {
		query = query.Where("destination LIKE ?", "%"+dest+"%")
	}

	if err := query.Find(&excursions).Error; err != nil {
		http.Error(w, "Erro ao buscar excursões", http.StatusInternalServerError)
		return
	}

	json.NewEncoder(w).Encode(excursions)
}

func GetPassengers(w http.ResponseWriter, r *http.Request) {
	tenantID := GetTenantID(r)
	vars := mux.Vars(r)
	excursionID, _ := strconv.Atoi(vars["id"])

	var bookings []models.Booking
	// Join com Client para pegar nomes
	if err := config.DB.Where("excursion_id = ? AND tenant_id = ?", excursionID, tenantID).Find(&bookings).Error; err != nil {
		http.Error(w, "Erro ao buscar passageiros", http.StatusInternalServerError)
		return
	}

	json.NewEncoder(w).Encode(bookings)
}
