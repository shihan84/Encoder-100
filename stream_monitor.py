#!/usr/bin/env python3
"""
Stream Monitoring Module
Real-time monitoring and metrics collection for TSDuck GUI
"""

import time
import threading
import queue
import json
import subprocess
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass
from datetime import datetime
import logging

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False


@dataclass
class StreamStats:
    """Stream statistics data structure"""
    timestamp: datetime
    bitrate: int
    packets_per_second: int
    errors: int
    pcr_accuracy: float
    continuity_errors: int
    services_count: int
    pids_count: int
    cpu_usage: float
    memory_usage: float
    network_in: int
    network_out: int


class MetricsCollector:
    """Collect system and stream metrics"""
    
    def __init__(self):
        self.stats_history = []
        self.max_history = 1000
        self.callbacks = []
        
    def add_callback(self, callback: Callable[[StreamStats], None]):
        """Add callback for new statistics"""
        self.callbacks.append(callback)
        
    def remove_callback(self, callback: Callable[[StreamStats], None]):
        """Remove callback"""
        if callback in self.callbacks:
            self.callbacks.remove(callback)
            
    def collect_stats(self) -> StreamStats:
        """Collect current statistics"""
        stats = StreamStats(
            timestamp=datetime.now(),
            bitrate=0,
            packets_per_second=0,
            errors=0,
            pcr_accuracy=0.0,
            continuity_errors=0,
            services_count=0,
            pids_count=0,
            cpu_usage=0.0,
            memory_usage=0.0,
            network_in=0,
            network_out=0
        )
        
        # Collect system metrics
        if PSUTIL_AVAILABLE:
            stats.cpu_usage = psutil.cpu_percent()
            stats.memory_usage = psutil.virtual_memory().percent
            
            # Network statistics
            net_io = psutil.net_io_counters()
            stats.network_in = net_io.bytes_recv
            stats.network_out = net_io.bytes_sent
            
        return stats
        
    def update_stats(self, stats: StreamStats):
        """Update statistics and notify callbacks"""
        self.stats_history.append(stats)
        
        # Keep only recent history
        if len(self.stats_history) > self.max_history:
            self.stats_history = self.stats_history[-self.max_history:]
            
        # Notify callbacks
        for callback in self.callbacks:
            try:
                callback(stats)
            except Exception as e:
                logging.error(f"Error in stats callback: {e}")
                
    def get_history(self, count: int = None) -> List[StreamStats]:
        """Get statistics history"""
        if count is None:
            return self.stats_history.copy()
        return self.stats_history[-count:] if count > 0 else []


class TSDuckMonitor:
    """Monitor TSDuck process and stream"""
    
    def __init__(self):
        self.monitoring = False
        self.monitor_thread = None
        self.metrics_collector = MetricsCollector()
        self.process = None
        self.output_queue = queue.Queue()
        
    def start_monitoring(self, process: subprocess.Popen):
        """Start monitoring TSDuck process"""
        self.process = process
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
        
    def stop_monitoring(self):
        """Stop monitoring"""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=1.0)
            
    def _monitor_loop(self):
        """Main monitoring loop"""
        while self.monitoring and self.process:
            try:
                # Collect system metrics
                stats = self.metrics_collector.collect_stats()
                
                # Parse TSDuck output for stream metrics
                self._parse_tsduck_output(stats)
                
                # Update statistics
                self.metrics_collector.update_stats(stats)
                
                time.sleep(1.0)  # Update every second
                
            except Exception as e:
                logging.error(f"Error in monitoring loop: {e}")
                time.sleep(1.0)
                
    def _parse_tsduck_output(self, stats: StreamStats):
        """Parse TSDuck output for stream metrics"""
        # This would parse actual TSDuck output
        # For now, simulate some metrics
        if self.process and self.process.poll() is None:
            # Simulate stream metrics
            stats.bitrate = 15000000  # 15 Mbps
            stats.packets_per_second = 25000
            stats.pcr_accuracy = 99.9
            stats.services_count = 5
            stats.pids_count = 20


