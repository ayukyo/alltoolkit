#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AllToolkit - System Monitoring Utilities Module

Comprehensive system monitoring utilities for Python with zero external dependencies.
Provides CPU, memory, disk, network, and process monitoring by reading /proc filesystem.

Author: AllToolkit
License: MIT
Version: 1.0.0
"""

import os
import time
import socket
import subprocess
import re
from typing import Optional, Dict, Any, List, Tuple, NamedTuple
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path


# =============================================================================
# Type Aliases
# =============================================================================

ProcessInfo = Dict[str, Any]
DiskUsage = Dict[str, Any]
NetworkStats = Dict[str, Any]
SystemInfo = Dict[str, Any]


# =============================================================================
# Constants
# =============================================================================

PROC_PATH = Path("/proc")
DEFAULT_ENCODING = "utf-8"
BYTES_IN_KB = 1024
BYTES_IN_MB = 1024 * 1024
BYTES_IN_GB = 1024 * 1024 * 1024


# =============================================================================
# Data Classes
# =============================================================================

@dataclass
class CPUStats:
    """CPU statistics."""
    user: float = 0.0
    system: float = 0.0
    idle: float = 0.0
    iowait: float = 0.0
    irq: float = 0.0
    softirq: float = 0.0
    steal: float = 0.0
    guest: float = 0.0
    usage_percent: float = 0.0
    cores: int = 1
    load_avg: Tuple[float, float, float] = (0.0, 0.0, 0.0)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "user": self.user,
            "system": self.system,
            "idle": self.idle,
            "iowait": self.iowait,
            "irq": self.irq,
            "softirq": self.softirq,
            "steal": self.steal,
            "guest": self.guest,
            "usage_percent": self.usage_percent,
            "cores": self.cores,
            "load_avg": list(self.load_avg)
        }


@dataclass
class MemoryStats:
    """Memory statistics."""
    total: int = 0
    available: int = 0
    used: int = 0
    free: int = 0
    buffers: int = 0
    cached: int = 0
    swap_total: int = 0
    swap_free: int = 0
    swap_used: int = 0
    usage_percent: float = 0.0
    swap_percent: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "total": self.total,
            "available": self.available,
            "used": self.used,
            "free": self.free,
            "buffers": self.buffers,
            "cached": self.cached,
            "swap_total": self.swap_total,
            "swap_free": self.swap_free,
            "swap_used": self.swap_used,
            "usage_percent": self.usage_percent,
            "swap_percent": self.swap_percent
        }
    
    @property
    def total_gb(self) -> float:
        """Total memory in GB."""
        return self.total / BYTES_IN_GB
    
    @property
    def available_gb(self) -> float:
        """Available memory in GB."""
        return self.available / BYTES_IN_GB
    
    @property
    def used_gb(self) -> float:
        """Used memory in GB."""
        return self.used / BYTES_IN_GB


@dataclass
class DiskStats:
    """Disk I/O statistics."""
    reads: int = 0
    writes: int = 0
    read_bytes: int = 0
    write_bytes: int = 0
    read_time: int = 0
    write_time: int = 0
    io_time: int = 0
    weighted_io_time: int = 0


@dataclass
class NetworkInterfaceStats:
    """Network interface statistics."""
    name: str = ""
    rx_bytes: int = 0
    rx_packets: int = 0
    rx_errors: int = 0
    rx_dropped: int = 0
    tx_bytes: int = 0
    tx_packets: int = 0
    tx_errors: int = 0
    tx_dropped: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "rx_bytes": self.rx_bytes,
            "rx_packets": self.rx_packets,
            "rx_errors": self.rx_errors,
            "rx_dropped": self.rx_dropped,
            "tx_bytes": self.tx_bytes,
            "tx_packets": self.tx_packets,
            "tx_errors": self.tx_errors,
            "tx_dropped": self.tx_dropped
        }


@dataclass
class ProcessStats:
    """Process statistics."""
    pid: int = 0
    name: str = ""
    status: str = ""
    ppid: int = 0
    uid: int = 0
    cpu_percent: float = 0.0
    memory_percent: float = 0.0
    memory_rss: int = 0
    memory_vms: int = 0
    num_threads: int = 0
    create_time: float = 0.0
    cmdline: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "pid": self.pid,
            "name": self.name,
            "status": self.status,
            "ppid": self.ppid,
            "uid": self.uid,
            "cpu_percent": self.cpu_percent,
            "memory_percent": self.memory_percent,
            "memory_rss": self.memory_rss,
            "memory_vms": self.memory_vms,
            "num_threads": self.num_threads,
            "create_time": self.create_time,
            "cmdline": self.cmdline
        }


@dataclass
class SystemMonitor:
    """Main system monitoring class."""
    _prev_cpu_times: Optional[Tuple[int, ...]] = None
    _prev_cpu_time: Optional[float] = None
    
    def get_cpu_stats(self) -> CPUStats:
        """Get CPU statistics."""
        stats = CPUStats()
        
        # Get number of cores
        stats.cores = os.cpu_count() or 1
        
        # Read load average
        try:
            with open("/proc/loadavg", "r") as f:
                load = f.read().split()
                stats.load_avg = (float(load[0]), float(load[1]), float(load[2]))
        except (FileNotFoundError, IOError, IndexError):
            pass
        
        # Read CPU times from /proc/stat
        try:
            with open("/proc/stat", "r") as f:
                for line in f:
                    if line.startswith("cpu "):
                        parts = line.split()
                        if len(parts) >= 8:
                            user = int(parts[1])
                            nice = int(parts[2])
                            system = int(parts[3])
                            idle = int(parts[4])
                            iowait = int(parts[5])
                            irq = int(parts[6])
                            softirq = int(parts[7])
                            steal = int(parts[8]) if len(parts) > 8 else 0
                            guest = int(parts[9]) if len(parts) > 9 else 0
                            
                            stats.user = user + nice
                            stats.system = system + irq + softirq
                            stats.idle = idle
                            stats.iowait = iowait
                            stats.irq = irq
                            stats.softirq = softirq
                            stats.steal = steal
                            stats.guest = guest
                            
                            # Calculate usage percentage
                            total = stats.user + stats.system + stats.idle + stats.iowait + stats.steal
                            if total > 0:
                                stats.usage_percent = ((total - stats.idle - stats.iowait) / total) * 100
                        break
        except (FileNotFoundError, IOError):
            pass
        
        return stats
    
    def get_cpu_stats_percent(self, interval: float = 1.0) -> CPUStats:
        """Get CPU usage percentage over an interval."""
        # First reading
        cpu1 = self._read_cpu_times()
        time.sleep(interval)
        # Second reading
        cpu2 = self._read_cpu_times()
        
        stats = CPUStats()
        stats.cores = os.cpu_count() or 1
        
        # Read load average
        try:
            with open("/proc/loadavg", "r") as f:
                load = f.read().split()
                stats.load_avg = (float(load[0]), float(load[1]), float(load[2]))
        except (FileNotFoundError, IOError, IndexError):
            pass
        
        # Calculate differences
        if cpu1 and cpu2:
            user_diff = cpu2[0] - cpu1[0]
            system_diff = cpu2[1] - cpu1[1]
            idle_diff = cpu2[2] - cpu1[2]
            iowait_diff = cpu2[3] - cpu1[3]
            
            total_diff = user_diff + system_diff + idle_diff + iowait_diff
            
            if total_diff > 0:
                stats.user = (user_diff / total_diff) * 100
                stats.system = (system_diff / total_diff) * 100
                stats.idle = (idle_diff / total_diff) * 100
                stats.iowait = (iowait_diff / total_diff) * 100
                stats.usage_percent = stats.user + stats.system
        
        return stats
    
    def _read_cpu_times(self) -> Optional[Tuple[int, ...]]:
        """Read raw CPU times."""
        try:
            with open("/proc/stat", "r") as f:
                for line in f:
                    if line.startswith("cpu "):
                        parts = line.split()
                        user = int(parts[1])
                        nice = int(parts[2])
                        system = int(parts[3])
                        idle = int(parts[4])
                        iowait = int(parts[5]) if len(parts) > 5 else 0
                        return (user + nice, system, idle, iowait)
        except (FileNotFoundError, IOError, IndexError):
            pass
        return None
    
    def get_memory_stats(self) -> MemoryStats:
        """Get memory statistics."""
        stats = MemoryStats()
        
        try:
            with open("/proc/meminfo", "r") as f:
                meminfo = {}
                for line in f:
                    parts = line.split(":")
                    if len(parts) == 2:
                        key = parts[0].strip()
                        value_parts = parts[1].strip().split()
                        # Convert from kB to bytes
                        value = int(value_parts[0]) * BYTES_IN_KB
                        meminfo[key] = value
                
                stats.total = meminfo.get("MemTotal", 0)
                stats.free = meminfo.get("MemFree", 0)
                stats.available = meminfo.get("MemAvailable", stats.free)
                stats.buffers = meminfo.get("Buffers", 0)
                stats.cached = meminfo.get("Cached", 0)
                stats.used = stats.total - stats.available
                
                stats.swap_total = meminfo.get("SwapTotal", 0)
                stats.swap_free = meminfo.get("SwapFree", 0)
                stats.swap_used = stats.swap_total - stats.swap_free
                
                # Calculate percentages
                if stats.total > 0:
                    stats.usage_percent = (stats.used / stats.total) * 100
                if stats.swap_total > 0:
                    stats.swap_percent = (stats.swap_used / stats.swap_total) * 100
        except (FileNotFoundError, IOError):
            pass
        
        return stats
    
    def get_disk_usage(self, path: str = "/") -> Dict[str, Any]:
        """Get disk usage for a path."""
        try:
            stat = os.statvfs(path)
            total = stat.f_blocks * stat.f_frsize
            free = stat.f_bfree * stat.f_frsize
            available = stat.f_bavail * stat.f_frsize
            used = total - free
            
            return {
                "path": path,
                "total": total,
                "free": free,
                "available": available,
                "used": used,
                "usage_percent": (used / total * 100) if total > 0 else 0,
                "total_gb": total / BYTES_IN_GB,
                "free_gb": free / BYTES_IN_GB,
                "available_gb": available / BYTES_IN_GB,
                "used_gb": used / BYTES_IN_GB
            }
        except (FileNotFoundError, IOError, OSError):
            return {"path": path, "error": "Unable to get disk usage"}
    
    def get_disk_io_stats(self, device: str = "sda") -> DiskStats:
        """Get disk I/O statistics for a device."""
        stats = DiskStats()
        
        try:
            with open("/proc/diskstats", "r") as f:
                for line in f:
                    parts = line.split()
                    if len(parts) >= 14 and parts[2] == device:
                        stats.reads = int(parts[3])
                        stats.read_bytes = int(parts[5]) * 512  # sectors to bytes
                        stats.writes = int(parts[7])
                        stats.write_bytes = int(parts[9]) * 512
                        stats.read_time = int(parts[6])
                        stats.write_time = int(parts[10])
                        stats.io_time = int(parts[12])
                        stats.weighted_io_time = int(parts[13])
                        break
        except (FileNotFoundError, IOError):
            pass
        
        return stats
    
    def get_network_stats(self) -> List[NetworkInterfaceStats]:
        """Get network interface statistics."""
        interfaces = []
        
        try:
            with open("/proc/net/dev", "r") as f:
                for line in f:
                    # Skip header lines
                    if ":" not in line:
                        continue
                    
                    parts = line.split(":")
                    if len(parts) != 2:
                        continue
                    
                    name = parts[0].strip()
                    values = parts[1].split()
                    
                    if len(values) >= 16:
                        stats = NetworkInterfaceStats(
                            name=name,
                            rx_bytes=int(values[0]),
                            rx_packets=int(values[1]),
                            rx_errors=int(values[2]),
                            rx_dropped=int(values[3]),
                            tx_bytes=int(values[8]),
                            tx_packets=int(values[9]),
                            tx_errors=int(values[10]),
                            tx_dropped=int(values[11])
                        )
                        interfaces.append(stats)
        except (FileNotFoundError, IOError):
            pass
        
        return interfaces
    
    def get_process_list(self) -> List[ProcessStats]:
        """Get list of all processes."""
        processes = []
        total_memory = self.get_memory_stats().total or 1
        
        try:
            for pid_dir in PROC_PATH.iterdir():
                if not pid_dir.is_dir():
                    continue
                
                try:
                    pid = int(pid_dir.name)
                except ValueError:
                    continue
                
                process = self.get_process_info(pid, total_memory)
                if process:
                    processes.append(process)
        except (FileNotFoundError, IOError, PermissionError):
            pass
        
        return processes
    
    def get_process_info(self, pid: int, total_memory: int = 0) -> Optional[ProcessStats]:
        """Get information about a specific process."""
        proc_path = PROC_PATH / str(pid)
        
        if not proc_path.exists():
            return None
        
        stats = ProcessStats(pid=pid)
        
        try:
            # Read process name and status
            with open(proc_path / "stat", "r") as f:
                stat_content = f.read()
                # Handle process names with spaces/parentheses
                match = re.search(r'\((.+)\)\s+(.+)', stat_content)
                if match:
                    stats.name = match.group(1)
                    stat_parts = match.group(2).split()
                    if len(stat_parts) >= 20:
                        stats.status = stat_parts[0]  # R, S, D, Z, etc.
                        stats.ppid = int(stat_parts[1])
                        stats.uid = int(stat_parts[3]) if len(stat_parts) > 3 else 0
                        stats.num_threads = int(stat_parts[17]) if len(stat_parts) > 17 else 0
                        stats.create_time = float(stat_parts[19]) if len(stat_parts) > 19 else 0
                        utime = int(stat_parts[11]) if len(stat_parts) > 11 else 0
                        stime = int(stat_parts[12]) if len(stat_parts) > 12 else 0
                        # Simple CPU estimate (not accurate without delta)
                        stats.cpu_percent = (utime + stime) / 100.0
                
            # Read memory info
            with open(proc_path / "status", "r") as f:
                for line in f:
                    if line.startswith("VmRSS:"):
                        parts = line.split()
                        stats.memory_rss = int(parts[1]) * BYTES_IN_KB
                    elif line.startswith("VmSize:"):
                        parts = line.split()
                        stats.memory_vms = int(parts[1]) * BYTES_IN_KB
            
            # Calculate memory percentage
            if total_memory > 0:
                stats.memory_percent = (stats.memory_rss / total_memory) * 100
            
            # Read command line
            try:
                with open(proc_path / "cmdline", "r") as f:
                    stats.cmdline = f.read().replace("\x00", " ").strip()
            except (FileNotFoundError, IOError):
                stats.cmdline = stats.name
            
        except (FileNotFoundError, IOError, PermissionError, IndexError):
            return None
        
        return stats
    
    def get_hostname(self) -> str:
        """Get system hostname."""
        try:
            return socket.gethostname()
        except Exception:
            return "unknown"
    
    def get_boot_time(self) -> Optional[float]:
        """Get system boot time as timestamp."""
        try:
            with open("/proc/stat", "r") as f:
                for line in f:
                    if line.startswith("btime"):
                        return float(line.split()[1])
        except (FileNotFoundError, IOError, IndexError):
            pass
        return None
    
    def get_uptime(self) -> float:
        """Get system uptime in seconds."""
        try:
            with open("/proc/uptime", "r") as f:
                return float(f.read().split()[0])
        except (FileNotFoundError, IOError, ValueError):
            return 0.0
    
    def get_system_info(self) -> SystemInfo:
        """Get comprehensive system information."""
        uname = os.uname() if hasattr(os, 'uname') else None
        
        info: SystemInfo = {
            "hostname": self.get_hostname(),
            "platform": uname.sysname if uname else "unknown",
            "release": uname.release if uname else "unknown",
            "version": uname.version if uname else "unknown",
            "machine": uname.machine if uname else "unknown",
            "processor": getattr(uname, 'processor', 'unknown') if uname else "unknown",
            "cpu_count": os.cpu_count() or 1,
            "boot_time": self.get_boot_time(),
            "uptime": self.get_uptime(),
            "python_version": f"{os.sys.version_info.major}.{os.sys.version_info.minor}.{os.sys.version_info.micro}",
            "timestamp": datetime.now().isoformat()
        }
        
        # Add memory info
        mem = self.get_memory_stats()
        info["memory_total"] = mem.total
        info["memory_available"] = mem.available
        
        # Add disk info for root
        disk = self.get_disk_usage("/")
        info["disk_total"] = disk.get("total", 0)
        info["disk_available"] = disk.get("available", 0)
        
        return info
    
    def get_top_processes(self, n: int = 10, by: str = "cpu") -> List[ProcessStats]:
        """Get top N processes by CPU or memory usage."""
        processes = self.get_process_list()
        
        if by.lower() == "memory":
            processes.sort(key=lambda p: p.memory_percent, reverse=True)
        else:
            processes.sort(key=lambda p: p.cpu_percent, reverse=True)
        
        return processes[:n]
    
    def get_all_stats(self) -> Dict[str, Any]:
        """Get all system statistics in one call."""
        return {
            "system": self.get_system_info(),
            "cpu": self.get_cpu_stats().to_dict(),
            "memory": self.get_memory_stats().to_dict(),
            "disk": self.get_disk_usage("/"),
            "network": [iface.to_dict() for iface in self.get_network_stats()],
            "top_cpu_processes": [p.to_dict() for p in self.get_top_processes(5, "cpu")],
            "top_memory_processes": [p.to_dict() for p in self.get_top_processes(5, "memory")],
            "timestamp": datetime.now().isoformat()
        }


# =============================================================================
# Convenience Functions
# =============================================================================

_monitor = SystemMonitor()


def get_cpu_stats() -> CPUStats:
    """Get CPU statistics."""
    return _monitor.get_cpu_stats()


def get_cpu_stats_percent(interval: float = 1.0) -> CPUStats:
    """Get CPU usage percentage over an interval."""
    return _monitor.get_cpu_stats_percent(interval)


def get_memory_stats() -> MemoryStats:
    """Get memory statistics."""
    return _monitor.get_memory_stats()


def get_disk_usage(path: str = "/") -> Dict[str, Any]:
    """Get disk usage for a path."""
    return _monitor.get_disk_usage(path)


def get_disk_io_stats(device: str = "sda") -> DiskStats:
    """Get disk I/O statistics for a device."""
    return _monitor.get_disk_io_stats(device)


def get_network_stats() -> List[NetworkInterfaceStats]:
    """Get network interface statistics."""
    return _monitor.get_network_stats()


def get_process_list() -> List[ProcessStats]:
    """Get list of all processes."""
    return _monitor.get_process_list()


def get_process_info(pid: int) -> Optional[ProcessStats]:
    """Get information about a specific process."""
    return _monitor.get_process_info(pid)


def get_top_processes(n: int = 10, by: str = "cpu") -> List[ProcessStats]:
    """Get top N processes by CPU or memory usage."""
    return _monitor.get_top_processes(n, by)


def get_system_info() -> SystemInfo:
    """Get comprehensive system information."""
    return _monitor.get_system_info()


def get_all_stats() -> Dict[str, Any]:
    """Get all system statistics in one call."""
    return _monitor.get_all_stats()


def get_uptime() -> float:
    """Get system uptime in seconds."""
    return _monitor.get_uptime()


def get_hostname() -> str:
    """Get system hostname."""
    return _monitor.get_hostname()


# =============================================================================
# Module Info
# =============================================================================

__version__ = "1.0.0"
__author__ = "AllToolkit"
__license__ = "MIT"

version = "1.0.0"

features = [
    "CPU monitoring (usage, load average, cores)",
    "Memory monitoring (RAM, swap, percentages)",
    "Disk monitoring (usage, I/O statistics)",
    "Network monitoring (interface statistics)",
    "Process monitoring (list, details, top N)",
    "System information (hostname, uptime, boot time)",
    "Zero external dependencies",
    "Linux /proc filesystem based",
    "Type-annotated",
    "Production ready"
]


# =============================================================================
# CLI Entry Point
# =============================================================================

if __name__ == "__main__":
    import json
    
    print("=" * 60)
    print("AllToolkit System Monitoring Utils")
    print("=" * 60)
    
    monitor = SystemMonitor()
    
    # System Info
    print("\n📊 System Information:")
    info = monitor.get_system_info()
    print(f"  Hostname: {info.get('hostname', 'N/A')}")
    print(f"  Platform: {info.get('platform', 'N/A')} {info.get('release', 'N/A')}")
    print(f"  CPU Cores: {info.get('cpu_count', 'N/A')}")
    uptime = monitor.get_uptime()
    hours, remainder = divmod(int(uptime), 3600)
    minutes, seconds = divmod(remainder, 60)
    print(f"  Uptime: {hours}h {minutes}m {seconds}s")
    
    # CPU Stats
    print("\n🔌 CPU Statistics:")
    cpu = monitor.get_cpu_stats()
    print(f"  Usage: {cpu.usage_percent:.1f}%")
    print(f"  Load Average: {cpu.load_avg}")
    print(f"  Cores: {cpu.cores}")
    
    # Memory Stats
    print("\n💾 Memory Statistics:")
    mem = monitor.get_memory_stats()
    print(f"  Total: {mem.total_gb:.2f} GB")
    print(f"  Used: {mem.used_gb:.2f} GB ({mem.usage_percent:.1f}%)")
    print(f"  Available: {mem.available_gb:.2f} GB")
    if mem.swap_total > 0:
        print(f"  Swap: {mem.swap_percent:.1f}% used")
    
    # Disk Usage
    print("\n💿 Disk Usage (/):")
    disk = monitor.get_disk_usage("/")
    print(f"  Total: {disk.get('total_gb', 0):.2f} GB")
    print(f"  Used: {disk.get('used_gb', 0):.2f} GB ({disk.get('usage_percent', 0):.1f}%)")
    print(f"  Available: {disk.get('available_gb', 0):.2f} GB")
    
    # Network Stats
    print("\n🌐 Network Interfaces:")
    for iface in monitor.get_network_stats():
        if iface.name != "lo":  # Skip loopback
            print(f"  {iface.name}:")
            print(f"    RX: {iface.rx_bytes / BYTES_IN_MB:.2f} MB")
            print(f"    TX: {iface.tx_bytes / BYTES_IN_MB:.2f} MB")
    
    # Top Processes
    print("\n📈 Top 5 CPU Processes:")
    for i, proc in enumerate(monitor.get_top_processes(5, "cpu"), 1):
        print(f"  {i}. {proc.name} (PID: {proc.pid}) - CPU: {proc.cpu_percent:.1f}%")
    
    print("\n📈 Top 5 Memory Processes:")
    for i, proc in enumerate(monitor.get_top_processes(5, "memory"), 1):
        print(f"  {i}. {proc.name} (PID: {proc.pid}) - Mem: {proc.memory_percent:.2f}%")
    
    print("\n" + "=" * 60)
    print(f"Generated at: {datetime.now().isoformat()}")
    print("=" * 60)
