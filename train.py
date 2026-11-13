"""FaceProof: train and score the detector in Python.

A Python port of the classifier that index.html trains in the browser
(function trainLogReg). It reads the saved CLIP features, so it needs
no photos, no GPU and no model download:

    pip install numpy
    python train.py

Input:  results/embeddings.json  (CLIP ViT-B/32 features, 512 numbers per face)
Output: accuracy, AI faces caught, real faces kept and ROC AUC on the test set.
"""
import json

import numpy as np

EPOCHS, LR, L2 = 1200, 2.0, 1e-4   # same settings as index.html


def train_logreg(X, y):
    """Logistic regression, full-batch gradient descent, balanced class weights."""
    mean = X.mean(axis=0)
    scale = 1 / np.sqrt(((X - mean) ** 2).sum(axis=1).mean())
    Z = (X - mean) * scale
    n = len(y)
    weight = np.where(y == 1, n / (2 * y.sum()), n / (2 * (n - y.sum())))
    w, b = np.zeros(X.shape[1]), 0.0
    for _ in range(EPOCHS):
        p = 1 / (1 + np.exp(-(Z @ w + b)))
        err = (p - y) * weight / n
        w -= LR * (Z.T @ err + L2 * w)
        b -= LR * err.sum()
    return {"mean": mean, "scale": scale, "w": w, "b": b}


def predict(model, X):
    """Probability that each face is AI-generated."""
    z = (X - model["mean"]) * model["scale"]
    return 1 / (1 + np.exp(-(z @ model["w"] + model["b"])))


def metrics(p_fake, p_real):
    tp, tn = int((p_fake >= 0.5).sum()), int((p_real < 0.5).sum())
    diff = p_fake[:, None] - p_real[None, :]
    auc = ((diff > 0).sum() + 0.5 * (diff == 0).sum()) / diff.size
    return {"accuracy": (tp + tn) / (len(p_fake) + len(p_real)),
            "tp": tp, "n_fake": len(p_fake), "tn": tn, "n_real": len(p_real), "auc": auc}


def show(name, m):
    print(f"{name:<28} accuracy {m['accuracy']:6.1%}   AI caught {m['tp']}/{m['n_fake']}"
          f"   real kept {m['tn']}/{m['n_real']}   AUC {m['auc']:.3f}")


def main():
    data = json.load(open("results/embeddings.json", encoding="utf-8"))
    emb = {c: {s: np.array(data["emb"][c][s]) for s in ("train", "test")} for c in ("real", "fake")}

    # 1. Ready-made detector: its saved scores on the same test faces.
    show("Open-source detector", metrics(np.array(data["existing"]["fake"]),
                                         np.array(data["existing"]["real"])))

    # 2. Ours: frozen CLIP features + logistic regression trained on the new dataset.
    X = np.vstack([emb["fake"]["train"], emb["real"]["train"]])
    y = np.r_[np.ones(len(emb["fake"]["train"])), np.zeros(len(emb["real"]["train"]))]
    model = train_logreg(X, y)
    show("FaceProof (trained)", metrics(predict(model, emb["fake"]["test"]),
                                        predict(model, emb["real"]["test"])))

    # 3. How many new images are needed: train on N generated + N real faces.
    #    Random subsets differ from the browser run, so these values can differ slightly.
    rng = np.random.default_rng(42)
    print("\nN generated + N real -> mean accuracy over 5 random subsets")
    for n in (5, 10, 25, 50, 100, 200):
        accs = []
        for _ in range(5):
            f = emb["fake"]["train"][rng.choice(len(emb["fake"]["train"]), n, replace=False)]
            r = emb["real"]["train"][rng.choice(len(emb["real"]["train"]), n, replace=False)]
            m = train_logreg(np.vstack([f, r]), np.r_[np.ones(n), np.zeros(n)])
            accs.append(metrics(predict(m, emb["fake"]["test"]), predict(m, emb["real"]["test"]))["accuracy"])
        print(f"  N = {n:<4} {np.mean(accs):6.1%}")


if __name__ == "__main__":
    main()
