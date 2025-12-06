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

Found in `assets/data/dialogue.json`, which contains all the dialogue in the
game. All dialogues must be identifiable by a unique id with a one-to-one
relation to an npc id.

A dialogue object is an array / list of strings, where each string represents
a line said by the npc.

An example dialogue would be:

```json
"Tiso": [
  "This is the first dialogue line of this npc.",
  "This is the second dialogue line of this npc. It can of course be a lot longer than this.",
  "This is the last dialogue line of this npc."
]
```

## Shops

Found in `assets/data/shops.json`, which contains all the shops in the game.
All shops must be identifiable by a unique id with a one-to-one relation to
an npc id, who has `has_shop` set to `true`, otherwise the shop will never
be accessible.

A shop object is an array / list of Item ids which the shop contains.

An example shop would be:

```json
"Example_Npc": [
  "Mask_1",
  "Mask_2",
  "Mask_3"
]
```

## Enemies

!!! IMPORTANT NOTICE !!!

As the implementation of the enemies isn't yet finalised this section is
subject to change and parts of the information provided may be out of date.
As of 06.12.2025, 15:58 the information provided is up to date.

Found in `assets/data/enemies.json`, which contains all the enemies in the game.
All enemies must be identifiable by a unique id.

An enemy object must contain:

- `type`: string, the type of enemy that needs to be loaded (check `src/core/utils.py` enemies dict for possible options)
- `sprite_path`: string representing the path to the folder that contains all the sprites of the enemy
- `scale`: a double by which the npc sprite is scaled
- `max_health`: int, the max health of the enemy
- `damage`: int, the damage dealt by the enemy to the player on contact
- `drop_curr1`: int, the amount of `currency1` awarded to the player when the enemy is killed
- `drop_curr2`: int, the amount of `currency2` awarded to the player when the enemy is killed
- `drop_curr3`: int, the amount of `currency3` awarded to the player when the enemy is killed
- `drop_curr4`: int, the amount of `currency4` awarded to the player when the enemy is killed
- `frame_duration`: int, the duration of a single frame of the enemy animation

An example enemy would be:

```json
"Example_Enemy_1": {
	"type": "GroundEnemy",
	"sprite_path": "../assets/sprites/crawler/walk_0.png",
	"scale": 0.7,
	"max_health": 1,
	"damage": 1,
	"drop_curr1": 1,
	"drop_curr2": 1,
	"drop_curr3": 1,
	"drop_curr4": 1,
    "frame_duration": 80
}
```
