"""Pydantic models for input and output validation."""

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class Protocol(str, Enum):
    """Network connection protocol."""

    SSH = "ssh"
    TELNET = "telnet"


class Credentials(BaseModel):
    """User credentials for device authentication."""

    username: str = Field(..., min_length=1, description="Username for authentication")
    password: str = Field(..., min_length=1, description="Password for authentication")
    enable: str = Field(..., min_length=1, description="Enable password for privileged mode")


class DeviceSettings(BaseModel):
    """Settings for connecting to and configuring a network device."""

    device_name: str = Field(..., min_length=1, description="Hostname or IP address of device")
    protocol: Protocol = Field(default=Protocol.SSH, description="Connection protocol")
    username: str = Field(..., min_length=1, description="Username for authentication")
    password: str = Field(..., min_length=1, description="Password for authentication")
    enable_password: str = Field(..., min_length=1, description="Enable password")
    delay: int = Field(default=2, ge=0, description="Delay between commands in seconds")
    buffer: int = Field(default=8192, ge=1024, description="SSH buffer size")
    commands: list[str] = Field(default_factory=list, description="Commands to execute")
    command_output: bool = Field(default=False, description="Show command output")

    @field_validator("device_name")
    @classmethod
    def validate_device_name(cls, v: str) -> str:
        """Validate device name is not empty after stripping."""
        if not v.strip():
            raise ValueError("Device name cannot be empty")
        return v.strip()


class Arguments(BaseModel):
    """Command-line arguments for the application."""

    username: str = Field(..., min_length=1, description="Username for authentication")
    delete_creds: Optional[bool] = Field(
        default=None, description="Delete credentials from keyring"
    )
    set_creds: Optional[bool] = Field(default=None, description="Set keyring credentials")
    devices: Optional[str] = Field(default=None, description="Path to hosts file")
    commands: Optional[str] = Field(default=None, description="Path to commands file")
    ssh: Optional[str] = Field(default=None, description="Use SSH protocol")
    telnet: Optional[str] = Field(default=None, description="Use Telnet protocol")
    output: Optional[bool] = Field(default=None, description="Verbose command output")
    verbose: Optional[bool] = Field(default=None, description="Debug script output")
    delay: str = Field(default="2", description="Delay between commands")
    buffer: str = Field(default="8192", description="SSH buffer size")
    threaded: Optional[bool] = Field(default=None, description="Enable threading")
    maxthreads: str = Field(default="10", description="Maximum number of threads")
    protocol: Protocol = Field(default=Protocol.SSH, description="Connection protocol")
