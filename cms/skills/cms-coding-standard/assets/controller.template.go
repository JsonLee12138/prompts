package module_name

import (
	"net/http"

	"github.com/JsonLee12138/headless-cms/core/http/binding"
	"github.com/JsonLee12138/headless-cms/core/http/responder"
	"github.com/casbin/casbin/v2"
	"github.com/go-chi/chi/v5"
)

type Controller struct {
	service          *Service
	responderFactory *responder.ResponderFactory
	enforcer         *casbin.Enforcer
}

func NewController(service *Service, factory *responder.ResponderFactory, enforcer *casbin.Enforcer) *Controller {
	return &Controller{
		service:          service,
		responderFactory: factory,
		enforcer:         enforcer,
	}
}

// List - 获取列表
func (c *Controller) List(w http.ResponseWriter, r *http.Request) {
	res := c.responderFactory.FromRequest(w, r)

	// 可选：权限检查
	// if ok, _ := c.enforcer.Enforce(r.Header.Get("user"), "module_name", "read"); !ok {
	// 	res.WriteError(http.StatusForbidden, responder.Error{Message: "无权访问"})
	// 	return
	// }

	// 解析查询参数
	var params struct {
		Page     int `json:"page" validate:"min=1,default=1"`
		PageSize int `json:"pageSize" validate:"min=1,max=100,default=20"`
	}
	if err := binding.Query(r, ¶ms); err != nil {
		res.WriteError(http.StatusBadRequest, responder.Error{Message: err.Error()})
		return
	}

	// 调用 Service
	list, total, err := c.service.List(r.Context(), params.Page, params.PageSize)
	if err != nil {
		res.WriteError(http.StatusInternalServerError, responder.Error{Message: err.Error()})
		return
	}

	// 返回分页列表
	pagination := responder.NewPagination(params.Page, params.PageSize, total)
	res.WriteList(list, pagination)
}

// Get - 获取单条
func (c *Controller) Get(w http.ResponseWriter, r *http.Request) {
	res := c.responderFactory.FromRequest(w, r)

	id := chi.URLParam(r, "id")
	if id == "" {
		res.WriteError(http.StatusBadRequest, responder.Error{Message: "ID is required"})
		return
	}

	// 可选：权限检查
	// if ok, _ := c.enforcer.Enforce(r.Header.Get("user"), "module_name", "read"); !ok {
	// 	res.WriteError(http.StatusForbidden, responder.Error{Message: "无权访问"})
	// 	return
	// }

	item, err := c.service.Get(r.Context(), id)
	if err != nil {
		res.WriteError(http.StatusNotFound, responder.Error{Message: err.Error()})
		return
	}

	res.Write(http.StatusOK, item)
}

// Create - 创建
func (c *Controller) Create(w http.ResponseWriter, r *http.Request) {
	res := c.responderFactory.FromRequest(w, r)

	// 可选：权限检查
	// if ok, _ := c.enforcer.Enforce(r.Header.Get("user"), "module_name", "create"); !ok {
	// 	res.WriteError(http.StatusForbidden, responder.Error{Message: "无权创建"})
	// 	return
	// }

	var dto CreateDTO
	if err := binding.JSON(r, &dto); err != nil {
		res.WriteError(http.StatusBadRequest, responder.Error{Message: err.Error()})
		return
	}

	item, err := c.service.Create(r.Context(), &dto)
	if err != nil {
		res.WriteError(http.StatusInternalServerError, responder.Error{Message: err.Error()})
		return
	}

	res.Write(http.StatusOK, item)
}

// Update - 更新
func (c *Controller) Update(w http.ResponseWriter, r *http.Request) {
	res := c.responderFactory.FromRequest(w, r)

	id := chi.URLParam(r, "id")
	if id == "" {
		res.WriteError(http.StatusBadRequest, responder.Error{Message: "ID is required"})
		return
	}

	// 可选：权限检查
	// if ok, _ := c.enforcer.Enforce(r.Header.Get("user"), "module_name", "update"); !ok {
	// 	res.WriteError(http.StatusForbidden, responder.Error{Message: "无权更新"})
	// 	return
	// }

	var dto UpdateDTO
	if err := binding.JSON(r, &dto); err != nil {
		res.WriteError(http.StatusBadRequest, responder.Error{Message: err.Error()})
		return
	}

	item, err := c.service.Update(r.Context(), id, &dto)
	if err != nil {
		res.WriteError(http.StatusInternalServerError, responder.Error{Message: err.Error()})
		return
	}

	res.Write(http.StatusOK, item)
}

// Delete - 删除
func (c *Controller) Delete(w http.ResponseWriter, r *http.Request) {
	res := c.responderFactory.FromRequest(w, r)

	id := chi.URLParam(r, "id")
	if id == "" {
		res.WriteError(http.StatusBadRequest, responder.Error{Message: "ID is required"})
		return
	}

	// 可选：权限检查
	// if ok, _ := c.enforcer.Enforce(r.Header.Get("user"), "module_name", "delete"); !ok {
	// 	res.WriteError(http.StatusForbidden, responder.Error{Message: "无权删除"})
	// 	return
	// }

	if err := c.service.Delete(r.Context(), id); err != nil {
		res.WriteError(http.StatusInternalServerError, responder.Error{Message: err.Error()})
		return
	}

	res.Write(http.StatusOK, responder.Response{
		Data: map[string]string{"message": "deleted"},
	})
}
