import logging
import os

# Création du dossier logs s'il n'existe pas
log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "logs")
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Configuration du logger
logging.basicConfig(
    filename=os.path.join(log_dir, "service.log"),  # Fichier de logs
    level=logging.INFO,  # Niveau des logs
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)

logger.info("Logger configuré avec succès !")
