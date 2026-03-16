package config

import (
	"fmt"
	"log"
	"os"

	"github.com/Godofin/anderson-api-v1/internal/models"
	"gorm.io/driver/postgres"
	"gorm.io/gorm"
)

var DB *gorm.DB

func InitDB() {
	host := os.Getenv("DB_HOST")
	user := os.Getenv("DB_USER")
	password := os.Getenv("DB_PASSWORD")
	dbname := os.Getenv("DB_NAME")
	port := os.Getenv("DB_PORT")

	dsn := fmt.Sprintf("host=%s user=%s password=%s dbname=%s port=%s sslmode=disable", host, user, password, dbname, port)
	db, err := gorm.Open(postgres.Open(dsn), &gorm.Config{})
	if err != nil {
		log.Fatal("Falha ao conectar ao banco de dados:", err)
	}

	// Auto Migration
	db.AutoMigrate(
		&models.Tenant{},
		&models.User{},
		&models.Client{},
		&models.Excursion{},
		&models.PickupPoint{},
		&models.Booking{},
	)

	DB = db
}
