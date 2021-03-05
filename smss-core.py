from bs4 import BeautifulSoup 
from colorama import init
from datetime import date, datetime
from pathlib import Path
from pprint import pprint, pformat
from random import randint
from urllib import request
import asyncio
import copy
import fileinput
import json
import logging
import math
import os
import requests 
import shutil
import sqlite3
import sys
import zipfile

sys.path.insert(0, '')
init()

class SmssConfig:
    """
    FIXME: Class description here
    """

    def __init__(self, **kwargs):
        logging.debug("Initializing MiscreatedRCON object")

        self.as_corpseCountMax = int(kwargs.get('ai_corpses_max', 20))
        self.as_corpseRemovalTime = int(kwargs.get('ai_corpses_removal', 300))
        self.asm_disable = int(bool(kwargs.get('disable_ai', 0)))
        self.asm_hordeCooldown = int(kwargs.get('horde_cooldown', 900))
        self.asm_maxMultiplier = float(kwargs.get('asm_maxMultiplier', 1))
        self.asm_percent = int(kwargs.get('asm_percent', 60))
        self.bind_ip = kwargs.get('bind_ip', '0.0.0.0')
        self.enable_rcon = bool(kwargs.get('enable_rcon', True))
        self.enable_upnp = bool(kwargs.get('enable_upnp', False))
        self.enable_whitelist = bool(kwargs.get('enable_whitelist', False))
        self.g_craftingSpeedMultiplier = float(kwargs.get('crafting_multiplier', 1))
        self.g_gameRules_Camera = int(kwargs.get('camera', 0))
        self.g_gameRules_bases = int(kwargs.get('base_rules', 1))
        self.g_idleKickTime = int(kwargs.get('idle_kick_seconds', 300))
        self.g_maxHealthMultiplier = float(kwargs.get('player_health_multiplier', 1))
        self.g_pingLimitGraceTimer = int(kwargs.get('ping_limit_grace_timer', 60))
        self.g_pingLimitTimer = int(kwargs.get('ping_limit_timer', 60))
        self.g_pinglimit = int(kwargs.get('ping_limit', 0))
        self.g_playerFoodDecay = float(kwargs.get('hunger_rate', 0.2777))
        self.g_playerFoodDecaySprinting = float(kwargs.get('hunger_rate_while_running', 0.34722))
        self.g_playerHealthRegen = float(kwargs.get('health_regen_rate', 0.111))
        self.g_playerInfiniteStamina = int(bool(kwargs.get('infinite_stamina', 0)))
        self.g_playerTemperatureEnvRate = float(kwargs.get('tempertature_environment_speed', 0.0005))
        self.g_playerTemperatureSpeed = float(kwargs.get('temperature_speed', 1.0))
        self.g_playerWaterDecay = float(kwargs.get('thirst_rate', 0.4861))
        self.g_playerWaterDecaySprinting = float(kwargs.get('thirst_rate_while_running', 0.607638))
        self.g_playerWeightLimit = int(kwargs.get('player_weight_limit', 40))
        self.g_respawnAtBaseTime = int(kwargs.get('respawn_at_base_timeout', 30))
        self.grant_guides = bool(kwargs.get('grant_guides', False))
        self.http_password = str(kwargs.get('rcon_password', 'secret{}'.format(str(randint(0, 99999)).rjust(5, "0"))))
        self.ism_maxCount = int(kwargs.get('loot_concurrent_item_spawned', 750))
        self.ism_percent = float(kwargs.get('loot_spawner_percent', 20))
        self.max_players = int(kwargs.get('max_players', 36))
        self.max_uptime = float(kwargs.get('max_uptime', 12))
        self.miscreated_map = str(kwargs.get('map', 'islands'))
        self.mod_ids = kwargs.get('mod_ids', False)
        self.pcs_maxCorpseTime = int(kwargs.get('max_corpse_time', 1200))
        self.pcs_maxCorpses = int(kwargs.get('max_player_corpses', 20))
        self.port = int(kwargs.get('port', 64090))
        self.reset_base_despawn_clan_ids = kwargs.get('reset_base_despawn_clan_ids', list())
        self.reset_base_despawn_ids = kwargs.get('reset_base_despawn_ids', list())
        self.reset_bases = kwargs.get('reset_bases', False)
        self.reset_tent_despawn_clan_ids = kwargs.get('reset_tent_despawn_clan_ids', list())
        self.reset_tent_despawn_ids = kwargs.get('reset_tent_despawn_ids', list())
        self.reset_tents = kwargs.get('reset_tents', False)
        self.reset_vehicle_despawn_clan_ids = kwargs.get('reset_vehicle_despawn_clan_ids', list())
        self.reset_vehicle_despawn_ids = kwargs.get('reset_vehicle_despawn_ids', list())
        self.reset_vehicles = kwargs.get('reset_vehicles', False)
        self.server_id = int(kwargs.get('server_id', False))
        self.sv_motd = kwargs.get('motd_a', False)
        self.sv_msg_conn = int(bool(kwargs.get('connection_messages', 0)))
        self.sv_msg_death = int(bool(kwargs.get('death_messages', 0)))
        self.sv_noBannedAccounts = int(bool(kwargs.get('no_bans', 0)))
        self.sv_servername = str(kwargs.get('server_name', 'Miscreated Self-hosted Server #{}'.format(str(randint(0, 999999)).rjust(6, "0"))))
        self.sv_url = kwargs.get('motd_b', False)
        self.theros_admin_mod = bool(kwargs.get('theros_admin_mod', False))
        self.theros_admin_mod_admin_ids = kwargs.get('theros_admin_mod_admins', False)
        self.time_day_minutes = float(kwargs.get('time_day_minutes', 390))
        self.time_night_minutes = float(kwargs.get('time_night_minutes', 82.5))
        self.wm_forceTime = kwargs.get('force_time', -1)
        self.wm_pattern = int(kwargs.get('force_pattern', -1))
        self.wm_timeOffset = kwargs.get('time_offset', -1)
        self.wm_timeScale = float(self.get_timeScale())
        self.wm_timeScaleNight = float(self.get_timeScaleNight())
        self.steam_ugc = self.condense_mods()

        self.script_path = os.path.dirname(os.path.realpath(__file__))

        self.miscreated_server_path = Path("{}/MiscreatedServer".format(self.script_path))
        self.miscreated_server_cmd = Path("{}/Bin64_dedicated/MiscreatedServer.exe".format(self.miscreated_server_path))
        self.miscreated_server_db = Path("{}/miscreated.db".format(self.miscreated_server_path))
        self.miscreated_server_config = Path("{}/hosting.cfg".format(self.miscreated_server_path))
        self.miscreated_server_admin_path = Path("{}/SvServerAdmin".format(self.miscreated_server_path))
        self.miscreated_server_admin_config = Path("{}/settings.cfg".format(self.miscreated_server_admin_path))

        self.steamcmd_path = Path("{}/SteamCMD".format(self.script_path))
        self.steamcmd = Path("{}/steamcmd.exe".format(self.steamcmd_path))

        self.temp_path = Path("{}/temp".format(self.script_path))

        if not self.server_id:
           self.server_id = self.get_server_id_from_db()

        logging.debug(vars(self))

        self.miscreated_server_admin_path.mkdir(parents=True, exist_ok=True)
        self.miscreated_server_path.mkdir(parents=True, exist_ok=True)
        self.steamcmd_path.mkdir(parents=True, exist_ok=True)
        self.temp_path.mkdir(parents=True, exist_ok=True)

    def condense_mods(self):
        if self.theros_admin_mod and not isinstance(self.mod_ids, list):
            self.mod_ids = list()
        self.mod_ids.append(2011185435)

        unique_mods = list()
        for mod_id in self.mod_ids:
            if mod_id not in unique_mods:
                unique_mods.append(mod_id)
        if unique_mods:
            return ','.join(str(m) for m in unique_mods)
        return ''

    def get_server_id_from_db(self):
        if not os.path.exists(self.miscreated_server_db):
            logging.debug('Database not yet created')
            logging.debug('Using default database ID')
            return 100
        logging.debug('Retrieving first server ID found in the database')
        query = 'SELECT GameServerID FROM Characters ORDER BY CharacterID LIMIT 1'
        try:
            conn = sqlite3.connect(self.miscreated_server_db)
            cur = conn.cursor()
            cur.execute(query)
            record = cur.fetchone()
            result = record[0]
        except Exception as e:
            logging.debug('Error retrieving first server ID found in the database')
            logging.debug(e)
            logging.debug('Falling back to default server ID')
            result = 100
        return result

    def get_timeScale(self):
        return round(780/self.time_day_minutes, 2)

    def get_timeScaleNight(self):
        return round(660/(self.get_timeScale()*self.time_night_minutes), 2)


