package handlers

import (
	"encoding/csv"
	"fmt"
	"net/http"
	"strconv"

	"github.com/Godofin/anderson-api-v1/internal/config"
	"github.com/Godofin/anderson-api-v1/internal/models"
	"github.com/gorilla/mux"
)

func ExportPassengersCSV(w http.ResponseWriter, r *http.Request) {
	tenantID := GetTenantID(r)
	vars := mux.Vars(r)
	excursionID, _ := strconv.Atoi(vars["id"])

	var bookings []models.Booking
	if err := config.DB.Where("excursion_id = ? AND tenant_id = ?", excursionID, tenantID).Find(&bookings).Error; err != nil {
		http.Error(w, "Erro ao buscar dados", http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "text/csv")
	w.Header().Set("Content-Disposition", fmt.Sprintf("attachment;filename=passageiros_excursao_%d.csv", excursionID))

	writer := csv.NewWriter(w)
	defer writer.Flush()

	// Header
	writer.Write([]string{"ID Reserva", "ID Cliente", "Valor Total", "Valor Pago", "Status Pagamento", "Status Check-In"})

	for _, b := range bookings {
		row := []string{
			strconv.Itoa(int(b.ID)),
			strconv.Itoa(int(b.ClientID)),
			fmt.Sprintf("%.2f", b.TotalValue),
			fmt.Sprintf("%.2f", b.DepositValue),
			string(b.PaymentStatus),
			string(b.CheckInStatus),
		}
		writer.Write(row)
	}
}
