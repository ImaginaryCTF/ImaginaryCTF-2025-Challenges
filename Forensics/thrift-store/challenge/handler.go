package main

import (
	"context"

	"github.com/ImaginaryCTF/ImaginaryCTF-2025-Challenges/forensics/thrift-store/challenge/gen-go/store"
)

var items []*store.StoreItem

func init() {
	items = []*store.StoreItem{
		{
			ItemId:      "apple-red-delicious",
			Name:        "Red Delicious Apple",
			Price:       120,
			Description: ptr("Crisp and sweet red apples, perfect for snacking."),
		},
		{
			ItemId: "banana",
			Name:   "Banana",
			Price:  90,
		},
		{
			ItemId:      "whole-milk-1l",
			Name:        "Whole Milk (1L)",
			Price:       250,
			Description: ptr("Fresh whole milk sourced from local farms."),
		},
		{
			ItemId: "brown-eggs-dozen",
			Name:   "Brown Eggs (Dozen)",
			Price:  450,
		},
		{
			ItemId:      "bread-sourdough-loaf",
			Name:        "Sourdough Bread Loaf",
			Price:       500,
			Description: ptr("Artisan sourdough with a crispy crust."),
		},
		{
			ItemId: "carrots-1kg",
			Name:   "Carrots (1kg)",
			Price:  300,
		},
		{
			ItemId:      "chicken-breast-500g",
			Name:        "Chicken Breast (500g)",
			Price:       750,
			Description: ptr("Lean chicken breast, skinless and boneless."),
		},
		{
			ItemId: "rice-basmati-1kg",
			Name:   "Basmati Rice (1kg)",
			Price:  600,
		},
		{
			ItemId:      "olive-oil-500ml",
			Name:        "Extra Virgin Olive Oil (500ml)",
			Price:       1200,
			Description: ptr("Cold-pressed, premium quality olive oil."),
		},
		{
			ItemId: "cheddar-cheese-200g",
			Name:   "Cheddar Cheese (200g)",
			Price:  550,
		},
		{
			ItemId:      "tomatoes-500g",
			Name:        "Tomatoes (500g)",
			Price:       280,
			Description: ptr("Juicy ripe tomatoes, great for salads."),
		},
		{
			ItemId: "onions-1kg",
			Name:   "Onions (1kg)",
			Price:  250,
		},
		{
			ItemId:      "orange-juice-1l",
			Name:        "Orange Juice (1L)",
			Price:       400,
			Description: ptr("100% pure squeezed orange juice."),
		},
		{
			ItemId: "potatoes-2kg",
			Name:   "Potatoes (2kg)",
			Price:  350,
		},
		{
			ItemId:      "yogurt-plain-500g",
			Name:        "Plain Yogurt (500g)",
			Price:       320,
			Description: ptr("Thick and creamy natural yogurt."),
		},
		{
			ItemId: "flag",
			Name:   "Flag",
			Price:  9999,
		},
	}
}

type StoreHandler struct {
	basketStore BasketStore
}

func NewStoreHandler(bs BasketStore) *StoreHandler {
	return &StoreHandler{bs}
}

func (h *StoreHandler) CreateBasket(ctx context.Context) (*store.CreateBasketResponse, error) {
	id, _ := h.basketStore.CreateBasket()
	return &store.CreateBasketResponse{BasketId: id}, nil
}

func ptr(s string) *string {
	return &s
}

func (h *StoreHandler) GetInventory(ctx context.Context) (*store.GetInventoryResponse, error) {

	return &store.GetInventoryResponse{Items: items}, nil
}

func (h *StoreHandler) GetBasket(ctx context.Context, basketId string) (*store.GetBasketResponse, error) {
	if basketId == "" {
		err := store.NewBasketNotFound()
		err.Message = "Basket ID cannot be empty"
		return nil, err
	}

	basket, err := h.basketStore.GetBasket(basketId)
	if err != nil {
		return nil, err
	}
	return &store.GetBasketResponse{Items: basket}, nil
}

func getItemById(itemId string) *store.StoreItem {
	for _, item := range items {
		if item.ItemId == itemId {
			return item
		}
	}
	return nil
}

func (h *StoreHandler) AddToBasket(ctx context.Context, basketId string, itemId string) error {
	item := getItemById(itemId)
	if item == nil {
		err := store.NewItemNotFound()
		err.Message = "Item not found"
		return err
	}

	err := h.basketStore.AddToBasket(basketId, itemId)
	if err != nil {
		response := store.NewBasketNotFound()
		response.Message = "Basket not found"
		return response
	}
	return nil
}

func (h *StoreHandler) Pay(ctx context.Context, basketId string, total int64) (*store.PayResponse, error) {
	basket, err := h.basketStore.GetBasket(basketId)
	if err != nil {
		response := store.NewBasketNotFound()
		response.Message = "Basket not found"
		return nil, response
	}

	flagInBasket := false
	basketTotal := int64(0)
	for _, item := range basket {
		if item.ItemId == "flag" {
			flagInBasket = true
		}
		if maybeItem := getItemById(item.ItemId); maybeItem != nil {
			basketTotal += maybeItem.Price
		}
	}

	if basketTotal != total {
		response := store.NewWrongTotal()
		response.Message = "Total does not match basket total"
		return nil, response
	}

	flag := "ictf{l1k3_gRPC_bUt_l3ss_g0ogly}"

	response := &store.PayResponse{}
	if flagInBasket {
		response.Flag = &flag
	}

	h.basketStore.DeleteBasket(basketId)

	return response, nil
}