async def run(cmd):
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)

    stdout, stderr = await proc.communicate()

    logging.debug(f'[{cmd!r} exited with {proc.returncode}]')
    if stdout:
        logging.debug(f'[stdout]\n{stdout.decode()}')
    if stderr:
        logging.debug(f'[stderr]\n{stderr.decode()}')

def calc_distance(x1, y1, x2, y2):
    dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return dist

def get_bases_sql():
    sql = """
        SELECT (AccountID + 76561197960265728) AS Owner,
            ROUND(PosX,5) AS PosX,
            ROUND(PosY,5) AS PosY
        FROM Structures
        WHERE ClassName='PlotSign'
        """
    return sql

def get_tents_sql():
    sql = """
        SELECT StructureID,
            ROUND(PosX,5) AS PosX,
            ROUND(PosY,5) AS PosY
        FROM Structures
        WHERE ClassName like '%tent%'
        """
    return sql

def get_vehicles_sql():
    sql = """
        SELECT VehicleID,
            ROUND(PosX,5) AS PosX,
            ROUND(PosY,5) AS PosY
        FROM Vehicles
        """
    return sql

def get_result_set(db, sql):
    if not os.path.exists(db):
        logging.debug('Database not yet created')
        return False

    conn = sqlite3.connect(db)
    c = conn.cursor()
    try:
        results = c.execute(sql)
    except sqlite3.Error as e:
        print(e)
        return None
    result_set = list()
    for result in results.fetchall():
        result_set.append(result)

    return result_set

