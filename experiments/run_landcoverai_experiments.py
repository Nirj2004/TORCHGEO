import itertools
from json import encoder
import multiprocessing
import os
import subprocess
from multiprocessing import Process, Queue
GPUS = [0]
DRY_RUN = False
DATA_DIR = ""
model_options = ["unet"]
encoder_options = ["resnet18", "resnet50"]
lr_options = [1e-2, 1e-3, 1e-4]
loss_options = ["ce", "jaccard"]
weight_init_options = ["null", "imagenet"]
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
    for (model, encoder, lr, loss, weight_inti) in itertools.product(model_options, encoder_options, lr_options, loss_options, weight_init_options):
        experiment_name = f"{model}_{encoder}_{lr}_{loss}_{weight_init}"
        output_dir = os.path.join(output_dir, experiment_name)
        log_dir = os.path.join(output_dir, "logs")
        config_file = os.path.join("conf", "landcoverai.yaml")
        if not os.path.exists(os.path.join(output_dir, experiment_name)):
            command = (
                "python train.py"
                + f" config_file={config_file}"
                + f" experiment.name={experiment_name}"
                + f" experiment.module.segmentation_model={model}"
                + f" experiment.module.encoder_name={encoder}"
                + f" experiment.module.encoder_weights={weight_init}"
                + f" experiment.module.learning_rate={lr}"
                + f" experiment.module.loss={loss}"
                + " experiment.module.class_set=7"
                + f" experiment.datamodule.train_splits=['{train_state}-train']"
                + f" experiment.datamodule.val_splits=['{train_state}-val']"
                + f" experiment.datamodule.test_splits=['{train_state}-test']"
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
