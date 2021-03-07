from bs4 import BeautifulSoup 
from colorama import init
from datetime import date, datetime
from glob import glob
from pathlib import Path
from pprint import pprint, pformat
from random import randint
import asyncio
import fileinput
import json
import logging
import math
import os
import requests
import shutil
import sqlite3
import sys

sys.path.insert(0, '')
init()


class SmssConfig:
    """
    The Simplified Miscreated Server Setup class installs and configures a
    Miscreated server. Configuration customization may be carried out through
    the use of a smss.json configuration file.
    """

    def __init__(self, **kwargs):
        logging.debug("Initializing MiscreatedRCON object")

        # These variables may all be passed to this class. Variables not passed will use default values.
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
        self.mod_ids = kwargs.get('mod_ids', list())
        self.pcs_maxCorpseTime = int(kwargs.get('max_corpse_time', 1200))
        self.pcs_maxCorpses = int(kwargs.get('max_player_corpses', 20))
        self.port = int(kwargs.get('port', 64090))
        self.reset_base_clan_ids = kwargs.get('reset_base_clan_ids', list())
        self.reset_base_owner_ids = kwargs.get('reset_base_owner_ids', list())
        self.reset_bases = bool(kwargs.get('reset_bases', False))
        self.reset_tent_clan_ids = kwargs.get('reset_tent_clan_ids', list())
        self.reset_tent_owner_ids = kwargs.get('reset_tent_owner_ids', list())
        self.reset_tents = bool(kwargs.get('reset_tents', False))
        self.reset_vehicle_clan_ids = kwargs.get('reset_vehicle_clan_ids', list())
        self.reset_vehicle_owner_ids = kwargs.get('reset_vehicle_owner_ids', list())
        self.reset_vehicles = bool(kwargs.get('reset_vehicles', False))
        self.server_id = int(kwargs.get('server_id', 0))
        self.sv_motd = str(kwargs.get('sv_motd', ''))
        self.sv_msg_conn = int(bool(kwargs.get('connection_messages', 0)))
        self.sv_msg_death = int(bool(kwargs.get('death_messages', 0)))
        self.sv_noBannedAccounts = int(bool(kwargs.get('no_bans', 0)))
        self.sv_servername = str(kwargs.get('server_name', 'Miscreated Self-hosted Server #{}'.format(str(randint(0, 999999)).rjust(6, "0"))))
        self.sv_url = str(kwargs.get('sv_url', ''))
        self.theros_admin_ids = kwargs.get('theros_admin_ids', list())
        self.time_day_minutes = float(kwargs.get('time_day_minutes', 390))
        self.time_night_minutes = float(kwargs.get('time_night_minutes', 82.5))
        self.wm_forceTime = float(kwargs.get('force_time', -1))
        self.wm_pattern = int(kwargs.get('force_pattern', -1))
        self.wm_timeOffset = float(kwargs.get('time_offset', -1))

        # Variables which are derived from passed/default values
        self.wm_timeScale = float(self.get_timeScale())
        self.wm_timeScaleNight = float(self.get_timeScaleNight())
        self.steam_ugc = self.condense_mods()

        # Configure paths variables for required directories
        self.script_path = os.path.dirname(os.path.realpath(__file__))
        self.miscreated_server_path = Path("{}/MiscreatedServer".format(self.script_path))
        self.steamcmd_path = Path("{}/SteamCMD".format(self.script_path))
        self.temp_path = Path("{}/temp".format(self.script_path))

        # Create required paths
        self.miscreated_server_path.mkdir(parents=True, exist_ok=True)
        self.steamcmd_path.mkdir(parents=True, exist_ok=True)
        self.temp_path.mkdir(parents=True, exist_ok=True)

        # Configure filename variables
        self.miscreated_server_cmd = Path("{}/Bin64_dedicated/MiscreatedServer.exe".format(self.miscreated_server_path))
        self.miscreated_server_config = Path("{}/hosting.cfg".format(self.miscreated_server_path))
        self.miscreated_server_db = Path("{}/miscreated.db".format(self.miscreated_server_path))
        self.steamcmd = Path("{}/steamcmd.exe".format(self.steamcmd_path))

        # Set the server id
        if not self.server_id:
           self.server_id = self.get_server_id_from_db()

        # Dump variables for this object if debugging is turned on
        logging.debug(vars(self))


    async def run(self, cmd):
        """Leverage asyncio to execute commands

        Args:
            cmd (string): preformatted commandline command to be executed
        """
        logging.debug('async method: run')
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


    def add_clan_members_for_timer_resets(self):
        """Adds clan members to base, tent, and vehicle exclusion lists
        """
        logging.debug('method: add_clan_members_for_timer_resets')
        if self.reset_base_clan_ids:
            for steam_id in self.get_clan_members(self.reset_base_clan_ids):
                self.reset_base_owner_ids.append(steam_id)

        if self.reset_tent_clan_ids:
            for steam_id in self.get_clan_members(self.reset_tent_clan_ids):
                self.reset_tent_owner_ids.append(steam_id)

        if self.reset_vehicle_clan_ids:
            for steam_id in self.get_clan_members(self.reset_vehicle_clan_ids):
                self.reset_vehicle_owner_ids.append(steam_id)


    def calc_distance(self, x1, y1, x2, y2):
        dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        return dist


    def condense_mods(self):
        """Removes non-unique mod ids and adds Theros' admin mod if the option
           was selected

        Returns:
            string: A comma delimited string for use in hosting.cfg
        """
        logging.debug('method: condense_mods')
        if self.theros_admin_ids:
            self.mod_ids.append(2011185435)

        unique_mods = list()
        for mod_id in self.mod_ids:
            if mod_id not in unique_mods:
                unique_mods.append(mod_id)
        if unique_mods:
            return ','.join(str(m) for m in unique_mods)
        return ''


    def database_tricks(self):
        """Method used to bundle other methods which massage the database
        """
        logging.debug('method: database_tricks')
        # Exit this method if the server dabase does not yet exist:
        if not os.path.exists(self.miscreated_server_db):
            return
        
        self.grant_guides_in_db()
        self.add_clan_members_for_timer_resets()
        self.reset_base_timers()
        self.reset_tent_timers()
        self.reset_vehicle_timers()


    def get_bases_sql(self):
        sql = """
            SELECT (AccountID + 76561197960265728) AS Owner,
                ROUND(PosX,5) AS PosX,
                ROUND(PosY,5) AS PosY
            FROM Structures
            WHERE ClassName='PlotSign'
            """
        return sql


    def get_clan_members(self, clan_ids):
        """Query the database for members of a clan

        Returns:
            list: clan member ids
        """
        logging.debug('method: get_clan_members')
        sql = """SELECT (AccountID + 76561197960265728) AS SteamID
                 FROM ClanMembers WHERE ClanID IN ({})"""
        sql = sql.format(', '.join(str(t) for t in clan_ids))
        result = self.get_result_set(sql)
        member_ids = list()
        for record in result:
            member_ids.append(record[0])
        return member_ids


    def get_cvars(self):
        hosting_cfg_cvars = {
            'ai': {
                'asm_disable': self.asm_disable,
                'asm_hordeCooldown': self.asm_hordeCooldown,
                'asm_maxMultiplier': self.asm_maxMultiplier,
                'asm_percent': self.asm_percent
            },
            'corpses': {
                'as_corpseCountMax': self.as_corpseCountMax,
                'as_corpseRemovalTime': self.as_corpseRemovalTime,
                'pcs_maxCorpseTime': self.pcs_maxCorpseTime,
                'pcs_maxCorpses': self.pcs_maxCorpses
            },
            'loot': {
                'ism_maxCount': self.ism_maxCount,
                'ism_percent': self.ism_percent
            },
            'players': {
                'g_craftingSpeedMultiplier': self.g_craftingSpeedMultiplier,
                'g_gameRules_Camera': self.g_gameRules_Camera,
                'g_gameRules_bases': self.g_gameRules_bases,
                'g_idleKickTime': self.g_idleKickTime,
                'g_maxHealthMultiplier': self.g_maxHealthMultiplier,
                'g_pingLimitGraceTimer': self.g_pingLimitGraceTimer,
                'g_pingLimitTimer': self.g_pingLimitTimer,
                'g_pinglimit': self.g_pinglimit,
                'g_playerFoodDecay': self.g_playerFoodDecay,
                'g_playerFoodDecaySprinting': self.g_playerFoodDecaySprinting,
                'g_playerHealthRegen': self.g_playerHealthRegen,
                'g_playerInfiniteStamina': self.g_playerInfiniteStamina,
                'g_playerTemperatureEnvRate': self.g_playerTemperatureEnvRate,
                'g_playerTemperatureSpeed': self.g_playerTemperatureSpeed,
                'g_playerWaterDecay': self.g_playerWaterDecay,
                'g_playerWaterDecaySprinting': self.g_playerWaterDecaySprinting,
                'g_respawnAtBaseTime': self.g_respawnAtBaseTime
            },
            'server': {
                'http_password': '*'*len(self.http_password),
                'max_uptime': self.max_uptime,
                'sv_msg_conn': self.sv_msg_conn,
                'sv_msg_death': self.sv_msg_death,
                'sv_noBannedAccounts': self.sv_noBannedAccounts,
                'sv_servername': self.sv_servername
            },
            'time and weather': {
                'wm_forceTime': self.wm_forceTime,
                'wm_pattern': self.wm_pattern,
                'wm_timeOffset': self.wm_timeOffset,
                'wm_timeScale': self.wm_timeScale,
                'wm_timeScaleNight': self.wm_timeScaleNight
            }
        }
        if len(self.steam_ugc):
            hosting_cfg_cvars['server']['steam_ugc'] = self.steam_ugc
        if self.sv_motd:
            hosting_cfg_cvars['server']['sv_motd'] = self.sv_motd
        if self.sv_url:
            hosting_cfg_cvars['server']['sv_url'] = self.sv_url
        return pformat(hosting_cfg_cvars, indent=2)


    def get_mod_name(self, mod_id):
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


    def get_mod_titles(self):
        if not len(self.steam_ugc):
            return "<none>"

        mod_ids=self.steam_ugc.split(',')
        first = True
        mod_list = ''
        for mod in mod_ids:
            this_line = ''
            if not first:
                this_line = '\n               '
            mod_list = mod_list + this_line + self.get_mod_name(mod)
            first=False
        return mod_list


    def get_result_set(self, sql):
        if not os.path.exists(self.miscreated_server_db):
            logging.debug('Database not yet created')
            return False

        logging.debug(sql)

        conn = sqlite3.connect(self.miscreated_server_db)
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


    def get_server_id_from_db(self):
        """Attempts to lookup an existing server ID from the Miscreated
           database, returning the first identified server ID or 100.

        Returns:
            int: Server ID of the Miscreated game server
        """
        logging.debug('method: get_server_id_from_db')
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
            logging.debug('Falling back to default server ID of 100')
            result = 100
        return result


    def get_steam(self):
        """Ensures steamcmd.exe is installed
        """
        logging.debug('method: get_steam')
        if os.path.exists(self.steamcmd):
            logging.debug("{} exists. Skipping download.".format(self.steamcmd))
            return

        logging.info("{} does not exist".format(self.steamcmd))
        steamcmd_url = 'https://steamcdn-a.akamaihd.net/client/installer/steamcmd.zip'
        steamcmd_zip_file = Path("{}/steamcmd.zip".format(self.temp_path))

        try:
            logging.info("Attempting SteamCMD download")
            request.urlretrieve(steamcmd_url, steamcmd_zip_file)
        except Exception as e:
            logging.debug(e)

        try:
            logging.info("Extracting {} archive".format(steamcmd_zip_file))
            with zipfile.ZipFile(steamcmd_zip_file, 'r') as zip_ref:
                zip_ref.extractall(self.steamcmd_path)
        except Exception as e:
            logging.debug(e)


    def get_timeScale(self):
        """Calculate the correct wm_timeScale value based on the number of
           minutes set in the configuration.

        Returns:
            float: wm_timeScale multiplier
        """
        logging.debug('method: get_timeScale')
        return round(780/self.time_day_minutes, 2)


    def get_timeScaleNight(self):
        """Calculate the correct wm_timeScaleNight value based on the number of
           minutes set in the configuration.

        Returns:
            float: wm_timeScaleNight multiplier
        """
        logging.debug('method: get_timeScaleNight')
        return round(660/(self.get_timeScale()*self.time_night_minutes), 2)


    def get_start_server_message(self):
        #║╔╗╚╝─═╟╢
        message = '═'*78+'\r\n'+'═'*78+'\r\n'\
                  '  [1m[36mServer Name: [1m[33m{sv_servername}[0m\r\n'\
                  '          [1m[36mMap: [1m[33m{map}[0m\r\n'\
                  '         [1m[36mMods: [1m[33m{mods}[0m\r\n'\
                  '    [1m[36mGame Port: [1m[33m{port}[0m\r\n'\
                  '    [1m[36mRCON Port: [1m[33m{rcon}[0m\r\n'\
                  ''+'═'*78+'\r\n\r\n'\
                  'Launching Miscreated server process ({timestamp})...\r\n'\
                  '╔'+'═'*76+'╗\r\n'\
                  '║'+' '*26+'[1m[31mDO NOT CLOSE THIS WINDOW[0m'+' '*26+'║\r\n'\
                  '║'+' '*76+'║\r\n'\
                  '╟'+'─'*76+'╢\r\n'\
                  '║'+' '*76+'║\r\n'\
                  '║  This window maintains the Miscreated server. If this window is closed     ║\r\n'\
                  '║  the server will not automatically restart.'+' '*32+'║\r\n'\
                  '║'+' '*76+'║\r\n'\
                  '╚'+'═'*76+'╝'
        return message


    def get_tents_sql(self):
        sql = """
            SELECT StructureID,
                ROUND(PosX,5) AS PosX,
                ROUND(PosY,5) AS PosY
            FROM Structures
            WHERE ClassName like '%tent%'
            """
        return sql


    def get_vehicles_sql(self):
        sql = """
            SELECT VehicleID,
                ROUND(PosX,5) AS PosX,
                ROUND(PosY,5) AS PosY
            FROM Vehicles
            """
        return sql


    def grant_guides_in_db(self):
        """Grants all guides to players.
        """
        logging.debug('method: grant_guides_in_db')
        if not self.grant_guides:
            return

        logging.debug('Granting guides to all players')

        sql = """
        DROP TRIGGER IF EXISTS grant_all_guides;
        CREATE TRIGGER IF NOT EXISTS grant_all_guides AFTER UPDATE ON Characters BEGIN UPDATE ServerAccountData SET Guide00="-1", Guide01="-1"; END; UPDATE ServerAccountData SET Guide00="-1", Guide01="-1";
        """
        try:
            conn = sqlite3.connect(self.miscreated_server_db)
            conn.executescript(sql)
        except Exception as e:
            logging.debug(e)


    def launch_server(self):
        logging.debug('method: launch_server')

        semaphore_file = Path('{}/smss.managed'.format(self.miscreated_server_path))

        f = open(semaphore_file, "w")
        f.write("This server is managed by Spafbi's Simplified Miscreated Server Setup script.")
        f.close()

        server_options = list()

        if self.bind_ip:
            server_options.append('-sv_bind {}'.format(self.bind_ip))

        if self.enable_whitelist:
            server_options.append('-mis_whitelist')
        
        if self.enable_rcon:
            server_options.append('+http_startserver')

        server_options.append('-sv_port {}'.format(self.port))
        server_options.append('-mis_gameserverid {}'.format(self.server_id))
        server_options.append('+sv_maxplayers {}'.format(self.max_players))
        server_options.append('+map {}'.format(self.miscreated_map))
        server_options.append('+sv_servername "{}"'.format(self.sv_servername))

        server_options = ' '.join(str(e) for e in server_options)

        server_cmd = '"{}"'.format(self.miscreated_server_cmd) + ' ' + server_options
    
        cvars=self.get_cvars()
        timestamp = str(date.today()) + ', ' + str(datetime.now().strftime("%I:%M %p"))
        message = self.get_start_server_message().format(
            cvars=cvars,
            date=date.today(),
            map=self.miscreated_map,
            mods=self.get_mod_titles(),
            port=self.port,
            rcon=self.port+4,
            sv_servername=self.sv_servername,
            timestamp=timestamp)
        print(message)
        logging.debug(server_cmd)
        logging.debug('Server started: ' + timestamp)
        asyncio.run(self.run(server_cmd))
        timestamp = str(date.today()) + ', ' + str(datetime.now().strftime("%I:%M %p"))
        logging.debug('Server closed: ' + timestamp)


    def prepare_server(self):
        """Method to bundle other methods to ensure server is ready to run
        """
        logging.debug('method: prepare_server')
        self.remove_server_mods()
        self.get_steam()
        self.validate_miscreated_server()


    def remove_server_mods(self):
        """Remove the mods directory if it exists. This is done to ensure that
           the latest version of the mods are installed in the Miscreated
           directory. We do this because Steam doesn't properly validate and
           refresh the mods; this does not force the mods to redownload each
           time as they are cached by steamcmd.
        """
        logging.debug('method: remove_server_mods')
        mods_dir = Path('{}/Mods'.format(self.miscreated_server_path))
        if os.path.exists(mods_dir):
            logging.debug('Removing mods directory to refresh mods')
            try:
                shutil.rmtree(mods_dir, ignore_errors=True)
            except OSError as e:
                logging.debug("Error: {} : {}".format(mods_dir, e.strerror))


    def replace_config_lines(self, filename, variable, value):
        """This method replaces all matching lines in config files having the
           format "variable=value"

        Args:
            filename (string): filesystem path to a file
            variable (string): variable name to be added or updated with a new
                               value
            value (string): the new value for the variable
        """
        logging.debug('method: replace_config_lines')
        # We haven't replaced anything yet so this value is False
        replaced = False

        # This rewrites the file making subsitutions where needed
        if os.path.exists(filename):
            for line in fileinput.input([filename], inplace=True):
                if line.strip().startswith('{}='.format(variable)):
                    line = '{}={}\n'.format(variable, value)
                    replaced = True
                sys.stdout.write(line)

        # if no lines were replaced open the file and write out the variable/value pair
        if not replaced:
            file = open(filename, 'a+')
            file.write('{}={}\n'.format(variable, value))
            file.close


    def reset_base_timers(self):
        if self.reset_bases:
            sql = "UPDATE Structures SET AbandonTimer=2419200 WHERE ClassName='PlotSign';"
            self.get_result_set(sql)
            return
        
        if not self.reset_base_owner_ids:
            return
        
        bases = self.get_result_set(self.get_bases_sql())

        account_ids = list()
        for base in bases:
            if base[0] in self.reset_base_owner_ids:
                account_ids.append(int(base[0]) - 76561197960265728)

        if len(account_ids):
            logging.debug('Reset bases for AccountIDs: {}'.format(account_ids))
            sql = "UPDATE Structures SET AbandonTimer=2419200 WHERE ClassName='PlotSign' AND AccountID IN ({});"
            sql = sql.format(', '.join(str(t) for t in account_ids))
            self.get_result_set(sql)


    def reset_base_object_timers(self, objects, owner_ids, update_sql, thing):
        bases = self.get_result_set(self.get_bases_sql())

        if not bases:
            return

        reset_objects = list()

        for base in bases:
            steam_id = base[0]
            x1 = base[1]
            y1 = base[2]
            if steam_id not in owner_ids:
                continue
            for this_object in objects:
                x2 = this_object[1]
                y2 = this_object[2]
                if self.calc_distance(x1, y1, x2, y2) <= 30:
                    reset_objects.append(this_object[0])

        if not len(reset_objects):
            return

        logging.debug('Reset {} ids: {}'.format(thing, reset_objects))
        update_sql = update_sql.format(', '.join(str(t) for t in reset_objects))
        self.get_result_set(update_sql)


    def reset_tent_timers(self):
        if self.reset_tents:
            sql = "UPDATE Structures SET AbandonTimer=2419200 WHERE ClassName like '%tent%';"
            self.get_result_set(sql)
            return

        if not self.reset_tent_owner_ids:
            return
        
        tents = self.get_result_set(self.get_tents_sql())

        if not tents:
            return

        sql = "UPDATE Structures SET AbandonTimer=2419200 WHERE StructureID IN ({});"
        self.reset_base_object_timers(tents, self.reset_tent_owner_ids, sql, 'tent')


    def reset_vehicle_timers(self):
        if self.reset_vehicles:
            sql = "UPDATE Vehicles SET AbandonTimer=2419200;"
            self.get_result_set(sql)
            return

        if not self.reset_vehicle_owner_ids:
            return
        
        vehicles = self.get_result_set(self.get_vehicles_sql())

        if not vehicles:
            return

        sql = "UPDATE Vehicles SET AbandonTimer=2419200 WHERE VehicleID IN ({});"
        self.reset_base_object_timers(vehicles, self.reset_vehicle_owner_ids, sql, 'vehicle')


    def stop_file_exists(self):
        """If any file staring with "stop" exists in the script directory then
           return True
        """
        if len(glob(str(Path('{}/stop*'.format(self.script_path))))):
            logging.info('stop file exist - remove the stop file to allow the server to restart automatically')
            return True
        return False


    def update_admin_cfg(self):
        """Updates the SvServerAdmin/settings.cfg file with the current class
           values if any ids are specified in the theros_admin_ids variable
        """
        logging.debug('method: update_admin_cfg')
        if not len(self.theros_admin_ids):
            return
    
        # Create the mod configuration directory if it doesn't exist
        admin_config_path = Path("{}/SvServerAdmin".format(self.miscreated_server_path))
        admin_config_path.mkdir(parents=True, exist_ok=True)

        # Convert the list to a string for use in the config file
        server_owner=','.join(str(t) for t in self.theros_admin_ids)
        server_owner='"{}"'.format(server_owner)
        
        # Assign sever_owner as the ServerOwner value in the mod config file
        admin_config = Path("{}/settings.cfg".format(admin_config_path))
        self.replace_config_lines(admin_config, 'ServerOwner', server_owner)


    def update_hosting_cfg(self):
        """Updates the hosting.cfg file with the current class values
        """
        logging.debug('method: update_hosting_cfg')
        filename = self.miscreated_server_config
        self.replace_config_lines(filename, 'as_corpseCountMax', self.as_corpseCountMax)
        self.replace_config_lines(filename, 'as_corpseRemovalTime', self.as_corpseRemovalTime)
        self.replace_config_lines(filename, 'asm_disable', int(self.asm_disable))
        self.replace_config_lines(filename, 'asm_hordeCooldown', self.asm_hordeCooldown)
        self.replace_config_lines(filename, 'asm_maxMultiplier', self.asm_maxMultiplier)
        self.replace_config_lines(filename, 'asm_percent', self.asm_percent)
        self.replace_config_lines(filename, 'g_craftingSpeedMultiplier', self.g_craftingSpeedMultiplier)
        self.replace_config_lines(filename, 'g_gameRules_Camera', self.g_gameRules_Camera)
        self.replace_config_lines(filename, 'g_gameRules_bases', self.g_gameRules_bases)
        self.replace_config_lines(filename, 'g_idleKickTime', self.g_idleKickTime)
        self.replace_config_lines(filename, 'g_maxHealthMultiplier', self.g_maxHealthMultiplier)
        self.replace_config_lines(filename, 'g_pingLimitGraceTimer', self.g_pingLimitGraceTimer)
        self.replace_config_lines(filename, 'g_pingLimitTimer', self.g_pingLimitTimer)
        self.replace_config_lines(filename, 'g_pinglimit', self.g_pinglimit)
        self.replace_config_lines(filename, 'g_playerFoodDecay', self.g_playerFoodDecay)
        self.replace_config_lines(filename, 'g_playerFoodDecaySprinting', self.g_playerFoodDecaySprinting)
        self.replace_config_lines(filename, 'g_playerHealthRegen', self.g_playerHealthRegen)
        self.replace_config_lines(filename, 'g_playerInfiniteStamina', self.g_playerInfiniteStamina)
        self.replace_config_lines(filename, 'g_playerTemperatureEnvRate', self.g_playerTemperatureEnvRate)
        self.replace_config_lines(filename, 'g_playerTemperatureSpeed', self.g_playerTemperatureSpeed)
        self.replace_config_lines(filename, 'g_playerWaterDecay', self.g_playerWaterDecay)
        self.replace_config_lines(filename, 'g_playerWaterDecaySprinting', self.g_playerWaterDecaySprinting)
        self.replace_config_lines(filename, 'g_playerWeightLimit', self.g_playerWeightLimit)
        self.replace_config_lines(filename, 'g_respawnAtBaseTime', self.g_respawnAtBaseTime)
        self.replace_config_lines(filename, 'http_password', self.http_password)
        self.replace_config_lines(filename, 'ism_maxCount', self.ism_maxCount)
        self.replace_config_lines(filename, 'ism_percent', self.ism_percent)
        self.replace_config_lines(filename, 'max_uptime', self.max_uptime)
        self.replace_config_lines(filename, 'pcs_maxCorpseTime', self.pcs_maxCorpseTime)
        self.replace_config_lines(filename, 'pcs_maxCorpses', self.pcs_maxCorpses)
        self.replace_config_lines(filename, 'sv_msg_conn', self.sv_msg_conn)
        self.replace_config_lines(filename, 'sv_msg_death', self.sv_msg_death)
        self.replace_config_lines(filename, 'sv_noBannedAccounts', self.sv_noBannedAccounts)
        self.replace_config_lines(filename, 'sv_servername', self.sv_servername)
        self.replace_config_lines(filename, 'wm_forceTime', self.wm_forceTime)
        self.replace_config_lines(filename, 'wm_pattern', self.wm_pattern)
        self.replace_config_lines(filename, 'wm_timeOffset', self.wm_timeOffset)
        self.replace_config_lines(filename, 'wm_timeScale', self.wm_timeScale)
        self.replace_config_lines(filename, 'wm_timeScaleNight', self.wm_timeScaleNight)

        if len(self.steam_ugc):
            self.replace_config_lines(filename, 'steam_ugc', self.steam_ugc)
        if len(self.sv_motd):
            self.replace_config_lines(filename, 'sv_motd', self.sv_motd)
        if len(self.sv_url):
            self.replace_config_lines(filename, 'sv_url', self.sv_url)


    def validate_miscreated_server(self):
        """Validates the Miscreated server. This also has the effect of
           installing the server if not yet installed.
        """
        logging.debug('method: validate_miscreated_server')

        """If any file staring with "skip" exists in the script directory then
           the Miscreated server will not be validated
        """
        if len(glob(str(Path('{}/skip*'.format(self.script_path))))):
            logging.info('skip file exist - remove the skip file to allow the server to validate the server automatically')
            return

        # Create the command used to validate/install the server
        install_cmd = 'steam_cmd +login anonymous +force_install_dir miscreated_server_path '\
                      '+app_update 302200 validate +quit'
        install_cmd = install_cmd.replace('steam_cmd', str(self.steamcmd))
        install_cmd = install_cmd.replace('miscreated_server_path', str(self.miscreated_server_path))
        
        # Execute the command
        logging.info('Validating Miscreated Server installation. This could take a while...')
        asyncio.run(self.run(install_cmd))
        logging.info('Miscreated Server installation validated')