def get_mod_name(mod_id):
    url="https://steamcommunity.com/sharedfiles/filedetails/?id={}".format(mod_id)
    try:
        reqs = requests.get(url)
        soup = BeautifulSoup(reqs.text, 'html.parser')
        title = soup.find('title').get_text()
    except Exception as e:
        return mod_id
    if title.find("Steam Workshop::") >= 0:
        title = title.replace("Steam Workshop::",mod_id + ": ")
    else:
        title = mod_id
    return title

def get_mod_titles(smss):
    if not len(smss.steam_ugc):
        return "<none>"

    mod_ids=smss.steam_ugc.split(',')
    first = True
    mod_list = ''
    for mod in mod_ids:
        this_line = ''
        if not first:
            this_line = '\n               '
        mod_list = mod_list + this_line + get_mod_name(mod)
        first=False
    return mod_list

def configure_admin_mod(smss):
    if not smss.theros_admin_mod or not smss.theros_admin_mod_admin_ids:
        return
    
    ServerOwner=','.join(str(t) for t in smss.theros_admin_mod_admin_ids)
    ServerOwner='"{}"'.format(ServerOwner)
    
    update_cfg(smss.miscreated_server_admin_config, 'ServerOwner', ServerOwner)

def get_steam(smss):
    logging.debug('method: get_steam')
    if os.path.exists(smss.steamcmd):
        logging.debug("{} exists. Skipping download.".format(smss.steamcmd))
        return

    logging.info("{} does not exist".format(smss.steamcmd))
    steamcmd_url = 'https://steamcdn-a.akamaihd.net/client/installer/steamcmd.zip'
    steamcmd_zip_file = Path("{}/steamcmd.zip".format(smss.temp_path))

    try:
        logging.info("Attempting SteamCMD download")
        request.urlretrieve(steamcmd_url, steamcmd_zip_file)
    except Exception as e:
        logging.debug(e)

    try:
        logging.info("Extracting {} archive".format(steamcmd_zip_file))
        with zipfile.ZipFile(steamcmd_zip_file, 'r') as zip_ref:
            zip_ref.extractall(smss.steamcmd_path)
    except Exception as e:
        logging.debug(e)

