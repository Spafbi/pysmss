from bs4 import BeautifulSoup 
from colorama import init
from datetime import date, datetime
from glob import glob
from pathlib import Path
from pprint import pformat
from random import randint
from urllib import request
import asyncio
import fileinput
import itertools
import json
import logging
import math
import os
import requests
import shutil
import sqlite3
import sys
import threading
import time
import zipfile

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
        self.adopt_server = kwargs.get('adopt_server', False)
        self.adopt_server_completed = bool(kwargs.get('adopt_server_completed', False))
        self.adopt_smss_completed = bool(kwargs.get('adopt_smss_completed', False))
        self.as_corpsecountmax = int(kwargs.get('ai_corpses_max', 20))
        self.as_corpseremovaltime = int(kwargs.get('ai_corpses_removal', 300))
        self.asm_disable = int(bool(kwargs.get('disable_ai', 0)))
        self.asm_hordecooldown = int(kwargs.get('horde_cooldown', 900))
        self.asm_maxmultiplier = float(kwargs.get('asm_maxmultiplier', 1))
        self.asm_percent = int(kwargs.get('asm_percent', 60))
        self.bind_ip = kwargs.get('bind_ip', '0.0.0.0')
        self.enable_basic_pve = bool(kwargs.get('enable_basic_pve', False))
        self.enable_rcon = bool(kwargs.get('enable_rcon', True))
        self.enable_upnp = bool(kwargs.get('enable_upnp', False))
        self.enable_whitelist = bool(kwargs.get('enable_whitelist', False))
        self.g_craftingspeedmultiplier = float(kwargs.get('crafting_multiplier', 1))
        self.g_gamerules_bases = int(kwargs.get('base_rules', 1))
        self.g_gamerules_camera = int(kwargs.get('camera', 0))
        self.g_idlekicktime = int(kwargs.get('idle_kick_seconds', 300))
        self.g_maxhealthmultiplier = float(kwargs.get('player_health_multiplier', 1))
        self.g_pinglimit = int(kwargs.get('ping_limit', 0))
        self.g_pinglimitgracetimer = int(kwargs.get('ping_limit_grace_timer', 60))
        self.g_pinglimittimer = int(kwargs.get('ping_limit_timer', 60))
        self.g_playerfooddecay = float(kwargs.get('hunger_rate', 0.2777))
        self.g_playerfooddecaysprinting = float(kwargs.get('hunger_rate_while_running', 0.34722))
        self.g_playerhealthregen = float(kwargs.get('health_regen_rate', 0.111))
        self.g_playerinfinitestamina = bool(kwargs.get('infinite_stamina', 0))
        self.g_playertemperatureenvrate = float(kwargs.get('tempertature_environment_speed', 0.0005))
        self.g_playertemperaturespeed = float(kwargs.get('temperature_speed', 1.0))
        self.g_playerwaterdecay = float(kwargs.get('thirst_rate', 0.4861))
        self.g_playerwaterdecaysprinting = float(kwargs.get('thirst_rate_while_running', 0.607638))
        self.g_playerweightlimit = int(kwargs.get('player_weight_limit', 40))
        self.g_respawnatbasetime = int(kwargs.get('respawn_at_base_timeout', 30))
        self.grant_guides = bool(kwargs.get('grant_guides', False))
        self.http_password = str(kwargs.get('rcon_password', 'secret{}'.format(str(randint(0, 99999)).rjust(5, "0"))))
        self.ism_maxcount = int(kwargs.get('loot_concurrent_item_spawned', 750))
        self.ism_percent = float(kwargs.get('loot_spawner_percent', 20))
        self.log_verbosity = int(kwargs.get('log_verbosity', 0))
        self.log_writetofileverbosity = int(kwargs.get('log_writetofileverbosity', 3))
        self.max_players = int(kwargs.get('max_players', 36))
        self.miscreated_map = str(kwargs.get('map', 'islands'))
        self.mod_ids = kwargs.get('mod_ids', list())
        self.pcs_maxcorpses = int(kwargs.get('max_player_corpses', 20))
        self.pcs_maxcorpsetime = int(kwargs.get('max_corpse_time', 1200))
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
        self.smss_first_run = bool(kwargs.get('smss_first_run', True))
        self.sv_maxuptime = float(kwargs.get('max_uptime', 12))
        self.sv_motd = str(kwargs.get('sv_motd', ''))
        self.sv_msg_conn = bool(kwargs.get('connection_messages', 0))
        self.sv_msg_death = bool(kwargs.get('death_messages', 0))
        self.sv_nobannedaccounts = bool(kwargs.get('no_bans', 0))
        self.sv_servername = str(kwargs.get('server_name', 'Miscreated Self-hosted Server #{}'.format(str(randint(0, 999999)).rjust(6, "0"))))
        self.sv_url = str(kwargs.get('sv_url', ''))
        self.theros_admin_ids = kwargs.get('theros_admin_ids', list())
        self.time_day_minutes = float(kwargs.get('time_day_minutes', 390))
        self.time_night_minutes = float(kwargs.get('time_night_minutes', 82.5))
        self.wm_effectscaleoffset = float(kwargs.get('wm_effectscaleoffset', 0.00))
        self.wm_forcetime = float(kwargs.get('force_time', -1))
        self.wm_pattern = int(kwargs.get('wm_pattern', -1))
        self.wm_timeoffset = float(kwargs.get('time_offset', -1))

        # Variables which are derived from passed/default values
        self.wm_timescale = float(self.get_timeScale(self.time_day_minutes))
        self.wm_timescalenight = float(self.get_timeScaleNight(self.time_night_minutes))
        self.steam_ugc = self.condense_mods()

        # Configure paths variables for required directories
        self.script_path = os.path.dirname(os.path.realpath(__file__))

        ## Adopt a legacy SMSS server
        if os.path.exists(Path('{}/scriptvars'.format(self.script_path))) and \
           os.path.exists(Path('{}/MiscreatedServer'.format(self.script_path))) and \
           not self.adopt_server:
            self.adopt_server = Path('{}/MiscreatedServer'.format(self.script_path))

        if self.adopt_server:
            ## Adopt and existing server
            self.miscreated_server_path = Path(self.adopt_server)
        else:
            ## Install the server in this path
            this_path = "{}/MiscreatedServer".format(self.script_path)
            self.miscreated_server_path = Path(this_path)
            self.adopt_server = self.miscreated_server_path

        print(self.script_path, self.miscreated_server_path, self.adopt_server)

        self.get_last_map()

        ## SteamCMD installation directory
        self.steamcmd_path = Path("{}/SteamCMD".format(self.script_path))

        ## A place where we'll store temporary files
        self.temp_path = Path("{}/temp".format(self.script_path))

        # Create required paths
        self.miscreated_server_path.mkdir(parents=True, exist_ok=True)
        self.steamcmd_path.mkdir(parents=True, exist_ok=True)
        self.temp_path.mkdir(parents=True, exist_ok=True)

        # Configure filename variables
        self.config_file = kwargs.get('config_file', Path('{}/smss.json'.format(self.script_path)))
        self.miscreated_server_cmd = Path("{}/Bin64_dedicated/MiscreatedServer.exe".format(self.miscreated_server_path))
        self.miscreated_server_config = Path("{}/hosting.cfg".format(self.miscreated_server_path))
        self.miscreated_server_db = Path("{}/miscreated.db".format(self.miscreated_server_path))
        self.steamcmd = Path("{}/steamcmd.exe".format(self.steamcmd_path))

        # Set the server id
        if not self.server_id:
           self.server_id = self.get_server_id_from_db()
           self.add_to_json_config('server_id', self.server_id)

        # Adding this for convenience
        self.add_to_json_config('enable_basic_pve', self.enable_basic_pve)

        # For spinner support
        self.spinner_done = False

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


    def add_to_json_config(self, key, value):
        """This adds a new key:value pair to smss.json

        Args:
            key (str): The name of the JSON key
            value (any): The value for this key
        """
        logging.debug('method: add_to_json_config')
        # Read the existing JSON file into a dictionary.
        try:
            with open(Path(self.config_file), "r") as f:
                json_config = json.load(f)
        except Exception as e:
            json_config = dict()
            logging.debug(e)

        # Add the new key:value pair to the dictionary
        json_config[key] = value

        # Write the dictionary out to smss.json
        with open(Path(self.config_file), 'w') as f:
            json.dump(json_config, f, indent = 4, sort_keys=True)


    def adopt_existing_server(self):
        """If the script is run in a legacy Simplified Miscreated Server Setup location the old "scriptvars" values will
           be adopted. If a path is specified in the smss.json configuration file for the "adopt_server" key, then
           settings handled by this script, and defined in hosting.cfg, will be adopted by this script. After an
           existing server is adopted, further changes for handled values will need to be made in the smss.json file.
        """
        logging.debug('method: adopt_existing_server')

        # Only adopt legacy SMSS values if they have not yet been adopted.
        if not self.adopt_smss_completed:
            self.adopt_existing_smss()

        # Only adopt an existing Miscreated server's hosting.cfg values if the "adopt_server" path for the existing
        # server has been defined and the server has not yet been adopted.
        if self.adopt_server and not self.adopt_server_completed:
            # Let's see what the last server map loaded was and adopt that.
            last_map = self.get_last_map()
            ## If the miscreated_map class var is islands, and last_map has a non-False value, use the detected last map
            if self.miscreated_map == 'islands' and last_map:
                self.miscreated_map = last_map
            self.adopt_existing_hosting_cfg_values()


    def adopt_existing_hosting_cfg_values(self):
        """Adopts an existing Miscreated server installation
        """
        logging.debug('method: adopt_existing_hosting_cfg_values')

        # If the specified hosting.cfg file does not exist we exit with critical error.
        if not os.path.exists(self.miscreated_server_config):
            logging.critical('The specified hosting.cfg cannot be adopted: {}'.format(self.miscreated_server_config))
            logging.critical('Make sure the "adopt_server" value specified in config.json is correct')
            exit(1)

        # 
        handled_values = self.get_handled_values()

        # Read existing values
        hosting_cfg = open(self.miscreated_server_config, 'r')
        cfg_lines = hosting_cfg.readlines()

        for line in cfg_lines:
            # If the line is commented out or doesn't have an = on it skip it.
            if line.strip().startswith('--') or not line.find('=') or not len(line.strip()):
                continue
            
            # Split our line into key and value
            key, value = line.strip().split('=', 1)

            # If either key or value has zero length continue
            if not len(key) or not len(value):
                continue

            # make the key lowercase
            key = key.strip().lower()

            # grab the JSON key name we'll use for this value
            json_cfg_key = handled_values.get(key, False)

            # Unless changed, this is the value which will be written to hosting.cfg
            cfg_value = value.strip()

            # if there's no key skip this line.
            if not key or not json_cfg_key:
                continue

            # Special Handling
            if key == "wm_timescale":
                # Calculate minutes of daylight
                json_value = self.get_timeScale(float(cfg_value))
            elif key == "wm_timescalenight":
                # Calculate minutes of night
                json_value = self.get_timeScaleNight(float(cfg_value))
            elif key == "steam_ugc":
                # Process the mods list
                json_value = list()
                for mod_id in cfg_value.split(','):
                    try:
                        # Convert the mod ID to an integer
                        this_value = int(mod_id.strip())
                    except:
                        # If we couldn't convert the mod ID to an integer the original hosting.cfg was borked.
                        logging.debug('Mod id is not an integer: {}'.format(mod_id))
                        this_value = False

                    # If the mod_id wasn't an integer, or if it's Theros' admin mod, continue on to the next mod
                    if this_value in (False, 2011185435):
                        continue
                    # Add the mod_id to the list of mods.
                    json_value.append(this_value)
                
                # Create a string from the mod list
                cfg_value = ','.join(str(x) for x in json_value)
            else:
                # Since special handling wasn't needed just do a direct value assignment
                json_value = cfg_value

            if isinstance(vars(self)[key], int):
                try:
                    cfg_value = int(cfg_value)
                    json_value = int(json_value)
                except:
                    logging.debug('Could not set type to int for key[{}]: {}'.format(key, cfg_value))
            if isinstance(vars(self)[key], float):
                try:
                    cfg_value = float(cfg_value)
                    json_value = float(json_value)
                except:
                    logging.debug('Could not set type to float for key[{}]: {}'.format(key, cfg_value))
            if isinstance(vars(self)[key], bool):
                try:
                    cfg_value = bool(int(cfg_value))
                    json_value = bool(int(json_value))
                except:
                    logging.debug('Could not set type to bool for key[{}]: {}'.format(key, cfg_value))

            # Assign our class variables by reference
            vars(self)[key] = cfg_value

            # Reprocess steam_ugc to remove duplicate mods
            if key == 'steam_ugc':
                self.steam_ugc = self.condense_mods()

            # If the value we're working with is one of our handled JSON keys, write it.
            if json_cfg_key:
                self.add_to_json_config(json_cfg_key, json_value)
        
        # Write out the imported values
        self.add_to_json_config('adopt_server_completed', True)
        
        # We'll write this out just in case the server was an imported legacy SMSS server
        self.add_to_json_config("adopt_server", str(self.adopt_server))


    def adopt_existing_smss(self):
        """Adopt the settings from a legacy SMSS installation
        """
        smss_vars = {
            'bind': {
                'json_name': 'bind_ip',
                'smss_name': 'bind'
                },
            'port': {
                'json_name': 'port',
                'smss_name': 'baseport',
                'type': 'int'
                },
            'g_gamerules_bases': {
                'json_name': 'base_rules',
                'smss_name': 'buildrule',
                'type': 'int'
                },
            'enable_upnp': {
                'json_name': 'enable_upnp',
                'smss_name': 'enableupnp',
                'type': 'bool'
                },
            'grant_guides': {
                'json_name': 'grant_guides',
                'smss_name': 'grantguides',
                'type': 'bool'
                },
            'miscreated_map': {
                'json_name': 'map',
                'smss_name': 'map'
                },
            'max_players': {
                'json_name': 'max_players',
                'smss_name': 'maxplayers',
                'type': 'int'
                },
            'http_password': {
                'json_name': 'rcon_password',
                'smss_name': 'rcon_password'
                },
            'sv_servername': {
                'json_name': 'server_name',
                'smss_name': 'server_name'
                },
            'enable_whitelist': {
                'json_name': 'enable_whitelist',
                'smss_name': 'whitelisted',
                'type': 'bool'
                }
        }

        # Loop through the handled settings
        for key, var_info in smss_vars.items():
            file_name = Path('{}/scriptvars/{}.txt'.format(self.script_path, var_info.get('smss_name')))
            try:
                with open(file_name) as f:
                    this_value = f.readline().strip()
            except:
                logging.debug('File does not exist - skipped: {}'.format(file_name))
                this_value = False
            
            if not this_value or not len(this_value):
                logging.debug('{} had no value'.format(var_info.get('smss_name')))
                continue
            
            this_type = var_info.get('type', 'str')
            if this_type == 'bool':
                if this_value.lower() in ('y', '1'):
                    this_value = True
                elif this_value.lower() in ('n', '0'):
                    this_value = False
                else:
                    logging.debug('Type mismatch for scriptvar: '+var_info.get(smss_name))
                    logging.debug('Skipping adoption of this setting')
                    continue
            elif this_type == 'int':
                try:
                    this_value = int(this_value)
                except Exception as e:
                    logging.debug(e)
                    logging.debug('Type mismatch for scriptvar: '+var_info.get(smss_name))

            vars(self)[key] = this_value
            self.add_to_json_config(var_info.get('json_name'), this_value)

        self.add_to_json_config('adopt_smss_completed', True)


    def calc_distance(self, x1, y1, x2, y2):
        """Calculates the distance between two objects on a plane

        Args:
            x1 (float): X position value for object 1
            y1 (float): Y position value for object 1
            x2 (float): X position value for object 2
            y2 (float): Y position value for object 2

        Returns:
            float: [description]
        """
        dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        return dist


    def condense_mods(self):
        """Removes non-unique mod ids and adds Theros' admin mod if the option
           was selected

        Returns:
            string: A comma delimited string for use in hosting.cfg
        """
        unique_mods = list()
        logging.debug('method: condense_mods')
        if self.theros_admin_ids:
            unique_mods.append(2011185435)

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
        """SQL command to look up all bases

        Returns:
            string: SQL command
        """
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
        """Returns a list of hosting.cfg cvars and their values. Primarily for
           logging purposts.

        Returns:
            dictionary: Dictionary of cvars by category, cvar name, and value
        """
        hosting_cfg_cvars = {
            'ai': {
                'asm_disable': self.asm_disable,
                'asm_hordecooldown': self.asm_hordecooldown,
                'asm_maxmultiplier': self.asm_maxmultiplier,
                'asm_percent': self.asm_percent
            },
            'corpses': {
                'as_corpsecountmax': self.as_corpsecountmax,
                'as_corpseremovaltime': self.as_corpseremovaltime,
                'pcs_maxcorpsetime': self.pcs_maxcorpsetime,
                'pcs_maxcorpses': self.pcs_maxcorpses
            },
            'loot': {
                'ism_maxcount': self.ism_maxcount,
                'ism_percent': self.ism_percent
            },
            'players': {
                'g_craftingspeedmultiplier': self.g_craftingspeedmultiplier,
                'g_gamerules_camera': self.g_gamerules_camera,
                'g_gamerules_bases': self.g_gamerules_bases,
                'g_idlekicktime': self.g_idlekicktime,
                'g_maxhealthmultiplier': self.g_maxhealthmultiplier,
                'g_pinglimitgracetimer': self.g_pinglimitgracetimer,
                'g_pinglimittimer': self.g_pinglimittimer,
                'g_pinglimit': self.g_pinglimit,
                'g_playerfooddecay': self.g_playerfooddecay,
                'g_playerfooddecaysprinting': self.g_playerfooddecaysprinting,
                'g_playerhealthregen': self.g_playerhealthregen,
                'g_playerinfinitestamina': self.g_playerinfinitestamina,
                'g_playertemperatureenvrate': self.g_playertemperatureenvrate,
                'g_playertemperaturespeed': self.g_playertemperaturespeed,
                'g_playerwaterdecay': self.g_playerwaterdecay,
                'g_playerwaterdecaysprinting': self.g_playerwaterdecaysprinting,
                'g_respawnatbasetime': self.g_respawnatbasetime
            },
            'server': {
                'http_password': '*'*len(self.http_password),
                'log_verbosity': self.log_verbosity,
                'log_writetofileverbosity': self.log_writetofileverbosity,
                'sv_maxuptime': self.sv_maxuptime,
                'sv_msg_conn': self.sv_msg_conn,
                'sv_msg_death': self.sv_msg_death,
                'sv_nobannedaccounts': self.sv_nobannedaccounts,
                'sv_servername': self.sv_servername
            },
            'time and weather': {
                'wm_effectscaleoffset': self.wm_effectscaleoffset,
                'wm_forcetime': self.wm_forcetime,
                'wm_pattern': self.wm_pattern,
                'wm_timeoffset': self.wm_timeoffset,
                'wm_timescale': self.wm_timescale,
                'wm_timescalenight': self.wm_timescalenight
            }
        }
        if len(self.steam_ugc):
            hosting_cfg_cvars['server']['steam_ugc'] = self.steam_ugc
        if self.sv_motd:
            hosting_cfg_cvars['server']['sv_motd'] = self.sv_motd
        if self.sv_url:
            hosting_cfg_cvars['server']['sv_url'] = self.sv_url
        return pformat(hosting_cfg_cvars, indent=2)

    def get_handled_values(self):
        """These are the hosting.cfg configuration values handled by this script - each hosting.cfg setting is paired
           with the corresponding JSON key names

        Returns:
            dictionary: hosting.cfg:smss.json configuration pairs.
        """
        return {
            'as_corpsecountmax': 'ai_corpses_max',
            'as_corpseremovaltime': 'ai_corpses_removal',
            'asm_disable': 'disable_ai',
            'asm_hordecooldown': 'horde_cooldown',
            'asm_maxmultiplier': 'asm_maxmultiplier',
            'asm_percent': 'asm_percent',
            'g_craftingspeedmultiplier': 'crafting_multiplier',
            'g_gamerules_camera': 'camera',
            'g_gamerules_bases': 'base_rules',
            'g_idlekicktime': 'idle_kick_seconds',
            'g_maxhealthmultiplier': 'player_health_multiplier',
            'g_pinglimitgracetimer': 'ping_limit_grace_timer',
            'g_pinglimittimer': 'ping_limit_timer',
            'g_pinglimit': 'ping_limit',
            'g_playerfooddecay': 'hunger_rate',
            'g_playerfooddecaysprinting': 'hunger_rate_while_running',
            'g_playerhealthregen': 'health_regen_rate',
            'g_playerinfinitestamina': 'infinite_stamina',
            'g_playertemperatureenvrate': 'tempertature_environment_speed',
            'g_playertemperaturespeed': 'temperature_speed',
            'g_playerwaterdecay': 'thirst_rate',
            'g_playerwaterdecaysprinting': 'thirst_rate_while_running',
            'g_playerweightlimit': 'player_weight_limit',
            'g_respawnatbasetime': 'respawn_at_base_timeout',
            'http_password': 'rcon_password',
            'ism_maxcount': 'loot_concurrent_item_spawned',
            'ism_percent': 'loot_spawner_percent',
            'log_verbosity': 'log_verbosity',
            'log_writetofileverbosity': 'log_writetofileverbosity',
            'pcs_maxcorpsetime': 'max_corpse_time',
            'pcs_maxcorpses': 'max_player_corpses',
            'steam_ugc': 'mod_ids',
            'sv_maxuptime': 'max_uptime',
            'sv_motd': 'sv_motd',
            'sv_msg_conn': 'connection_messages',
            'sv_msg_death': 'death_messages',
            'sv_nobannedaccounts': 'no_bans',
            'sv_servername': 'server_name',
            'sv_url': 'sv_url',
            'wm_effectscaleoffset': 'wm_effectscaleoffset',
            'wm_forcetime': 'force_time',
            'wm_pattern': 'wm_pattern',
            'wm_timeoffset': 'time_offset',
            'wm_timescale': 'time_day_minutes',
            'wm_timescalenight': 'time_night_minutes'
            }


    def get_last_map(self):
        """Read the server logs and try to derive the most recent map loaded by the server. 

        Returns:
            string or bool: map name or False
        """
        server_logs = glob(str(Path('{}/server*.log'.format(self.miscreated_server_path))))
        if not len(server_logs):
            return 'islands'
        latest_log = max(server_logs, key=os.path.getctime)
        search = open(latest_log, "r")
        this_map = False
        for line in search:
            if not line.find(" Command line: ") > -1:
                continue
            cli_parts = line.split('+')
            for part in cli_parts:
                if part[:3] == 'map':
                    map_directive, value = part.split(' ', 1)
                    this_map = value.strip().lower()
        return this_map


    def get_mod_name(self, mod_id):
        """Retrieves the name of a Steam Workshop mod

        Args:
            mod_id (int): Steam Workshop file id

        Returns:
            string: Steam Workshop mod name
        """
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
        """Returns a list of mod ids and their names, formatted for output in
           the server start summary screen.

        Returns:
            string: list of mod ids and their names
        """
        if not len(self.steam_ugc):
            return "<none>"

        mod_ids=self.steam_ugc.split(',')
        first = True
        mod_list = ''
        for mod in mod_ids:
            this_line = ''
            if not first:
                this_line = '\n'+' '*20
            mod_list = mod_list + this_line + self.get_mod_name(mod)
            first=False
        return mod_list


    def get_result_set(self, sql):
        """The executes a passed SQL command and returns a result set. If
           INSERT or UPDATE is detected, a write is assumed and a commit is
           also performed.

        Args:
            sql (string): SQL command

        Returns:
            list: a result set resulting from the execution of the SQL command
        """
        if not os.path.exists(self.miscreated_server_db):
            logging.debug('Database not yet created')
            return False

        logging.debug(sql)

        # If 'insert ' or 'update ' exist in the sql statement, we're probably
        # doing a database write and will want to commit the changes.
        commit = (sql.lower().find('insert ') >= 0) or \
                 (sql.lower().find('update ') >= 0)

        conn = sqlite3.connect(self.miscreated_server_db)
        c = conn.cursor()
        try:
            results = c.execute(sql)
            if commit:
                conn.commit()
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


    def get_timeScale(self, time_length = 1):
        """Calculate the correct wm_timescale value based on the passed value. If the passed value is in minutes, the
           returned value is the multiplier (sv_timeScale). Conversely, if an multiplier use passed, the time in minutes
           for time_day_minutes is returned.

        Returns:
            float: wm_timescale multiplier or time_day_minutes value
        """
        logging.debug('method: get_timeScale')
        if not time_length: # prevent divide by zero attempt
            return 1
        return round(780/time_length, 2)


    def get_timeScaleNight(self, time_length = 1):
        """Calculate the correct wm_timescalenight value based on the passed value. If the passed value is in minutes,
            the returned value is the multiplier (sv_timeScaleNight). Conversely, if an multiplier use passed, the time
            in minutes for time_night_minutes is returned.

        Returns:
            float: wm_timescalenight multiplier or time_night_minutes value
        """
        logging.debug('method: get_timeScaleNight')
        if not self.wm_timescale or not time_length: # prevent divide by zero attempt
            return 1
        return round(660/(self.wm_timescale*time_length), 2)


    def get_start_server_message(self):
        """Returns a block of text to be used for the server start summary
           screen

        Returns:
            string: server summary string
        """

        # The following is just some ASCII characters for creating boxes
        # ║╔╗╚╝─═╟╢
        
        message = '═'*118+'\r\n'+'═'*118+'\r\n'\
                  '       [1m[36mServer Name: [1m[33m{sv_servername}[0m\r\n'\
                  '               [1m[36mMap: [1m[33m{map}[0m\r\n'\
                  '              [1m[36mMods: [1m[33m{mods}[0m\r\n'\
                  '  [1m[36mGame Ports (UDP): [1m[33m{port}[0m\r\n'\
                  '   [1m[36mRCON Port (TCP): [1m[33m{rcon}[0m\r\n'\
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
        """SQL command to look up all tents

        Returns:
            string: SQL command
        """
        sql = """
            SELECT StructureID,
                ROUND(PosX,5) AS PosX,
                ROUND(PosY,5) AS PosY
            FROM Structures
            WHERE ClassName like '%tent%'
            """
        return sql


    def get_vehicles_sql(self):
        """SQL command to look up all vehicles

        Returns:
            string: SQL command
        """
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
        """Launch a Miscreated server instance
        """
        logging.debug('method: launch_server')

        semaphore_file = Path('{}/smss.managed'.format(self.miscreated_server_path))

        f = open(semaphore_file, "w")
        f.write("This server is managed by Spafbi's Simplified Miscreated Server Setup script.")
        f.close()

        if self.smss_first_run:
            self.add_to_json_config('smss_first_run', False)
            print("The server's configurable settings have been written to smss.json. Edit smss.json with the desired "\
                  "values and re-run the script to start the server.")
            return

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
            port=", ".join([str(i) for i in range(self.port,self.port+4)]),
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
        logging.debug('method: replace_config_lines :: {}'.format(variable))
        # We haven't replaced anything yet so this value is False
        replaced = False

        # This rewrites the file making subsitutions where needed
        if os.path.exists(filename):
            for line in fileinput.input([filename], inplace=True):
                if line.strip().lower().startswith('{}='.format(variable.lower())):
                    line = '{}={}\n'.format(variable.lower(), value)
                    replaced = True
                sys.stdout.write(line)

        # if no lines were replaced open the file and write out the variable/value pair
        if not replaced:
            with open(filename, 'r') as f:
                for line in f:
                    pass
            file_name = open(filename, 'a+')
            if not line == "\n":
                file_name.write('\n')
            file_name.write('{}={}'.format(variable.lower(), value))
            file_name.close


    def reset_base_timers(self):
        """Reset base timers according to configured settings
        """
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
        """Reset timers bases on passed settings.

        Args:
            objects (dictionary): result set of objects to be reset
            owner_ids (list): 'owner' ids for which objects should be reset
            update_sql (string): SQL command to perform update
            thing (string): the type of object being reset - for logging purposes
        """
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
        """Reset tent timers according to configured settings
        """
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
        """Reset vehicle timers according to configured settings
        """
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


    def spinner(self):
        """As long as self.spinner_done is False a spinner will appear to help
           keep the script from looking like it's stalled.
        """
        for c in itertools.cycle(['|', '/', '-', '\\']):
            if self.spinner_done:
                break
            sys.stdout.write('\rloading ' + c)
            sys.stdout.flush()
            time.sleep(0.1)
        sys.stdout.write('\r')


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
        self.replace_config_lines(filename, 'as_corpsecountmax', self.as_corpsecountmax)
        self.replace_config_lines(filename, 'as_corpseremovaltime', self.as_corpseremovaltime)
        self.replace_config_lines(filename, 'asm_disable', int(self.asm_disable))
        self.replace_config_lines(filename, 'asm_hordecooldown', self.asm_hordecooldown)
        self.replace_config_lines(filename, 'asm_maxmultiplier', self.asm_maxmultiplier)
        self.replace_config_lines(filename, 'asm_percent', self.asm_percent)
        self.replace_config_lines(filename, 'g_craftingspeedmultiplier', self.g_craftingspeedmultiplier)
        self.replace_config_lines(filename, 'g_gamerules_camera', self.g_gamerules_camera)
        self.replace_config_lines(filename, 'g_gamerules_bases', self.g_gamerules_bases)
        self.replace_config_lines(filename, 'g_idlekicktime', self.g_idlekicktime)
        self.replace_config_lines(filename, 'g_maxhealthmultiplier', self.g_maxhealthmultiplier)
        self.replace_config_lines(filename, 'g_pinglimitgracetimer', self.g_pinglimitgracetimer)
        self.replace_config_lines(filename, 'g_pinglimittimer', self.g_pinglimittimer)
        self.replace_config_lines(filename, 'g_pinglimit', self.g_pinglimit)
        self.replace_config_lines(filename, 'g_playerfooddecay', self.g_playerfooddecay)
        self.replace_config_lines(filename, 'g_playerfooddecaysprinting', self.g_playerfooddecaysprinting)
        self.replace_config_lines(filename, 'g_playerhealthregen', self.g_playerhealthregen)
        self.replace_config_lines(filename, 'g_playerinfinitestamina', int(self.g_playerinfinitestamina))
        self.replace_config_lines(filename, 'g_playertemperatureenvrate', self.g_playertemperatureenvrate)
        self.replace_config_lines(filename, 'g_playertemperaturespeed', self.g_playertemperaturespeed)
        self.replace_config_lines(filename, 'g_playerwaterdecay', self.g_playerwaterdecay)
        self.replace_config_lines(filename, 'g_playerwaterdecaysprinting', self.g_playerwaterdecaysprinting)
        self.replace_config_lines(filename, 'g_playerweightlimit', self.g_playerweightlimit)
        self.replace_config_lines(filename, 'g_respawnatbasetime', self.g_respawnatbasetime)
        self.replace_config_lines(filename, 'http_password', self.http_password)
        self.replace_config_lines(filename, 'ism_maxcount', self.ism_maxcount)
        self.replace_config_lines(filename, 'ism_percent', self.ism_percent)
        self.replace_config_lines(filename, 'log_verbosity', self.log_verbosity)
        self.replace_config_lines(filename, 'log_writetofileverbosity', self.log_writetofileverbosity)
        self.replace_config_lines(filename, 'pcs_maxcorpsetime', self.pcs_maxcorpsetime)
        self.replace_config_lines(filename, 'pcs_maxcorpses', self.pcs_maxcorpses)
        self.replace_config_lines(filename, 'sv_maxuptime', self.sv_maxuptime)
        self.replace_config_lines(filename, 'sv_msg_conn', int(self.sv_msg_conn))
        self.replace_config_lines(filename, 'sv_msg_death', int(self.sv_msg_death))
        self.replace_config_lines(filename, 'sv_nobannedaccounts', int(self.sv_nobannedaccounts))
        self.replace_config_lines(filename, 'sv_servername', self.sv_servername)
        self.replace_config_lines(filename, 'wm_effectscaleoffset', self.wm_effectscaleoffset)
        self.replace_config_lines(filename, 'wm_forcetime', self.wm_forcetime)
        self.replace_config_lines(filename, 'wm_pattern', self.wm_pattern)
        self.replace_config_lines(filename, 'wm_timeoffset', self.wm_timeoffset)
        self.replace_config_lines(filename, 'wm_timescale', self.wm_timescale)
        self.replace_config_lines(filename, 'wm_timescalenight', self.wm_timescalenight)

        if len(self.steam_ugc):
            self.replace_config_lines(filename, 'steam_ugc', self.steam_ugc)
        if len(self.sv_motd):
            self.replace_config_lines(filename, 'sv_motd', self.sv_motd)
        if len(self.sv_url):
            self.replace_config_lines(filename, 'sv_url', self.sv_url)

        if self.enable_basic_pve:
            self.replace_config_lines(filename, 'g_gamerules_faction0_dmg_f0', 0)
            self.replace_config_lines(filename, 'g_gamerules_faction0_dmg_f2', 0)
            self.replace_config_lines(filename, 'g_gamerules_faction1_dmg_f2', 0)


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

        self.spinner_done=False
        t = threading.Thread(target=self.spinner)
        t.start()
        asyncio.run(self.run(install_cmd))
        self.spinner_done=True
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

    # Read the JSON configuration file
    try:
        with open(args.config) as f:
            json_config = json.load(f)
    except Exception as e:
        logging.debug(e)
        logging.debug("Configuration file load error. Using default configuration")
        json_config={}

    logging.debug(json_config)

    smss = SmssConfig(**json_config)

    # Adopt an existing server - 
    smss.adopt_existing_server()

    # Update hosting.cfg
    smss.update_hosting_cfg()

    # Update Theros' admin mod config
    smss.update_admin_cfg()

    # Prepare the Miscreated server
    smss.prepare_server()

    # Execute database maintenance "tricks"
    smss.database_tricks()

    # Record the time we start the server
    start_time = time.time()

    # Launch the Miscreated server
    smss.launch_server()

    # Restart the server if a stop file does not exist
    run_server = not smss.stop_file_exists()

    # If the server executed prematurely create a stop file
    if time.time() - start_time < 10:
        print("The server process exited in less than 10 seconds. A 'stop' file has been created to prevent the " \
              "server from trying to restart. Remove the stop file to allow the server to automatically restart.")
        f = open("stop", "w+")
        f.write("Don't restart the Miscreated server")
        f.close()

if __name__ == '__main__':
    main()