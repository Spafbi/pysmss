# Simplified Miscreated Server Setup - Python Edition
This is a complete rewrite of the legacy *Simplified Miscreated Server Setup* script. It was written in just a few hours and is somewhat sloppy...but it works.

The script doesn't yet auto-update, nor does it currently prompt for server values. Rather, all desired configurable values may be populated in a [smss.json](smss.example.json) configuration file. If values aren't specified, defaults will be used.

## Running the script
At a minumum, download and place both [SMSSv2.cmd](SMSSv2.cmd) and [SMSSv2.py](SMSSv2.py) in an empty directory. Execute the [SMSSv2.cmd](SMSSv2.cmd) script to setup and start the server. While the server will start with a default configuration, it is suggested you create an [smss.json](smss.example.json) file with at least the `server_name` configured.

### Configurable JSON values
If a variable has a `hosting.cfg` equivalent, you can find a description for most of the variables here: [https://servers.miscreatedgame.com/help](https://servers.miscreatedgame.com/help)

| variable | default (if not defined) | `hosting.cfg` equivalent |
| -------- | ------------------------ | ------------------------ |
| ai_corpses_max | `20` | as_corpseCountMax |
| ai_corpses_removal | `300` | as_corpseRemovalTime |
| asm_maxMultiplier | `1` | asm_maxMultiplier |
| asm_percent | `60` | asm_percent |
| base_rules | `1` | g_gameRules_bases |
| bind_ip | `0.0.0.0` | N/A |
| camera | `0` | g_gameRules_Camera |
| connection_messages | `false` | sv_msg_conn |
| crafting_multiplier | `1` | g_craftingSpeedMultiplier |
| death_messages | `false` | sv_msg_death |
| disable_ai | `false` | asm_disable |
| enable_rcon | `true` | N/A |
| enable_upnp | `false` | N/A |
| enable_whitelist | `false` | N/A |
| force_pattern | `-1` | wm_pattern |
| force_time | `-1` | wm_forceTime |
| grant_guides | `false` | N/A |
| health_regen_rate | `0.111` | g_playerHealthRegen |
| horde_cooldown | `900` | asm_hordeCooldown |
| hunger_rate | `0.2777` | g_playerFoodDecay |
| hunger_rate_while_running | `0.34722` | g_playerFoodDecaySprinting |
| idle_kick_seconds | `300` | g_idleKickTime |
| infinite_stamina | `0` | g_playerInfiniteStamina |
| loot_concurrent_item_spawned | `750` | ism_maxCount |
| loot_spawner_percent | `20` | ism_percent |
| map | `islands` | N/A |
| max_corpse_time | `1200` | pcs_maxCorpseTime |
| max_player_corpses | `20` | pcs_maxCorpses |
| max_players | `36` | N/A |
| max_uptime | `12` | max_uptime |
| mod_ids | `(empty list)` | steam_ugc |
| no_bans | `false` | sv_noBannedAccounts |
| ping_limit | `0` | g_pinglimit |
| ping_limit_grace_timer | `60` | g_pingLimitGraceTimer |
| ping_limit_timer | `60` | g_pingLimitTimer |
| player_health_multiplier | `1` | g_maxHealthMultiplier |
| player_weight_limit | `40` | g_playerWeightLimit |
| port | `64090` | N/A |
| rcon_password | `(randomized)` | http_password |
| reset_base_clan_ids | `(empty list)` | N/A |
| reset_base_owner_ids | `(empty list)` | N/A |
| reset_bases | `false` | N/A |
| reset_tent_clan_ids | `(empty list)` | N/A |
| reset_tent_owner_ids | `(empty list)` | N/A |
| reset_tents | `false` | N/A |
| reset_vehicle_clan_ids | `(empty list)` | N/A |
| reset_vehicle_owner_ids | `(empty list)` | N/A |
| reset_vehicles | `false` | N/A |
| respawn_at_base_timeout | `30` | g_respawnAtBaseTime |
| server_id | `100` or first value in db | N/A |
| server_name | `Miscreated Self-hosted Server #(random#)` | sv_servername |
| sv_motd | `false` | sv_motd |
| sv_url | `false` | sv_url |
| temperature_speed | `1.0` | g_playerTemperatureSpeed |
| tempertature_environment_speed | `0.0005` | g_playerTemperatureEnvRate |
| theros_admin_ids | `(empty list)` | N/A |
| thirst_rate | `0.4861` | g_playerWaterDecay |
| thirst_rate_while_running | `0.607638` | g_playerWaterDecaySprinting |
| time_day_minutes | `390` | wm_timeScale |
| time_night_minutes | `82.5` | wm_timeScaleNight |
| time_offset | `-1` | wm_timeOffset |

Note: the `enable_upnp` setting currently has no effect. Server ports must be manually forwarded through your firewall. The first four ports should be forwarded as UDP, the fifth port (RCON) as TCP. If you use the default base port of `64090`, the UDP ports to be forwarded are `64090`-`64093`, and the TCP port is `64094`.

### Special files
Any files *starting* with these filenames which are placed in the script directory to invoke special script behavior, just create an empty file with the desired name to trigger the action:
* `debug` - Enable verbose logging. Logging is also written to `smss.log`.
* `skip` - Skips validating the Miscreated server files - don't do this until *after* the script has been run at least once resulting in the server launching as expected.
* `stop` - If this file exists the Miscreated server will not restart upon termination.

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
    "reset_base_clan_ids": [256512],
    "reset_tent_owner_ids": [76561198027894420, 76561198822937906],
    "reset_vehicle_owner_ids": [76561198027894420, 76561198822937906]
}
```
## Theros' Admin Mod
To make it easy to get started with *admin powers* on a server, in [smss.json](smss.example.json) you can specify a list of SteamID64 accounts to act as admins and this will enable [Theros' admin mod](https://steamcommunity.com/sharedfiles/filedetails/?id=2011185435):
```json
{
    "theros_admin_ids": [76561198027894420, 76561198822937906]
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
    "reset_tent_owner_ids": [76561198027894420, 76561198822937906],
    "server_name": "My Miscreated server",
    "theros_admin_ids": [76561198027894420, 76561198822937906]
}
```
The above example sets:
* the base port of the game server - the RCON port is always that value + 4)
* the RCON password
* resets the despawn timer for all bases
* resets tents at bases belonging to the two specified SteamID64 accounts
* sets the server name to *My Miscreated server*
* and adds two SteamID64 accounts as admins - this enables the admin mod and updates the configuration file 