def grant_guides(smss):
    if not smss.grant_guides:
        return

    logging.debug('Granting guides to all players')

    query = """
    DROP TRIGGER IF EXISTS grant_all_guides;
    CREATE TRIGGER IF NOT EXISTS grant_all_guides AFTER UPDATE ON Characters BEGIN UPDATE ServerAccountData SET Guide00="-1", Guide01="-1"; END; UPDATE ServerAccountData SET Guide00="-1", Guide01="-1";
    """
    try:
        conn = sqlite3.connect(smss.miscreated_server_db)
        conn.executescript(query)
    except Exception as e:
        logging.debug(e)

def base_timer_reset(smss):
    if not len(smss.reset_base_despawn_ids):
        return

    logging.debug("Extending base despawn timers")
    if not os.path.exists(smss.miscreated_server_db):
        logging.debug('Database not yet created')
        return

    update_ids = list()

    for steam_id in smss.reset_base_despawn_ids:
        this_id = steam_id - 76561197960265728
        update_ids.append(this_id)

    update_ids = ', '.join(str(t) for t in update_ids)

    query = """
    Update Structures SET AbandonTimer=2419200 WHERE AccountID IN ({});
    """.format(update_ids)

    logging.debug(query)

    try:
        conn = sqlite3.connect(smss.miscreated_server_db)
        conn.execute(query)
    except Exception as e:
        logging.debug(e)

def launch_miscreated_server(smss):
    logging.debug('method: launch_miscreated_server')

    semaphore_file = Path(str(smss.miscreated_server_path) + '/smss.managed')

    f = open(semaphore_file, "w")
    f.write("This server is managed by Spafbi's Simplified Miscreated Server Setup script.")
    f.close()

    server_options = list()

    if smss.bind_ip:
        server_options.append('-sv_bind {}'.format(smss.bind_ip))

    if smss.enable_whitelist:
        server_options.append('-mis_whitelist')
    
    if smss.enable_rcon:
        server_options.append('+http_startserver')

    server_options.append('-sv_port {}'.format(smss.port))
    server_options.append('-mis_gameserverid {}'.format(smss.server_id))
    server_options.append('+sv_maxplayers {}'.format(smss.max_players))
    server_options.append('+map {}'.format(smss.miscreated_map))
    server_options.append('+sv_servername "{}"'.format(smss.sv_servername))

    server_options = ' '.join(str(e) for e in server_options)

    server_cmd = '"{}"'.format(smss.miscreated_server_cmd) + ' ' + server_options
#║╔╗╚╝─═╟╢
    cvars=get_cvars(smss)
    timestamp = str(date.today()) + ', ' + str(datetime.now().strftime("%I:%M %p"))
    print("""
══════════════════════════════════════════════════════════════════════════════
                              hosting.cfg cvars
══════════════════════════════════════════════════════════════════════════════
{cvars}
══════════════════════════════════════════════════════════════════════════════
══════════════════════════════════════════════════════════════════════════════
  [1m[36mServer Name: [1m[33m{sv_servername}[0m
          [1m[36mMap: [1m[33m{map}[0m
         [1m[36mMods: [1m[33m{mods}[0m
    [1m[36mGame Port: [1m[33m{port}[0m
    [1m[36mRCON Port: [1m[33m{rcon}[0m
══════════════════════════════════════════════════════════════════════════════

Launching Miscreated server process ({timestamp})...
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║                          [1m[31mDO NOT CLOSE THIS WINDOW[0m                          ║
║                                                                            ║
╟────────────────────────────────────────────────────────────────────────────╢
║                                                                            ║    
║  This window maintains the Miscreated server. If this window is closed     ║
║  the server will not automatically restart.                                ║
║                                                                            |
╚════════════════════════════════════════════════════════════════════════════╝
""".format(cvars=cvars,
           date=date.today(),
           map=smss.miscreated_map,
           mods=get_mod_titles(smss),
           port=smss.port,
           rcon=smss.port+4,
           sv_servername=smss.sv_servername,
           timestamp=timestamp))
    logging.debug(server_cmd)
    logging.debug('Server started: ' + timestamp)
    asyncio.run(run(server_cmd))
    timestamp = str(date.today()) + ', ' + str(datetime.now().strftime("%I:%M %p"))
    logging.debug('Server closed: ' + timestamp)

