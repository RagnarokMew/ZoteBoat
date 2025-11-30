# On the Subject of JSON Data

The below document will detail the structure of the json data and serve as a
guide to extend it.

## Items

Found in `assets/data/items.json`, which contains all the existing items in the game.
An item object implements the attributes of the `ShopItem` class and is identified
by an id. For a complete list of item ids please check in `src/core/player_stats.py`
the `self.unlocks` attribute or in `src/core/shop.py` the `unlock_handler`.

An item object MUST contain:

- `display_name`: a string representing the name of the item which will be displayed in a shop
- `description`: a string which contains a description of the item to be displayed in a shop
- `currency`: string which describes which currency is used to purchase the item
- `price`: integer which describes the amount of currency consumed to purchase the item

The currency must be set to one of the following: `currency1`, `currency2`,
`currency3`, `currency4`.

An example item would be:

```json
"Mask_1": {
  "display_name": "Mask",
  "description": "Ah, this old thing... I found it on the ground a while back, but don't remember where. It looks pretty so it's got to be worth a bit.\n\n(Increases max hp by 1)",
  "currency": "currency1",
  "price": 150
}
```

To add another item to the game you would need to modify the following files:

- `src/core/shop.py`: in `ShopHandler.unlock()` you would need to add a handler function and value;
- `src/core/player_stats.py`: you would need to define an entry in the `self.unlocks` dict with the item id; (ONLY IF the item isn't repurchaseable)

## NPCs

Found in `assets/data/npcs.json`, which contains all the npcs in the game. All npcs
MUST BE identifiable by a unique id.

An npc object MUST contain:

- `name`: a string representing the name of the npc
- `title`: a string representing the title / small description of the npc
- `has_shop`: a boolean, `true` if the npc has a shop, `false` otherwise
- `sprite_path`: a string containing the path to the sprite of the npc
- `scale`: a double by which the npc sprite is scaled

ADDITIONALY an npc SHOULD also have a dialogue associated with its id, otherwise
some default dialogue will be used when speaking to the npc.

An example npc would be:

```json
"Example_Npc_Id": {
  "name": "Tiso",
  "title": "Ambitious Fool",
  "has_shop": false,
  "sprite_path": "assets/sprites/tiso_sprite.png",
  "scale": 1
}
```

## Dialogue

## Shops
