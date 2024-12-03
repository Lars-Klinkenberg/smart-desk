import subprocess
import logging


def is_service_active(service_name):
    logger = logging.getLogger(__name__)

    try:
        # Run the systemctl command to check if the service is active
        result = subprocess.run(
            ["systemctl", "is-active", service_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        # Check the output; 'active' indicates the service is running
        return result.stdout.strip() == "active"

    except Exception:
        logger.exception(f"Failed to load service ({service_name}) status")
        return False