def object_timer_reset_for_clans(smss):
    override_ids_sql = """SELECT (AccountID + 76561197960265728) AS SteamID
                               FROM ClanMembers WHERE ClanID IN ({})"""
    if smss.reset_base_despawn_clan_ids:
        override_base_ids_sql = copy.deepcopy(override_ids_sql)
        override_base_ids_sql = override_base_ids_sql.format(', '.join(str(t) for t in smss.reset_base_despawn_clan_ids))
        result = get_result_set(smss.miscreated_server_db, override_base_ids_sql)
        for steam_id in result:
            smss.reset_base_despawn_ids.append(steam_id[0])

    if smss.reset_tent_despawn_clan_ids:
        override_tent_ids_sql = copy.deepcopy(override_ids_sql)
        override_tent_ids_sql = override_tent_ids_sql.format(', '.join(str(t) for t in smss.reset_tent_despawn_clan_ids))
        result = get_result_set(smss.miscreated_server_db, override_tent_ids_sql)
        for steam_id in result:
            smss.reset_tent_despawn_ids.append(steam_id[0])

    if smss.reset_vehicle_despawn_clan_ids:
        override_vehicle_ids_sql = copy.deepcopy(override_ids_sql)
        override_vehicle_ids_sql = override_vehicle_ids_sql.format(', '.join(str(t) for t in smss.reset_vehicle_despawn_clan_ids))
        result = get_result_set(smss.miscreated_server_db, override_vehicle_ids_sql)
        for steam_id in result:
            smss.reset_vehicle_despawn_ids.append(steam_id[0])

def object_timer_reset(smss):
    if smss.reset_bases:
        sql = "UPDATE Structures SET AbandonTimer=2419200 WHERE ClassName='PlotSign';"
        get_result_set(smss.miscreated_server_db, sql)
    if smss.reset_tents:
        sql = "UPDATE Structures SET AbandonTimer=2419200 WHERE ClassName like '%tent%';"
        get_result_set(smss.miscreated_server_db, sql)
    if smss.reset_vehicles:
        sql = "UPDATE Vehicles SET AbandonTimer=2419200;"
        get_result_set(smss.miscreated_server_db, sql)
    if not len(smss.reset_vehicle_despawn_ids) and not len(smss.reset_tent_despawn_ids):
        return
    bases = get_result_set(smss.miscreated_server_db, get_bases_sql())
    if not bases:
        return
    tents = get_result_set(smss.miscreated_server_db, get_tents_sql())
    vehicles = get_result_set(smss.miscreated_server_db, get_vehicles_sql())
    reset_vehicles = list()
    reset_tents = list()

    for base in bases:
        steam_id = base[0]
        x1 = base[1]
        y1 = base[2]
        if vehicles:
            for vehicle in vehicles:
                if steam_id not in smss.reset_vehicle_despawn_ids:
                    continue
                x2 = vehicle[1]
                y2 = vehicle[2]
                if calc_distance(x1, y1, x2, y2) <= 30:
                    reset_vehicles.append(vehicle[0])
        if tents:
            for tent in tents:
                if steam_id not in smss.reset_tent_despawn_ids:
                    continue
                x2 = tent[1]
                y2 = tent[2]
                if calc_distance(x1, y1, x2, y2) <= 30:
                    reset_tents.append(tent[0])

    tents_sql = """
    UPDATE Structures
        SET AbandonTimer=2419200
        WHERE StructureID IN ({});
    """.format(', '.join(str(t) for t in reset_tents))

    vehicles_sql = """
    UPDATE Vehicles
        SET AbandonTimer=2419200
        WHERE VehicleID IN ({});
    """.format(', '.join(str(v) for v in reset_vehicles))

    if tents:
        logging.debug(tents_sql)
        get_result_set(smss.miscreated_server_db, tents_sql)
    if vehicles:
        logging.debug(vehicles_sql)
        get_result_set(smss.miscreated_server_db, vehicles_sql)

