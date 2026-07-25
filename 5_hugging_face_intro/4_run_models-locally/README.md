# Run (Locally - Windows)

Run in terminal commands

```bash
uv venv --seed
uv run --with jupyter jupyter lab
```

Copy Jupyter server address in the output of the terminal
Ex. `http://127.0.0.1:8888/lab?token=7bd8bdcebb53d85b2d9d9740b38d2203d03e47fe13fd454e`

In VSCode Open Jupyter notebook, in the right corner select
`Select Kernel` > `Select Another Kernel` > `Existing Jupyter Server` > paste the URL from terminal `http://127.0.0.1:8888/lab?token=7bd8bdcebb53d85b2d9d9740b38d2203d03e47fe13fd454e` > Enter



# Run (Runpod.io - Via VSCode)

Create a pod:

- RTX A5000 GPU
- Storage 100GB

1) Open Jupyter notebook and copy url ex. `https://mspd2urui5j44q-8888.proxy.runpod.net`

2) Copy Jupyter server password from EnvVars of the RunPod pod.

3) In VSCode in python notebook `Select Kernel` > `Existing Jupyter Server` > paste the URL of Jupyter notebook on runpod ex. `https://mspd2urui5j44q-8888.proxy.runpod.net` > Paste password from EnvVars ex. `yvxddft167mr2zilppi9` > Enter

> ⚠️ Note: `Select Kernel > Existing Jupyter Server` only borrows the **remote kernel** to run
> the cells on the GPU. The `.ipynb` **file stays on your laptop** — it is never written to the
> pod. That is fine for running cells, but it means Claude Code's Jupyter MCP (see below) has no
> server-side document to attach to.

