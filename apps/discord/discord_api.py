# Source https://github.com/phillco/talon-videoconferencing/tree/work

import json
import os
import platform
import re
import socket
import struct
import uuid

import requests
from typing import Optional
from talon import Context, Module, actions, ui

# ================================================================================
# SET UP INSTRUCTIONS:
# ================================================================================

# 1. Create an app here: https://discord.com/developers/applications

# 2. Create a JSON file at this path:
OAUTH2_CREDENTIALS_PATH = os.path.expanduser("~/.discord/discord-oauth2-creds.json")

# ...with client_id, client_secret, redirect_uri keys, like so:
# {
# 	"client_id": "YOUR_CLIENT_ID",
# 	"client_secret": "YOUR_CLIENT_SECRET",
# 	"redirect_uri": "https://YOUR_REDIRECT_URL"
# }

# 3. That's it! Try calling `actions.user.discord_toggle_mute()` from the REPL.

# ================================================================================
# Constants
# ================================================================================

API_ENDPOINT = "https://discord.com/api/v10"

# Where we store the refresh and access token on disk.
OAUTH2_CACHE_PATH = os.path.expanduser("~/.discord/discord-creds.json")

VERBOSE_LOGGING = False


class DiscordError(RuntimeError):
    pass


class DiscordClient:
    """Client that connects to Discord's local IPC API"""

    def __init__(self, client_id: str, client_secret: str, redirect_uri: str):
        super().__init__()

        system = platform.system().lower()
        if system not in ["darwin", "linux", "windows"]:
            raise DiscordError(f"Discord IPC doesn't support {system}.")

        self.platform = system
        self.ipc_path = self._get_ipc_path()

        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.access_token = None
        self.refresh_token = None

        self.pid = os.getpid()
        self.connected = False
        self.activity = None
        self.socket = None

    def _get_ipc_path(self, ipc_id=0):
        """Get the path to IPC Socket connection."""
        if self.platform == "windows":
            # IPC path for Windows.
            return f"\\\\?\\pipe\\discord-ipc-{ipc_id}"
        else:
            # IPC path for unix based systems (Linux, macOS).
            path = (
                os.environ.get("XDG_RUNTIME_DIR")
                or os.environ.get("TMPDIR")
                or os.environ.get("TMP")
                or os.environ.get("TEMP")
                or "/tmp"
            )
            return re.sub(r"\/$", "", path) + f"/discord-ipc-{ipc_id}"

    def _encode(self, opcode, payload):
        """Encode the payload to send to the IPC Socket."""
        payload = json.dumps(payload)
        payload = payload.encode("utf-8")
        return struct.pack("<ii", opcode, len(payload)) + payload

    def _decode(self):
        """Decode the data received from Discord."""
        try:
            if self.platform == "windows":
                encoded_header = b""
                header_size = 8

                while header_size:
                    encoded_header += self.socket.read(header_size)
                    header_size -= len(encoded_header)

                decoded_header = struct.unpack("<ii", encoded_header)
                encoded_data = b""
                remaining_packet_size = int(decoded_header[1])

                while remaining_packet_size:
                    encoded_data += self.socket.read(remaining_packet_size)
                    remaining_packet_size -= len(encoded_data)
            else:
                recived_data = self.socket.recv(4096)
                encoded_header = recived_data[:8]
                decoded_header = struct.unpack("<ii", encoded_header)
                encoded_data = recived_data[8:]
        except socket.timeout as e:
            raise DiscordError(f"Socket timeout: {e}")

        result = json.loads(encoded_data.decode("utf-8"))
        if VERBOSE_LOGGING:
            print(result)
        return result

    def _send(self, opcode, payload):
        """Send the payload to Discord via Discord IPC Socket."""
        encoded_payload = self._encode(opcode, payload)

        try:
            if self.platform == "windows":
                self.socket.write(encoded_payload)
                self.socket.flush()
            else:
                self.socket.sendall(encoded_payload)
        except Exception as e:
            raise DiscordError(f"Can't send data to Discord via IPC: {e}")

    def connect(self):
        """Connect to Discord Client via IPC."""
        if self.connected:
            print("[discord_client] Already connected.")
            return

        try:
            if self.platform == "windows":
                self.socket = open(self.ipc_path, "w+b")
            else:
                self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
                self.socket.settimeout(0.25)
                self.socket.connect(self.ipc_path)
        except Exception as e:
            raise DiscordError(f"Can't connect to Discord Client: {e}")

        # Handshake
        self._send(0, {"v": 1, "client_id": self.client_id})
        self._decode()
        self.connected = True

    def disconnect(self):
        """Terminate connection to Discord IPC Socket."""
        # Send disconnect command
        self._send(2, {})

        if self.platform != "windows":
            self.socket.shutdown(socket.SHUT_RDWR)

        self.socket.close()
        self.socket = None
        self.connected = False
        self.activity = None

    def authorize_if_needed(self):
        if os.path.exists(OAUTH2_CACHE_PATH):
            # Just use the cached OAuth2 details:
            with open(OAUTH2_CACHE_PATH) as f:
                obj = json.load(f)
                self.access_token = obj["access_token"]
                self.refresh_token = obj["refresh_token"]
                return

        self.oauth2_authorize()

    def oauth2_authorize(self):
        print("[discord_client] Performing OAuth2 authorization flow...")

        payload = {
            "cmd": "AUTHORIZE",
            "nonce": str(uuid.uuid4()),
            "args": {
                "client_id": self.client_id,
                "scopes": "rpc",
            },
        }

        self._send(1, payload)
        resp = self._decode()
        code = resp["data"]["code"]
        self.oauth2_authenticate(code)

    def oauth2_authenticate(self, code):
        print("[discord_client] Acquiring OAuth2 token...")
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": self.redirect_uri,
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        http_resp = requests.post(
            f"{API_ENDPOINT}/oauth2/token", data=data, headers=headers
        )
        http_resp.raise_for_status()

        with open(OAUTH2_CACHE_PATH, "w") as f:
            f.write(json.dumps(http_resp.json(), indent=4))

        self.access_token = http_resp.json()["access_token"]

    def oauth2_refresh(self):
        print("[discord_client] Refreshing OAuth2 token...")
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token,
            "redirect_uri": self.redirect_uri,
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        http_resp = requests.post(
            f"{API_ENDPOINT}/oauth2/token", data=data, headers=headers
        )
        print(
            f"[discord_client] Refreshing token request got {http_resp.status_code} {http_resp.text}..."
        )

        http_resp.raise_for_status()

        with open(OAUTH2_CACHE_PATH, "w") as f:
            f.write(json.dumps(http_resp.json(), indent=4))

        self.access_token = http_resp.json()["access_token"]

    def authenticate(self):
        """Authenticates with the local RPC, after OAuth2 authentication is complete"""
        print("[discord_client] Authenticating...")
        payload = {
            "cmd": "AUTHENTICATE",
            "nonce": str(uuid.uuid4()),
            "args": {
                "access_token": self.access_token,
            },
        }

        self._send(1, payload)
        resp = self._decode()["data"]

        if resp.get("code") == 4009:
            print("Access token is expired; refreshing...")
            self.oauth2_refresh()
            # NOTE(pcohen): prevent infinite looping here
            return self.authenticate()

        print("[discord_client] Authenticating succeeded!")

    def update_activity(self, activity):
        """Update User's Discord activity."""
        payload = {
            "cmd": "SET_ACTIVITY",
            "args": {"activity": activity, "pid": self.pid},
            "nonce": str(uuid.uuid4()),
        }

        self._send(1, payload)
        self._decode()

    def select_voice_channel(self, channel_id: str):
        """Select a voice channel."""
        payload = {
            "cmd": "SELECT_VOICE_CHANNEL",
            "args": {"channel_id": channel_id},
            "nonce": str(uuid.uuid4()),
        }

        self._send(1, payload)
        self._decode()

    def get_selected_voice_channel(self):
        """Get selected voice channel"""
        payload = {
            "cmd": "GET_SELECTED_VOICE_CHANNEL",
            "nonce": str(uuid.uuid4()),
        }

        self._send(1, payload)
        return self._decode()["data"]

    def get_voice_settings(self):
        """Returns the current voice settings."""
        payload = {"cmd": "GET_VOICE_SETTINGS", "nonce": str(uuid.uuid4())}

        self._send(1, payload)
        data = self._decode()["data"]
        if data.get("code"):
            raise DiscordError(
                f"Error code {data.get('code')} from Discord: {data['message']}"
            )

        return data

    def set_mute_status(self, mute: bool):
        """Sets the mute status."""
        payload = {
            "cmd": "SET_VOICE_SETTINGS",
            "nonce": str(uuid.uuid4()),
            "args": {
                "mute": mute,
            },
        }

        self._send(1, payload)
        return self._decode()["data"]["mute"]