def get_cvars(smss):
    hosting_cfg_cvars = {
        'ai': {
            'asm_disable': smss.asm_disable,
            'asm_hordeCooldown': smss.asm_hordeCooldown,
            'asm_maxMultiplier': smss.asm_maxMultiplier,
            'asm_percent': smss.asm_percent
        },
        'corpses': {
            'as_corpseCountMax': smss.as_corpseCountMax,
            'as_corpseRemovalTime': smss.as_corpseRemovalTime,
            'pcs_maxCorpseTime': smss.pcs_maxCorpseTime,
            'pcs_maxCorpses': smss.pcs_maxCorpses
        },
        'loot': {
            'ism_maxCount': smss.ism_maxCount,
            'ism_percent': smss.ism_percent
        },
        'players': {
            'g_craftingSpeedMultiplier': smss.g_craftingSpeedMultiplier,
            'g_gameRules_Camera': smss.g_gameRules_Camera,
            'g_gameRules_bases': smss.g_gameRules_bases,
            'g_idleKickTime': smss.g_idleKickTime,
            'g_maxHealthMultiplier': smss.g_maxHealthMultiplier,
            'g_pingLimitGraceTimer': smss.g_pingLimitGraceTimer,
            'g_pingLimitTimer': smss.g_pingLimitTimer,
            'g_pinglimit': smss.g_pinglimit,
            'g_playerFoodDecay': smss.g_playerFoodDecay,
            'g_playerFoodDecaySprinting': smss.g_playerFoodDecaySprinting,
            'g_playerHealthRegen': smss.g_playerHealthRegen,
            'g_playerInfiniteStamina': smss.g_playerInfiniteStamina,
            'g_playerTemperatureEnvRate': smss.g_playerTemperatureEnvRate,
            'g_playerTemperatureSpeed': smss.g_playerTemperatureSpeed,
            'g_playerWaterDecay': smss.g_playerWaterDecay,
            'g_playerWaterDecaySprinting': smss.g_playerWaterDecaySprinting,
            'g_respawnAtBaseTime': smss.g_respawnAtBaseTime
        },
        'server': {
            'http_password': '*'*len(smss.http_password),
            'max_uptime': smss.max_uptime,
            'sv_msg_conn': smss.sv_msg_conn,
            'sv_msg_death': smss.sv_msg_death,
            'sv_noBannedAccounts': smss.sv_noBannedAccounts,
            'sv_servername': smss.sv_servername
        },
        'time and weather': {
            'wm_forceTime': smss.wm_forceTime,
            'wm_pattern': smss.wm_pattern,
            'wm_timeOffset': smss.wm_timeOffset,
            'wm_timeScale': smss.wm_timeScale,
            'wm_timeScaleNight': smss.wm_timeScaleNight
        }
    }
    if len(smss.steam_ugc):
        hosting_cfg_cvars['server']['steam_ugc'] = smss.steam_ugc
    if smss.sv_motd:
        hosting_cfg_cvars['server']['sv_motd'] = smss.sv_motd
    if smss.sv_url:
        hosting_cfg_cvars['server']['sv_url'] = smss.sv_url
    return pformat(hosting_cfg_cvars, indent=2)

def remove_mods(smss):
    mods_dir = Path('{}/Mods'.format(smss.miscreated_server_path))
    if os.path.exists(mods_dir):
        logging.debug('Removing mods directory to refresh mods')
        try:
            shutil.rmtree(mods_dir, ignore_errors=True)
        except OSError as e:
            logging.debug("Error: {} : {}".format(mods_dir, e.strerror))

def stop_server(smss):
    stop_file = Path('{}/stop'.format(smss.script_path))
    stop_txt_file = Path('{}/stop.txt'.format(smss.script_path))
    if os.path.exists(stop_file) or os.path.exists(stop_txt_file):
        logging.info('stop file exist - remove the stop file to allow the server to restart automatically')
        return True
    logging.info('stop file does not exist - server should restart automatically at this time')
    return False

def update_cfg(filename, cvar, cvar_value):
    replaced = False
    mode = 'a+'

    if os.path.exists(filename):
        for line in fileinput.input([filename], inplace=True):
            if line.strip().startswith('{}='.format(cvar)):
                line = '{}={}\n'.format(cvar, cvar_value)
                replaced = True
            sys.stdout.write(line)
    else:
        mode = 'w+'

    if not replaced:
        file = open(filename, mode)
        file.write('{}={}\n'.format(cvar, cvar_value))
        file.close

