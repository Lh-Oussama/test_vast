from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator


def preparer_donnees():
    print("Preparation des donnees...")
    return "donnees pretes"


def entrainer_modele():
    print("Entrainement du modele...")
    try:
        import torch
        print("GPU disponible :", torch.cuda.is_available())
    except ImportError:
        print("PyTorch non installe, entrainement simule.")


def evaluer_modele():
    print("Evaluation du modele...")


with DAG(
    dag_id="mon_premier_dag",
    start_date=datetime(2026, 1, 1),
    schedule=None,  # lancement manuel
    catchup=False,
    tags=["vast", "test"],
) as dag:

    verifier_gpu = BashOperator(
        task_id="verifier_gpu",
        bash_command="nvidia-smi || echo 'Pas de GPU detecte'",
    )

    preparer = PythonOperator(task_id="preparer_donnees", python_callable=preparer_donnees)
    entrainer = PythonOperator(task_id="entrainer_modele", python_callable=entrainer_modele)
    evaluer = PythonOperator(task_id="evaluer_modele", python_callable=evaluer_modele)

    verifier_gpu >> preparer >> entrainer >> evaluer