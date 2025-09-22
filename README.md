# Game AI: Minimax vs Q-Learning

This repository implements and compares **search-based** (Minimax, Minimax with Alpha-Beta Pruning) and **learning-based** (Q-Learning) AI strategies for two classic board games: **Tic Tac Toe** and **Connect 4**.

---

## 📖 Project Overview
The project investigates algorithm performance under different game complexities:

- **Tic Tac Toe**: Small state space, solvable exhaustively.  
- **Connect 4**: Large state space, requiring depth limits and heuristics.

### 🔑 Key Takeaways
- **Minimax** guarantees optimal play but is computationally expensive.  
- **Alpha-Beta Pruning** reduces node exploration by up to **87%**.  
- **Q-Learning** underperforms in Tic Tac Toe but achieves **54% win rate** in Connect 4.  

---

## 📂 Folder Structure

```
├── algorithms/        # Minimax, Minimax-AB, Q-Learning implementations
├── experiments/       # Scripts for running and benchmarking experiments
├── games/             # Game logic for Tic Tac Toe and Connect 4
├── models/            # Saved Q-learning models / state representations
├── opponents/         # Semi-intelligent baseline opponents
├── results/           # CSVs, logs, and evaluation outputs
├── utils/             # Helper functions (evaluation, metrics, configs)
├── visualization/     # Plotting and result visualization tools
├── demo.py            # Example run showcasing algorithms in action
├── main.py            # Main entry point to run experiments
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8+  
- Recommended: create a virtual environment  
- Install dependencies:
```bash
pip install -r requirements.txt
```

### Run Experiments
Run demo games:
```bash
python demo.py
```

Run full experiment suite:
```bash
python main.py
```

Results will be saved in the `results/` folder.  

---

## 📊 Example Results

- **Tic Tac Toe**  
  - Minimax & Minimax-AB dominate with >80% win rate vs baseline.  
  - Q-Learning struggles, achieving only ~8%.  

- **Connect 4**  
  - Minimax (depth=4) achieves ~100% win rate.  
  - Q-Learning is more competitive, ~54% win rate.  

---

## 📈 Visualization

The `visualization/` module provides:
- Win/Draw/Loss distributions  
- Execution time comparisons  
- Node exploration statistics  
- Alpha-Beta pruning efficiency plots  

---

## 📘 References
- Allis, V. (1988). *A knowledge-based approach of Connect-4*.  
- Sutton & Barto (2018). *Reinforcement Learning: An Introduction*.  
- Campbell et al. (2002). *Deep Blue*.  

---

## 👩‍💻 Author
**Vishaalini Ramasamy Manikandan**  
MSc Computer Science (Data Science), Trinity College Dublin  
