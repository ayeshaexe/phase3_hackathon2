"""
Performance monitoring utilities for AI response times
"""
import time
from datetime import datetime
import json
import logging
from typing import Callable, Any
from functools import wraps


class PerformanceMonitor:
    """
    Class to monitor performance metrics for AI interactions
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.metrics_log = []

    def measure_response_time(self, func: Callable) -> Callable:
        """
        Decorator to measure the response time of a function
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()

            try:
                result = func(*args, **kwargs)
                end_time = time.time()

                response_time = end_time - start_time

                # Log the performance metric
                metric = {
                    "function": func.__name__,
                    "response_time_seconds": response_time,
                    "timestamp": datetime.now().isoformat(),
                    "status": "success"
                }

                self.metrics_log.append(metric)
                self.logger.info(f"Performance metric: {json.dumps(metric)}")

                return result
            except Exception as e:
                end_time = time.time()
                response_time = end_time - start_time

                # Log the error with performance metric
                metric = {
                    "function": func.__name__,
                    "response_time_seconds": response_time,
                    "timestamp": datetime.now().isoformat(),
                    "status": "error",
                    "error": str(e)
                }

                self.metrics_log.append(metric)
                self.logger.error(f"Performance metric (error): {json.dumps(metric)}")

                raise

        return wrapper

    def get_performance_summary(self) -> dict:
        """
        Get a summary of performance metrics
        """
        if not self.metrics_log:
            return {
                "total_requests": 0,
                "average_response_time": 0,
                "min_response_time": 0,
                "max_response_time": 0,
                "error_count": 0
            }

        response_times = [
            metric["response_time_seconds"]
            for metric in self.metrics_log
            if metric["status"] == "success"
        ]

        error_count = sum(
            1 for metric in self.metrics_log
            if metric["status"] == "error"
        )

        if response_times:
            avg_time = sum(response_times) / len(response_times)
            min_time = min(response_times)
            max_time = max(response_times)
        else:
            avg_time = 0
            min_time = 0
            max_time = 0

        return {
            "total_requests": len(self.metrics_log),
            "average_response_time": avg_time,
            "min_response_time": min_time,
            "max_response_time": max_time,
            "error_count": error_count,
            "success_rate": (len(response_times) / len(self.metrics_log)) * 100 if self.metrics_log else 0
        }

    def log_ai_response_time(self, user_id: str, conversation_id: int, response_time: float):
        """
        Log specific AI response time
        """
        metric = {
            "component": "ai_agent",
            "user_id": user_id,
            "conversation_id": conversation_id,
            "response_time_seconds": response_time,
            "timestamp": datetime.now().isoformat()
        }

        self.metrics_log.append(metric)
        self.logger.info(f"AI Response Time: {json.dumps(metric)}")


# Global performance monitor instance
performance_monitor = PerformanceMonitor()