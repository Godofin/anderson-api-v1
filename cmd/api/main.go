package main

import (
	"fmt"
	"log"
	"net/http"
	"os"

	"github.com/Godofin/anderson-api-v1/internal/config"
	"github.com/Godofin/anderson-api-v1/internal/handlers"
	"github.com/gorilla/mux"
)

func main() {
	// Inicializa o banco de dados (Necessário setar variáveis de ambiente)
	if os.Getenv("DB_HOST") != "" {
		config.InitDB()
	} else {
		fmt.Println("Variáveis de ambiente do banco não configuradas. Rodando sem banco para teste.")
	}

	r := mux.NewRouter()

	// Middleware de Autenticação e Multi-tenancy
	api := r.PathPrefix("/api/v1").Subrouter()
	api.Use(handlers.AuthMiddleware)

	// Rotas de Excursões
	api.HandleFunc("/excursions", handlers.CreateExcursion).Methods("POST")
	api.HandleFunc("/excursions", handlers.ListExcursions).Methods("GET")
	api.HandleFunc("/excursions/{id}/passengers", handlers.GetPassengers).Methods("GET")
	api.HandleFunc("/excursions/{id}/export", handlers.ExportPassengersCSV).Methods("GET")

	// Rotas de Reservas
	api.HandleFunc("/bookings", handlers.CreateBooking).Methods("POST")
	api.HandleFunc("/bookings/{id}/payment", handlers.UpdatePayment).Methods("PATCH")
	api.HandleFunc("/bookings/{id}/checkin", handlers.CheckIn).Methods("PATCH")

	// Rotas de Clientes
	api.HandleFunc("/clients", handlers.ListClients).Methods("GET")
	api.HandleFunc("/clients/{id}/history", handlers.GetClientHistory).Methods("GET")

	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
	}

	fmt.Printf("Servidor rodando na porta %s...\n", port)
	log.Fatal(http.ListenAndServe(":"+port, r))
}
