package repository

import (
	"errors"
	"github.com/Godofin/anderson-api-v1/internal/config"
	"github.com/Godofin/anderson-api-v1/internal/models"
)

var (
	ErrPlanLimitExceeded = errors.New("limite do plano excedido")
)

func CheckExcursionLimit(tenantID uint) error {
	var tenant models.Tenant
	if err := config.DB.First(&tenant, tenantID).Error; err != nil {
		return err
	}

	var count int64
	config.DB.Model(&models.Excursion{}).Where("tenant_id = ?", tenantID).Count(&count)

	limit := 0
	switch tenant.Plan {
	case models.Basic:
		limit = 20
	case models.Pro:
		limit = 100
	case models.Ultimate:
		limit = 999999 // Sem limite prático
	}

	if int(count) >= limit {
		return ErrPlanLimitExceeded
	}

	return nil
}

func CheckStaffLimit(tenantID uint) error {
	var tenant models.Tenant
	if err := config.DB.First(&tenant, tenantID).Error; err != nil {
		return err
	}

	var count int64
	config.DB.Model(&models.User{}).Where("tenant_id = ?", tenantID).Count(&count)

	limit := 0
	switch tenant.Plan {
	case models.Basic:
		limit = 2 // 1 Admin + 1 Staff
	case models.Pro:
		limit = 5 // Exemplo de limite Pro
	case models.Ultimate:
		limit = 999999
	}

	if int(count) >= limit {
		return ErrPlanLimitExceeded
	}

	return nil
}