class InfluxDBExporter:
    """Export metrics to InfluxDB"""
    
    def __init__(self, host: str = "localhost", port: int = 8086, 
                 database: str = "tsduck", username: str = None, password: str = None):
        self.host = host
        self.port = port
        self.database = database
        self.username = username
        self.password = password
        self.enabled = False
        
    def enable(self):
        """Enable InfluxDB export"""
        self.enabled = True
        
    def disable(self):
        """Disable InfluxDB export"""
        self.enabled = False
        
    def export_stats(self, stats: StreamStats):
        """Export statistics to InfluxDB"""
        if not self.enabled:
            return
            
        try:
            # Create InfluxDB line protocol format
            timestamp_ns = int(stats.timestamp.timestamp() * 1000000000)
            
            lines = [
                f"stream_bitrate,host=tsduck value={stats.bitrate} {timestamp_ns}",
                f"stream_packets_per_second,host=tsduck value={stats.packets_per_second} {timestamp_ns}",
                f"stream_errors,host=tsduck value={stats.errors} {timestamp_ns}",
                f"stream_pcr_accuracy,host=tsduck value={stats.pcr_accuracy} {timestamp_ns}",
                f"stream_continuity_errors,host=tsduck value={stats.continuity_errors} {timestamp_ns}",
                f"stream_services_count,host=tsduck value={stats.services_count} {timestamp_ns}",
                f"stream_pids_count,host=tsduck value={stats.pids_count} {timestamp_ns}",
                f"system_cpu_usage,host=tsduck value={stats.cpu_usage} {timestamp_ns}",
                f"system_memory_usage,host=tsduck value={stats.memory_usage} {timestamp_ns}",
                f"network_bytes_in,host=tsduck value={stats.network_in} {timestamp_ns}",
                f"network_bytes_out,host=tsduck value={stats.network_out} {timestamp_ns}"
            ]
            
            # Send to InfluxDB (simplified - would use proper InfluxDB client)
            self._send_to_influxdb('\n'.join(lines))
            
        except Exception as e:
            logging.error(f"Error exporting to InfluxDB: {e}")
            
    def _send_to_influxdb(self, data: str):
        """Send data to InfluxDB"""
        # This would use a proper InfluxDB client
        # For now, just log the data
        logging.info(f"InfluxDB data: {data}")


class GrafanaDashboard:
    """Generate Grafana dashboard configuration"""
    
    @staticmethod
    def generate_dashboard() -> Dict[str, Any]:
        """Generate Grafana dashboard configuration"""
        return {
            "dashboard": {
                "id": None,
                "title": "TSDuck Stream Monitoring",
                "tags": ["tsduck", "streaming"],
                "timezone": "browser",
                "panels": [
                    {
                        "id": 1,
                        "title": "Stream Bitrate",
                        "type": "graph",
                        "targets": [
                            {
                                "expr": "stream_bitrate",
                                "legendFormat": "Bitrate (bps)"
                            }
                        ],
                        "yAxes": [
                            {
                                "label": "Bitrate (bps)",
                                "min": 0
                            }
                        ],
                        "gridPos": {"h": 8, "w": 12, "x": 0, "y": 0}
                    },
                    {
                        "id": 2,
                        "title": "Packets per Second",
                        "type": "graph",
                        "targets": [
                            {
                                "expr": "stream_packets_per_second",
                                "legendFormat": "Packets/sec"
                            }
                        ],
                        "yAxes": [
                            {
                                "label": "Packets/sec",
                                "min": 0
                            }
                        ],
                        "gridPos": {"h": 8, "w": 12, "x": 12, "y": 0}
                    },
                    {
                        "id": 3,
                        "title": "System Resources",
                        "type": "graph",
                        "targets": [
                            {
                                "expr": "system_cpu_usage",
                                "legendFormat": "CPU Usage (%)"
                            },
                            {
                                "expr": "system_memory_usage",
                                "legendFormat": "Memory Usage (%)"
                            }
                        ],
                        "yAxes": [
                            {
                                "label": "Usage (%)",
                                "min": 0,
                                "max": 100
                            }
                        ],
                        "gridPos": {"h": 8, "w": 24, "x": 0, "y": 8}
                    },
                    {
                        "id": 4,
                        "title": "Stream Errors",
                        "type": "graph",
                        "targets": [
                            {
                                "expr": "stream_errors",
                                "legendFormat": "Errors"
                            },
                            {
                                "expr": "stream_continuity_errors",
                                "legendFormat": "Continuity Errors"
                            }
                        ],
                        "yAxes": [
                            {
                                "label": "Error Count",
                                "min": 0
                            }
                        ],
                        "gridPos": {"h": 8, "w": 12, "x": 0, "y": 16}
                    },
                    {
                        "id": 5,
                        "title": "PCR Accuracy",
                        "type": "graph",
                        "targets": [
                            {
                                "expr": "stream_pcr_accuracy",
                                "legendFormat": "PCR Accuracy (%)"
                            }
                        ],
                        "yAxes": [
                            {
                                "label": "Accuracy (%)",
                                "min": 0,
                                "max": 100
                            }
                        ],
                        "gridPos": {"h": 8, "w": 12, "x": 12, "y": 16}
                    }
                ],
                "time": {
                    "from": "now-1h",
                    "to": "now"
                },
                "refresh": "5s"
            }
        }


