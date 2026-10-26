from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator


def preparer_donnees():
    print("Preparation des donnees...")
    return "donnees pretes"


def entrainer_modele():
    import torch  # import dans la fonction : chargement du DAG plus rapide

    device = "cuda" if torch.cuda.is_available() else "cpu"
    print("Device utilise :", device)
    if device == "cuda":
        print("GPU :", torch.cuda.get_device_name(0))

    # Mini entrainement de test
    model = torch.nn.Linear(10, 1).to(device)
    optimizer = torch.optim.SGD(model.parameters(), lr=0.01)
    x = torch.randn(256, 10, device=device)
    y = torch.randn(256, 1, device=device)

    for epoch in range(5):
        loss = torch.nn.functional.mse_loss(model(x), y)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        print(f"epoch {epoch} - loss {loss.item():.4f}")


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