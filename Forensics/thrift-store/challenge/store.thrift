
struct StoreItem {
    1: required string itemId;
    2: required string name;
    3: required i64 price;
    4: optional string description;
}

struct BasketItem {
    1: required string itemId;
    2: required i8 amount;
}

struct CreateBasketResponse {
    1: required string basketId;
}

struct GetInventoryResponse {
    1: required list<StoreItem> items;
}

struct GetBasketResponse {
    1: required list<BasketItem> items;
}

struct PayResponse {
    1: optional string flag;
}

exception BasketNotFound {
    1: required string message;
}

exception ItemNotFound {
    1: required string message;
}

exception WrongTotal {
    1: required string message;
}

service Store {
    CreateBasketResponse createBasket(),
    GetInventoryResponse getInventory(),
    GetBasketResponse getBasket(1: string basketId) throws (1: BasketNotFound basketNotFound),
    void addToBasket(1: string basketId, 2: string itemId) throws (1: BasketNotFound basketNotFound, 2: ItemNotFound itemNotFound),
    PayResponse pay(1: string basketId, 2: i64 total) throws (1: BasketNotFound basketNotFound, 2: WrongTotal wrongTotal);
}
