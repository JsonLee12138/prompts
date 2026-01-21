package module_name

import (
	"github.com/JsonLee12138/headless-cms/cms/_gen"
	"github.com/JsonLee12138/headless-cms/core/http/responder"
	"github.com/casbin/casbin/v2"
	"github.com/go-chi/chi/v5"
)

type Module struct {
	controller *Controller
	service    *Service
}

func NewModule(client *_gen.Client, enforcer *casbin.Enforcer) *Module {
	// 1. 创建 Service
	service := NewService(client)

	// 2. 创建 Responder Factory
	responderFactory := responder.NewResponderFactory(responder.DefaultPanicFn)

	// 3. 创建 Controller
	controller := NewController(service, responderFactory, enforcer)

	return &Module{
		controller: controller,
		service:    service,
	}
}

func (m *Module) Setup(r chi.Router) {
	r.Route("/module_name", func(r chi.Router) {
		// 可选：添加认证中间件
		// r.Use(middleware.APIKeyAuth(...))

		r.Get("/", m.controller.List)
		r.Get("/{id}", m.controller.Get)
		r.Post("/", m.controller.Create)
		r.Put("/{id}", m.controller.Update)
		r.Delete("/{id}", m.controller.Delete)
	})
}