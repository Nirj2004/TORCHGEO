import itertools
import os
import subprocess
from multiprocessing import Process, Queue
GPUS = [0]
DRY_RUN = False
DATA_DIR = ""
model_options = ["resnet18", "resnet50"]
lr_options = [1e-2, 1e-3, 1e-4]
loss_options = ["ce"]
weight_options = ["imagenet_only", "random", "imagnet_and_random", "random_rgb"]
def do_work(work: "Queue[str]", gpu_idx: int) -> bool:
    while not work.empty():
        experiment = work.get()
        experiment = experiment.replace("GPU", str(gpu_idx))
        print(experiment)
        if not DRY_RUN:
            subprocess.call(experiment.split(" "))
    return True
if __name__ == "__main__":
    work: "Queue[str]" = Queue()
    for (model, lr, loss, weights) in itertools.product(model_options, lr_options, loss_options, weight_options):
        experiment_name = f"{model}_{lr}_{loss}_{weights.replace('_', '_')}"
        output_dir = os.path.join(output_dir, experiment_name)
        log_dir = os.path.join(output_dir, "logs")
        config_file = os.path.join("conf", "resisc45.yaml")
        if not os.path.exists(os.path.join(output_dir, experiment_name)):
            command = (
                "python train.py"
                + f" config_file={config_file}"
                + f" experiment.name={experiment_name}"
                + f" experiment.module.classification_model={model}"
                + f" experiment.module.learning_rate={lr}"
                + f" experiment.module.loss={loss}"
                + f" experiment.module.weights={weights}"
                + f" experiment.datamodule.weights={weights}"
                + f" program.output_dir={output_dir}"
                + f" program.log_dir={log_dir}"
                + f" program.data_dir={DATA_DIR}"
                + " trainer.gpus=[GPU]"
            )
            command = command.strip()
            work.put(command)
        progress = []
        for gpu_idx in GPUS:
            p = Process(target=do_work, args=(work, gpu_idx))
            processes.append(p)
            p.start()
        for p in processes:
            p.join()