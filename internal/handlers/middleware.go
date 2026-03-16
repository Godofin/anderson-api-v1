package handlers

import (
	"context"
	"net/http"
	"strings"

	_ "github.com/golang-jwt/jwt/v5"
)

type contextKey string

const (
	TenantIDKey contextKey = "tenant_id"
	UserIDKey   contextKey = "user_id"
	UserRoleKey contextKey = "user_role"
)

func AuthMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		authHeader := r.Header.Get("Authorization")
		if authHeader == "" {
			http.Error(w, "Token de autorização ausente", http.StatusUnauthorized)
			return
		}

		_ = strings.TrimPrefix(authHeader, "Bearer ")
		
		// Para fins deste desenvolvimento, vamos simular a validação do token
		// Em produção, você deve validar o token JWT aqui
		
		// Simulando extração de dados do token (TenantID, UserID, Role)
		// Estes dados viriam do payload do JWT
		tenantID := uint(1) // Simulado
		userID := uint(1)   // Simulado
		role := "Admin"     // Simulado

		ctx := context.WithValue(r.Context(), TenantIDKey, tenantID)
		ctx = context.WithValue(ctx, UserIDKey, userID)
		ctx = context.WithValue(ctx, UserRoleKey, role)

		next.ServeHTTP(w, r.WithContext(ctx))
	})
}

// GetTenantID recupera o ID do tenant do contexto da requisição
func GetTenantID(r *http.Request) uint {
	if tenantID, ok := r.Context().Value(TenantIDKey).(uint); ok {
		return tenantID
	}
	return 0
}
