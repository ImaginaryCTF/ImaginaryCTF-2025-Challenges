package main

import (
	"sync"

	"github.com/ImaginaryCTF/ImaginaryCTF-2025-Challenges/forensics/thrift-store/challenge/gen-go/store"
	"github.com/google/uuid"
)

type BasketStore interface {
	CreateBasket() (string, error)
	GetBasket(basketId string) ([]*store.BasketItem, error)
	AddToBasket(basketId string, itemId string) error
	DeleteBasket(basketId string) error
}

type InMemoryBasketStore struct {
	data map[string][]*store.BasketItem
	mu   sync.RWMutex
}

func (s *InMemoryBasketStore) CreateBasket() (string, error) {
	s.mu.Lock()
	defer s.mu.Unlock()

	basketId := uuid.NewString()
	s.data[basketId] = []*store.BasketItem{}

	return basketId, nil
}

func (s *InMemoryBasketStore) GetBasket(basketId string) ([]*store.BasketItem, error) {
	s.mu.RLock()
	defer s.mu.RUnlock()

	if items, exists := s.data[basketId]; exists {
		return items, nil
	}

	return nil, store.NewBasketNotFound()
}

func (s *InMemoryBasketStore) AddToBasket(basketId string, itemId string) error {
	s.mu.Lock()
	defer s.mu.Unlock()

	if _, exists := s.data[basketId]; !exists {
		return store.NewBasketNotFound()
	}

	for _, item := range s.data[basketId] {
		if item.ItemId == itemId {
			item.Amount++
			return nil
		}
	}

	s.data[basketId] = append(s.data[basketId], &store.BasketItem{ItemId: itemId, Amount: 1})
	return nil
}

func (s *InMemoryBasketStore) DeleteBasket(basketId string) error {
	s.mu.Lock()
	defer s.mu.Unlock()

	if _, exists := s.data[basketId]; !exists {
		return store.NewBasketNotFound()
	}
	delete(s.data, basketId)
	return nil
}
