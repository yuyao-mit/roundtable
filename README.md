# Roundtable Policy: Compositional Large Language Model Agents Aided Scientific Discovery and Proposal

### [![][project-icon]][project-page] | [![][arxiv-icon]][arxiv-paper]

[project-icon]: https://img.shields.io/badge/🌍-Project%20Page-green
[arxiv-icon]: https://img.shields.io/badge/arXiv-2206.01714-b31b1b

<!-- [![][colab]][composable-demo][colab]: https://colab.research.google.com/assets/colab-badge.svg -->
<!-- [![][huggingface]][huggingface-demo][huggingface]: https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Spaces-blue -->


[project-page]: https://energy-based-model.github.io/Compositional-Visual-Generation-with-Composable-Diffusion-Models/
[arxiv-paper]: https://arxiv.org/pdf/2206.01714.pdf
[composable-demo]: https://colab.research.google.com/github/energy-based-model/Compositional-Visual-Generation-with-Composable-Diffusion-Models-PyTorch/blob/main/notebooks/demo.ipynb
[huggingface-demo]: https://huggingface.co/spaces/Shuang59/Composable-Diffusion


## Contributors
[Yu Yao](https://www.linkedin.com/in/yu-yao-8599b5265/) <sup>1*</sup>,
[Jiayi Dong](https://www.linkedin.com/in/jiayi-dong-6a2a6b26b/) <sup>2*</sup>,
[Yilun Du](https://scholar.google.com/citations?user=GRMMc_MAAAAJ&hl=en) <sup>3</sup>,
[Yang Yang](https://scholar.google.com/citations?user=ceCfTvcAAAAJ&hl=en) <sup>2</sup>,
[Ju Li](https://scholar.google.com/citations?user=SHVhdhoAAAAJ&hl=en) <sup>1</sup>

<sup>*</sup> Equal Contribution  
<sup>1</sup> Massachusetts Institute of Technology    
<sup>2</sup> University of California, Los Angeles  
<sup>3</sup> Harvard University  


## Updates:
- 2025/02/17: Github repo set up
- 2925/02/22: Project release

## Table of Contents
- [Overview](#Overview-of-Roundtable-Policy)
- [Benchmark](#benchmark)
- [Licensing Information](#licensing-information)
- [Disclaimer](#disclaimer)
- [Citation](#citation) 

## Overview of Roundtable Policy

<p align="center">
  <img src="figures/cover_roundtable.png" alt="Framework for ROUNDTABLE POLICY" width="45%">
  <img src="figures/roundtablechat.png" alt="Internal pipeline" width="55%">
</p>


Recent advancements in large language models (LLMs) have demonstrated their exceptional potential across a wide range of scientific applications, including predictive modeling and generative analysis. However, no single LLM excels at all tasks simultaneously—some models are optimized for high-precision numerical predictions, while others specialize in generating coherent, context-rich text. To address this limitation, we introduce \textsc{Roundtable Policy}, guided by which a multi-LLM agent framework is designed for scientific discovery and proposal generation. Central to our approach are two key concepts: the \textit{Arbitrator}, which serves as an intelligent aggregator, and the \textit{confidence weight table}, a dynamic mechanism that optimally weights the contributions of different expert models. To evaluate the efficacy of our framework, we benchmarked it against single-model baselines on the task of perovskite solar cell property prediction and decision-making. In this framework, multiple LLMs—each acting as an independent “expert”—are trained on the same multimodal dataset and leverage their specialized capabilities to generate diverse outputs. These outputs are then fused through a “roundtable discussion,” where the Arbitrator agent systematically compiles, compares, and integrates each expert’s response. The final answer is refined based on the collective intelligence of all models weighted by confidence weight table. Unlike conventional LLM pipelines that rely on extensive parameter tuning, our \textit{confidence weight table} is trainable yet computationally lightweight, enabling rapid adaptation to new tasks while maintaining high performance. Experimental results demonstrate that our ensemble strategy consistently outperforms single-model baselines across both predictive and generative tasks. Furthermore, our approach achieves state-of-the-art performance across multiple input modalities, highlighting its robustness and adaptability in scientific applications.

## Benchmark

To prevent benchmark data contamination, we only provide the annotation sheet on [Huggingface](https://huggingface.co/datasets/osunlp/ScienceAgentBench), which includes all necessary *inputs* to run an agent.

To evaluate the agent outcomes, i.e. generated code, please download the full benchmark [here](https://buckeyemailosu-my.sharepoint.com/:u:/g/personal/chen_8336_buckeyemail_osu_edu/EQuA6uJ3CtRHvRfZ2GiN1tYBRVJE4DSUD10MW61fr7HuSQ?e=sCBegG) and unzip it with password `scienceagentbench`.


## Licensing Information

Most tasks in '''Roundtable Policy: Compositional Large Language Model Agents Aided Scientific Discovery and Proposal''' is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0 International License</a>.

Code under this repo is licensed under a MIT License.

## Disclaimer

Our benchmark is constructed by adapting open-source code and data, to which we respect their creators' ownership and intellectual property. In the Appendix of our paper, we have made our best effort to cite the original papers, list the repositories, and provide their licenses.<\br>
We give sincere acknowledgement to the following copyrighted repositories:

[rasterio/rasterio](https://github.com/rasterio/rasterio)<br>
[hackingmaterials/matminer](https://github.com/hackingmaterials/matminer)<br>
[ScienceAgentBench](https://github.com/OSU-NLP-Group/ScienceAgentBench)<br>

We welcome requests from the original authors to modify or remove relevant tasks related to those two repositories if needed.

## Citation

If you find our code and data useful, please cite our paper:

```
@article{yao2025roundtable1.0,
      title={Roundtable Policy: Compositional Large Language Model Agents Aided Scientific Discovery and Proposal}, 
      author={Yu Yao and Jiayi Dong and Yilun Du and Yang Yang and Ju Li},
      journal={arXiv preprint arXiv:2502.xxxxx},
      year={2025}
}
```