class AlertManager:
    """Manage alerts and notifications"""
    
    def __init__(self):
        self.alerts = []
        self.alert_callbacks = []
        
    def add_alert(self, name: str, condition: Callable[[StreamStats], bool], 
                  message: str, severity: str = "warning"):
        """Add an alert"""
        alert = {
            'name': name,
            'condition': condition,
            'message': message,
            'severity': severity,
            'triggered': False,
            'last_triggered': None
        }
        self.alerts.append(alert)
        
    def add_alert_callback(self, callback: Callable[[Dict[str, Any]], None]):
        """Add callback for alerts"""
        self.alert_callbacks.append(callback)
        
    def check_alerts(self, stats: StreamStats):
        """Check all alerts against current statistics"""
        for alert in self.alerts:
            try:
                if alert['condition'](stats):
                    if not alert['triggered']:
                        alert['triggered'] = True
                        alert['last_triggered'] = stats.timestamp
                        self._trigger_alert(alert, stats)
                else:
                    if alert['triggered']:
                        alert['triggered'] = False
                        self._clear_alert(alert, stats)
            except Exception as e:
                logging.error(f"Error checking alert {alert['name']}: {e}")
                
    def _trigger_alert(self, alert: Dict[str, Any], stats: StreamStats):
        """Trigger an alert"""
        alert_data = {
            'name': alert['name'],
            'message': alert['message'],
            'severity': alert['severity'],
            'timestamp': stats.timestamp,
            'stats': stats
        }
        
        for callback in self.alert_callbacks:
            try:
                callback(alert_data)
            except Exception as e:
                logging.error(f"Error in alert callback: {e}")
                
    def _clear_alert(self, alert: Dict[str, Any], stats: StreamStats):
        """Clear an alert"""
        alert_data = {
            'name': alert['name'],
            'message': f"{alert['name']} cleared",
            'severity': 'info',
            'timestamp': stats.timestamp,
            'stats': stats
        }
        
        for callback in self.alert_callbacks:
            try:
                callback(alert_data)
            except Exception as e:
                logging.error(f"Error in alert clear callback: {e}")


# Predefined alert conditions
class AlertConditions:
    """Predefined alert conditions"""
    
    @staticmethod
    def high_bitrate(threshold: int = 20000000):
        """High bitrate alert"""
        return lambda stats: stats.bitrate > threshold
        
    @staticmethod
    def low_bitrate(threshold: int = 1000000):
        """Low bitrate alert"""
        return lambda stats: stats.bitrate < threshold
        
    @staticmethod
    def high_error_rate(threshold: int = 100):
        """High error rate alert"""
        return lambda stats: stats.errors > threshold
        
    @staticmethod
    def low_pcr_accuracy(threshold: float = 95.0):
        """Low PCR accuracy alert"""
        return lambda stats: stats.pcr_accuracy < threshold
        
    @staticmethod
    def high_cpu_usage(threshold: float = 80.0):
        """High CPU usage alert"""
        return lambda stats: stats.cpu_usage > threshold
        
    @staticmethod
    def high_memory_usage(threshold: float = 80.0):
        """High memory usage alert"""
        return lambda stats: stats.memory_usage > threshold


# Example usage
if __name__ == "__main__":
    # Create monitor
    monitor = TSDuckMonitor()
    
    # Create alert manager
    alert_manager = AlertManager()
    
    # Add alerts
    alert_manager.add_alert(
        "High Bitrate",
        AlertConditions.high_bitrate(20000000),
        "Stream bitrate is above 20 Mbps",
        "warning"
    )
    
    alert_manager.add_alert(
        "Low PCR Accuracy",
        AlertConditions.low_pcr_accuracy(95.0),
        "PCR accuracy is below 95%",
        "critical"
    )
    
    # Add alert callback
    def alert_callback(alert_data):
        print(f"ALERT: {alert_data['severity'].upper()} - {alert_data['message']}")
        
    alert_manager.add_alert_callback(alert_callback)
    
    # Add metrics callback
    def stats_callback(stats):
        print(f"Stats: Bitrate={stats.bitrate}, CPU={stats.cpu_usage}%")
        alert_manager.check_alerts(stats)
        
    monitor.metrics_collector.add_callback(stats_callback)
    
    # Generate Grafana dashboard
    dashboard = GrafanaDashboard.generate_dashboard()
    print("Grafana dashboard generated")
