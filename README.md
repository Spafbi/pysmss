# Simplified Miscreated Server Setup - Python Edition
This is a complete rewrite of the legacy *Simplified Miscreated Server Setup* script. It was written in just a few hours and is somewhat sloppy...but it works.

The script doesn't yet auto-update, nor does it currently prompt for server values. Rather, all configurable values may be populated in a [smss.json](smss.example.log) configuration file. If values aren't specified, defaults will be used.

## Configurable JSON values

| variable | default (if not defined) | `hosting.cfg` equivalent |
| -------- | ------------------------ | ------------------------ |
| asm_maxMultiplier | 1 | asm_maxMultiplier |
| asm_percent | 60 | asm_percent |
| base_rules | 1 | g_gameRules_bases |
| bind_ip | '0.0.0.0' | N/A |
| camera | 0 | g_gameRules_Camera |
| connection_messages | false | sv_msg_conn |
| crafting_multiplier | 1 | g_craftingSpeedMultiplier |
| death_messages | false | sv_msg_death |
| enable_rcon | true | N/A |
| enable_upnp | false | N/A |
| enable_whitelist | false | N/A |
| force_pattern | -1 | wm_pattern |
| force_time | -1 | wm_forceTime |
| grant_guides | false | N/A |
| horde_cooldown | 900 | asm_hordeCooldown |
| idle_kick_seconds | 300 | g_idleKickTime |
| infinite_stamina | 0 | g_playerInfiniteStamina |
| map | islands | N/A |
| max_corpse_time | 1200 | pcs_maxCorpseTime |
| max_players | 36 | N/A |
| max_uptime | 12 | max_uptime |
| mod_ids | (empty list) | steam_ugc |
| motd_a | false | sv_motd |
| motd_b | false | sv_url |
| no_bans | false | sv_noBannedAccounts |
| ping_limit | 0 | asm_hordeCoolg_pinglimitdown |
| ping_limit_grace_timer | 60 | g_pingLimitGraceTimer |
| ping_limit_timer | 60 | g_pingLimitTimer |
| port | 64090 | N/A |
| rcon_password | (randomized) | http_password |
| reset_base_despawn_clan_ids | `(empty list)` | N/A |
| reset_base_despawn_ids | `(empty list)` | N/A |
| reset_bases | false | N/A |
| reset_tent_despawn_clan_ids | `(empty list)` | N/A |
| reset_tent_despawn_ids | `(empty list)` | N/A |
| reset_tents | false | N/A |
| reset_vehicle_despawn_clan_ids | `(empty list)` | N/A |
| reset_vehicle_despawn_ids | `(empty list)` | N/A |
| reset_vehicles | false | N/A |
| server_id | 100 or first value in db | N/A |
| server_name | Miscreated Self-hosted Server#(random#) | sv_servername |
| theros_admin_mod | false | N/A |
| theros_admin_mod_admin_ids | false | N/A |
| time_day_minutes | 180 | wm_timeScale |
| time_night_minutes | 60 | wm_timeScaleNight |
| time_offset | -1 | wm_timeOffset |

## Despawn prevention
### Global despawn prevention
Do you have a casual server on which you wish to prevent bases, vehicles, and/or tents from despawning? Just add the following to the [smss.json](smss.example.json) configuration file:
```json
{
    "reset_bases": true,
    "reset_tents": true,
    "reset_vehicles": true
}
```
### Clan and individual ID granular control
It's possible to prevent the despawning of bases, as well as vehicles and tents at given bases, by specifying a list of Steam IDs and/or internal clan IDs. A use case for this is to allow for an admin account, or admin clan, to have resources which don't despawn so that they may maintain such resources for events or execution of admin duties without having to regularly log in the account(s) to refresh resources.

#### Example
If you wish to refresh bases for admins, but only vehicles and tents for two SteamID64s, then the JSON for this would look like this:
256512
```json
{
    "reset_base_despawn_clan_ids": [256512],
    "reset_tent_despawn_ids": [76561198027894420, 76561198822937906],
    "reset_vehicle_despawn_ids": [76561198027894420, 76561198822937906]
}
```
## Theros' Admin Mod
To make it easy to get started with *admin powers* on a server you can enable [Theros' admin mod](https://steamcommunity.com/sharedfiles/filedetails/?id=2011185435) and specify the SteamID64 accounts for admins in the [smss.json](smss.example.json) file:
```json
{
    "theros_admin_mod": true,
    "theros_admin_mod_admin_ids": [76561198027894420, 76561198822937906]
}
```
Of course, you'll want to use your SteamID64 values and not the values in the above examples.

## JSON configuration example
There is a basic [smss.json](smss.example.json) example file you may view. Here's another full example incorporating portions of the above despawn examples:
```json
{
    "port": 64090,
    "rcon_password": "secret-password",
    "reset_bases": true,
    "reset_tent_despawn_ids": [76561198027894420, 76561198822937906],
    "server_name": "My Miscreated server",
    "theros_admin_mod": true,
    "theros_admin_mod_admin_ids": [76561198027894420, 76561198822937906]
}
```
The above example sets:
* the base port of the game server - the RCON port is always that value + 4)
* the RCON password
* resets the despawn timer for all bases
* resets tents at bases belonging to the two specified SteamID64 accounts
* sets the server name to *My Miscreated server*
* enables the admin mod
* and adds two SteamID64 accounts to the admin mod's configuration file 