def main():
    """
    Summary: Default method if this module is run as __main__.
    """
    import argparse

    # Argeparse description and configuration
    prog = os.path.basename(__file__)
    description = "{prog} Runs a Miscreated game server - all values not "\
                  "configured in a JSON formatted file will use Miscreated "\
                  "server defaults.".format(prog=prog)
    parser = argparse.ArgumentParser(prog=prog, description=description)
    parser.add_argument('-c', '--config', type=str, required=False,
                        help="""JSON configuration file""", default="smss.json")
    args = parser.parse_args()

    # This just grabs our script's path for reuse
    script_path = os.path.abspath(os.path.dirname(sys.argv[0]))

    # Check to see if the path includes a space and exit if it does
    if script_path.find(' ') >= 0:
        print('This script cannot be run in paths having spaces. Current path:')
        print('   {}'.format(script_path) + "\n")
        return

    # Check for files to trigger debug logging
    verbose = True if len(glob(str(Path('{}/debug*'.format(script_path))))) else False

    # Enable either INFO or DEBUG logging
    if verbose:
        smss_logger = logging.getLogger()
        smss_logger.setLevel(logging.DEBUG)

        output_file_handler = logging.FileHandler("smss.log")
        stdout_handler = logging.StreamHandler(sys.stdout)

        smss_logger.addHandler(output_file_handler)
        smss_logger.addHandler(stdout_handler)
    else:
        logging.basicConfig(level=logging.INFO)

    # Output argparse values
    logging.debug(args)

    # Start the server execution loop
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

        # Update hosting.cfg
        smss.update_hosting_cfg()

        # Update Theros' admin mod config
        smss.update_admin_cfg()

        # Prepare the Miscreated server
        smss.prepare_server()

        # Execute database maintenance "tricks"
        smss.database_tricks()

        # Launch the Miscreated server
        smss.launch_server()

        # Restart the server if a stop file does not exist
        run_server = not smss.stop_file_exists()

if __name__ == '__main__':
    main()