def create_discord_client() -> DiscordClient:
    if os.path.exists(OAUTH2_CREDENTIALS_PATH):
        with open(OAUTH2_CREDENTIALS_PATH) as f:
            obj = json.load(f)
            client_id = obj["client_id"]
            client_secret = obj["client_secret"]
            redirect_uri = obj["redirect_uri"]
            return DiscordClient(client_id, client_secret, redirect_uri)

    raise DiscordError(
        f"To create a Discord client, please create a file at {OAUTH2_CREDENTIALS_PATH} with your client ID and secret."
    )


def validate_client(client: DiscordClient):
    try:
        # verify that the client is connected by reading its voice settings
        _ = client.get_voice_settings()
        return True
    except DiscordError as e:
        print(
            f"[discord_client] client is not valid: {type(e).__name__}: {e}; retrying"
        )
        return False


_client = None


def client():
    """Returns a Discord client, tries to validate that it is working"""
    global _client
    if _client is not None and validate_client(_client):
        return _client

    _client = create_discord_client()
    _client.connect()
    _client.authorize_if_needed()
    _client.authenticate()

    return _client


mod = Module()


@mod.action_class
class Actions:
    # def discord_client_reconnect():
    #     """Forces the Discord client to reconnect"""
    #     global _client
    #     _client = None
    #     return client()

    # def discord_leave_meeting():
    #     """Leaves the current meeting"""
    #     client().select_voice_channel(None)

    def discord_voice_settings() -> dict:
        """Returns the current Discord voice settings"""
        return client().get_voice_settings()

    def discord_get_mute_status() -> bool:
        """Returns the current mute status"""
        return client().get_voice_settings()["mute"]

    def discord_set_mute_status(mute: bool) -> bool:
        """Sets the Discord mute status"""
        return client().set_mute_status(mute)

    def discord_toggle_mute() -> bool:
        """Toggles the mute status on Discord"""
        c = client()
        return c.set_mute_status(
            not c.get_voice_settings()["mute"],
        )

    def discord_get_selected_voice_channel() -> Optional[dict]:
        """Gets the selected discord voice channel"""
        return client().get_selected_voice_channel()
