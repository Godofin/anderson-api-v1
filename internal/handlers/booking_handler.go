package handlers

import (
	"encoding/json"
	"net/http"
	"strconv"
	"time"

	"github.com/Godofin/anderson-api-v1/internal/config"
	"github.com/Godofin/anderson-api-v1/internal/models"
	"github.com/gorilla/mux"
)

func CreateBooking(w http.ResponseWriter, r *http.Request) {
	tenantID := GetTenantID(r)
	var booking models.Booking
	if err := json.NewDecoder(r.Body).Decode(&booking); err != nil {
		http.Error(w, "Payload inválido", http.StatusBadRequest)
		return
	}

	// Verifica vagas ocupadas
	var excursion models.Excursion
	if err := config.DB.Where("id = ? AND tenant_id = ?", booking.ExcursionID, tenantID).First(&excursion).Error; err != nil {
		http.Error(w, "Excursão não encontrada", http.StatusNotFound)
		return
	}

	var occupiedSeats int64
	config.DB.Model(&models.Booking{}).Where("excursion_id = ?", booking.ExcursionID).Count(&occupiedSeats)

	if int(occupiedSeats) >= excursion.TotalSeats {
		http.Error(w, "Não há vagas disponíveis", http.StatusConflict)
		return
	}

	// Lógica de Status de Pagamento
	booking.PaymentStatus = calculatePaymentStatus(booking.TotalValue, booking.DepositValue)
	
	if err := config.DB.Create(&booking).Error; err != nil {
		http.Error(w, "Erro ao criar reserva", http.StatusInternalServerError)
		return
	}

	json.NewEncoder(w).Encode(booking)
}

func UpdatePayment(w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
	bookingID, _ := strconv.Atoi(vars["id"])

	var input struct {
		DepositValue float64 `json:"deposit_value"`
	}
	if err := json.NewDecoder(r.Body).Decode(&input); err != nil {
		http.Error(w, "Payload inválido", http.StatusBadRequest)
		return
	}

	var booking models.Booking
	if err := config.DB.First(&booking, bookingID).Error; err != nil {
		http.Error(w, "Reserva não encontrada", http.StatusNotFound)
		return
	}

	booking.DepositValue = input.DepositValue
	booking.PaymentStatus = calculatePaymentStatus(booking.TotalValue, booking.DepositValue)

	config.DB.Save(&booking)
	json.NewEncoder(w).Encode(booking)
}

func CheckIn(w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
	bookingID, _ := strconv.Atoi(vars["id"])

	var input struct {
		Status models.CheckInStatus `json:"status"`
	}
	if err := json.NewDecoder(r.Body).Decode(&input); err != nil {
		http.Error(w, "Payload inválido", http.StatusBadRequest)
		return
	}

	now := time.Now()
	if err := config.DB.Model(&models.Booking{}).Where("id = ?", bookingID).Updates(map[string]interface{}{
		"check_in_status": input.Status,
		"check_in_time":   &now,
	}).Error; err != nil {
		http.Error(w, "Erro ao realizar check-in", http.StatusInternalServerError)
		return
	}

	w.WriteHeader(http.StatusOK)
}

func calculatePaymentStatus(total, deposit float64) models.PaymentStatus {
	if deposit == 0 {
		return models.Pending
	}
	if deposit < total {
		return models.Partial
	}
	return models.Paid
}
