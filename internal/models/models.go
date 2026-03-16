package models

import (
	"time"
)

type Plan string

const (
	Basic    Plan = "Basic"
	Pro      Plan = "Pro"
	Ultimate Plan = "Ultimate"
)

type Tenant struct {
	ID      uint   `gorm:"primaryKey" json:"id"`
	Name    string `gorm:"not null" json:"name"`
	Plan    Plan   `gorm:"default:'Basic'" json:"plan"`
	AdminID uint   `json:"admin_id"`
}

type User struct {
	ID       uint      `gorm:"primaryKey" json:"id"`
	TenantID uint      `gorm:"not null" json:"tenant_id"`
	Name     string    `gorm:"not null" json:"name"`
	Email    string    `gorm:"unique;not null" json:"email"`
	Password string    `gorm:"not null" json:"-"`
	Role     string    `gorm:"default:'Staff'" json:"role"` // Admin/Staff
	CreatedAt time.Time `json:"created_at"`
}

type Client struct {
	ID                     uint   `gorm:"primaryKey" json:"id"`
	TenantID               uint   `gorm:"not null" json:"tenant_id"`
	Name                   string `gorm:"not null" json:"name"`
	CPF                    string `gorm:"not null" json:"cpf"`
	Phone                  string `json:"phone"`
	FavoritePickupPointID  uint   `json:"favorite_pickup_point_id"`
}

type Excursion struct {
	ID           uint      `gorm:"primaryKey" json:"id"`
	TenantID     uint      `gorm:"not null" json:"tenant_id"`
	Destination  string    `gorm:"not null" json:"destination"`
	DepartureDate time.Time `gorm:"not null" json:"departure_date"`
	ReturnDate    time.Time `gorm:"not null" json:"return_date"`
	Price        float64   `gorm:"not null" json:"price"`
	TotalSeats   int       `gorm:"not null" json:"total_seats"`
	VehicleType  string    `json:"vehicle_type"`
	VehicleCount int       `json:"vehicle_count"`
	StopCount    int       `json:"stop_count"`
}

type PickupPoint struct {
	ID          uint      `gorm:"primaryKey" json:"id"`
	ExcursionID uint      `gorm:"not null" json:"excursion_id"`
	Location    string    `gorm:"not null" json:"location"`
	Time        time.Time `gorm:"not null" json:"time"`
}

type PaymentStatus string

const (
	Pending PaymentStatus = "Pendente"
	Partial PaymentStatus = "Parcial"
	Paid    PaymentStatus = "Pago"
)

type CheckInStatus string

const (
	Boarded  CheckInStatus = "Embarcou"
	Unboarded CheckInStatus = "Desembarcou"
)

type Booking struct {
	ID            uint          `gorm:"primaryKey" json:"id"`
	ClientID      uint          `gorm:"not null" json:"client_id"`
	ExcursionID   uint          `gorm:"not null" json:"excursion_id"`
	PickupPointID uint          `gorm:"not null" json:"pickup_point_id"`
	TotalValue    float64       `gorm:"not null" json:"total_value"`
	DepositValue  float64       `gorm:"default:0" json:"deposit_value"`
	PaymentStatus PaymentStatus `json:"payment_status"`
	CheckInStatus CheckInStatus `json:"check_in_status"`
	CheckInTime   *time.Time    `json:"check_in_time"`
}