def validate_miscreated_server(smss):
    logging.debug('method: validate_miscreated_server')
    stop_file = Path('{}/skip'.format(smss.script_path))
    stop_txt_file = Path('{}/skip.txt'.format(smss.script_path))
    if os.path.exists(stop_file) or os.path.exists(stop_txt_file):
        logging.info('skip file exist - remove the skip file to allow the server to validate the server automatically')
        return True
    install_cmd = 'steam_cmd +login anonymous +force_install_dir miscreated_server_path '\
                  '+app_update 302200 validate +quit'
    install_cmd_string = copy.deepcopy(install_cmd)

    steamcmd = '{}'.format(smss.steamcmd)
    miscreated_server_path = '{}'.format(smss.miscreated_server_path)
    install_cmd_string = install_cmd_string.replace('steam_cmd',steamcmd)
    install_cmd_string = install_cmd_string.replace('miscreated_server_path',miscreated_server_path)
    
    logging.info('Validating Miscreated Server installation. This could take a while...')
    asyncio.run(run(install_cmd_string))

    logging.info('Miscreated Server installation validated')

def main():
    """
    Summary: Default method if this modules is run as __main__.
    """
    import argparse

    # Just grabbing this script's filename
    prog = os.path.basename(__file__)
    description = """{prog} sets up and runs a Miscreated game server""".format(prog=prog)

    # Set up argparse to help people use this as a CLI utility
    parser = argparse.ArgumentParser(prog=prog, description=description)

    parser.add_argument('-c', '--config', type=str, required=False,
                        help="""JSON configuration file""", default="smss.json")
    parser.add_argument('-f', '--force', action='store_true', required=False,
                        help="""Force configuration prompts - this should be used if you wish to change previously selected options""")

    script_path = os.path.dirname(sys.argv[0])
    script_path = os.path.abspath(script_path)

    if script_path.find(' ') >= 0:
        print('This script cannot be run in paths having spaces. Current path:')
        print('   {}'.format(script_path) + "\n")
        return

    debug_file = str(Path('{}/debug'.format(script_path)))
    debug_txt_file = str(Path('{}/debug.txt'.format(script_path)))
    verbose = False
    if ((os.path.exists(debug_file)) or (os.path.exists(debug_txt_file))):
        verbose = True

    # Parse our arguments!
    args = parser.parse_args()

    if verbose:
        smss_logger = logging.getLogger()
        smss_logger.setLevel(logging.DEBUG)

        output_file_handler = logging.FileHandler("smss.log")
        stdout_handler = logging.StreamHandler(sys.stdout)

        smss_logger.addHandler(output_file_handler)
        smss_logger.addHandler(stdout_handler)
    else:
        logging.basicConfig(level=logging.INFO)

    logging.debug(args)

    # FIXME - If configuration is forced, run configurator to create the JSON file

    run_server = True
    while run_server:
        try:
            with open(args.config) as f:
                json_config = json.load(f)
        except Exception as e:
            logging.debug(e)
            logging.debug("Configuration file load error. Using default configuration")
            json_config={}

        logging.debug(json_config)

        smss = SmssConfig(**json_config)

        update_cfg(smss.miscreated_server_config, 'as_corpseCountMax', smss.as_corpseCountMax)
        update_cfg(smss.miscreated_server_config, 'as_corpseRemovalTime', smss.as_corpseRemovalTime)
        update_cfg(smss.miscreated_server_config, 'asm_disable', int(smss.asm_disable))
        update_cfg(smss.miscreated_server_config, 'asm_hordeCooldown', smss.asm_hordeCooldown)
        update_cfg(smss.miscreated_server_config, 'asm_maxMultiplier', smss.asm_maxMultiplier)
        update_cfg(smss.miscreated_server_config, 'asm_percent', smss.asm_percent)
        update_cfg(smss.miscreated_server_config, 'g_craftingSpeedMultiplier', smss.g_craftingSpeedMultiplier)
        update_cfg(smss.miscreated_server_config, 'g_gameRules_Camera', smss.g_gameRules_Camera)
        update_cfg(smss.miscreated_server_config, 'g_gameRules_bases', smss.g_gameRules_bases)
        update_cfg(smss.miscreated_server_config, 'g_idleKickTime', smss.g_idleKickTime)
        update_cfg(smss.miscreated_server_config, 'g_maxHealthMultiplier', smss.g_maxHealthMultiplier)
        update_cfg(smss.miscreated_server_config, 'g_pingLimitGraceTimer', smss.g_pingLimitGraceTimer)
        update_cfg(smss.miscreated_server_config, 'g_pingLimitTimer', smss.g_pingLimitTimer)
        update_cfg(smss.miscreated_server_config, 'g_pinglimit', smss.g_pinglimit)
        update_cfg(smss.miscreated_server_config, 'g_playerFoodDecay', smss.g_playerFoodDecay)
        update_cfg(smss.miscreated_server_config, 'g_playerFoodDecaySprinting', smss.g_playerFoodDecaySprinting)
        update_cfg(smss.miscreated_server_config, 'g_playerHealthRegen', smss.g_playerHealthRegen)
        update_cfg(smss.miscreated_server_config, 'g_playerInfiniteStamina', smss.g_playerInfiniteStamina)
        update_cfg(smss.miscreated_server_config, 'g_playerTemperatureEnvRate', smss.g_playerTemperatureEnvRate)
        update_cfg(smss.miscreated_server_config, 'g_playerTemperatureSpeed', smss.g_playerTemperatureSpeed)
        update_cfg(smss.miscreated_server_config, 'g_playerWaterDecay', smss.g_playerWaterDecay)
        update_cfg(smss.miscreated_server_config, 'g_playerWaterDecaySprinting', smss.g_playerWaterDecaySprinting)
        update_cfg(smss.miscreated_server_config, 'g_playerWeightLimit', smss.g_playerWeightLimit)
        update_cfg(smss.miscreated_server_config, 'g_respawnAtBaseTime', smss.g_respawnAtBaseTime)
        update_cfg(smss.miscreated_server_config, 'http_password', smss.http_password)
        update_cfg(smss.miscreated_server_config, 'ism_maxCount', smss.ism_maxCount)
        update_cfg(smss.miscreated_server_config, 'ism_percent', smss.ism_percent)
        update_cfg(smss.miscreated_server_config, 'max_uptime', smss.max_uptime)
        update_cfg(smss.miscreated_server_config, 'pcs_maxCorpseTime', smss.pcs_maxCorpseTime)
        update_cfg(smss.miscreated_server_config, 'pcs_maxCorpses', smss.pcs_maxCorpses)
        update_cfg(smss.miscreated_server_config, 'sv_msg_conn', smss.sv_msg_conn)
        update_cfg(smss.miscreated_server_config, 'sv_msg_death', smss.sv_msg_death)
        update_cfg(smss.miscreated_server_config, 'sv_noBannedAccounts', smss.sv_noBannedAccounts)
        update_cfg(smss.miscreated_server_config, 'sv_servername', smss.sv_servername)
        update_cfg(smss.miscreated_server_config, 'wm_forceTime', smss.wm_forceTime)
        update_cfg(smss.miscreated_server_config, 'wm_pattern', smss.wm_pattern)
        update_cfg(smss.miscreated_server_config, 'wm_timeOffset', smss.wm_timeOffset)
        update_cfg(smss.miscreated_server_config, 'wm_timeScale', smss.wm_timeScale)
        update_cfg(smss.miscreated_server_config, 'wm_timeScaleNight', smss.wm_timeScaleNight)

        configure_admin_mod(smss)
    
        if len(smss.steam_ugc):
            update_cfg(smss.miscreated_server_config, 'steam_ugc', smss.steam_ugc)
        if smss.sv_motd:
            update_cfg(smss.miscreated_server_config, 'sv_motd', smss.sv_motd)
        if smss.sv_url:
            update_cfg(smss.miscreated_server_config, 'sv_url', smss.sv_url)

        remove_mods(smss)
        get_steam(smss)
        validate_miscreated_server(smss)
        if os.path.exists(smss.miscreated_server_db):
            grant_guides(smss)
            object_timer_reset_for_clans(smss)
            object_timer_reset(smss)
            base_timer_reset(smss)
        launch_miscreated_server(smss)

        run_server = not stop_server(smss)

if __name__ == '__main__':
    main()